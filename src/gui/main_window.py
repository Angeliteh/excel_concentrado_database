import PySimpleGUI as sg
import pandas as pd
from ..config.settings import (
    RUTA_SALIDA_DEFAULT,
    RANGOS_EXCEL,
    NOMBRE_HOJAS,
    DB_CONFIG
)
from ..procesador.procesador import ProcesadorDatosEscolares
from ..procesador.normalizador import NormalizadorDatosEscolares
from ..utils.db_utils import procesar_archivos_db

class MainWindow:
    def __init__(self):
        # Inicializadores para el proceso Excel
        self.procesador = ProcesadorDatosEscolares()
        self.normalizador = NormalizadorDatosEscolares()
        sg.theme('DefaultNoMoreNagging')
        self.window = None

    def crear_layout(self):
        return [
            [sg.Text("=== Procesador de Datos Escolares ===", font=('Helvetica', 12, 'bold'), expand_x=True, justification='center')],
            [sg.Text("Estado: Listo para procesar", key='-ESTADO-', font=('Helvetica', 10), text_color='green', expand_x=True)],
            [sg.Frame('Selección de Archivos', [
                [sg.Text("Selecciona los archivos Excel:")],
                [sg.Input(key="-ARCHIVOS-", expand_x=True),
                 sg.FilesBrowse("Buscar", file_types=(("Excel Files", "*.xlsx"),))]
            ], expand_x=True)],
            [sg.Frame('Proceso Excel (Método Original)', [
                [sg.Text("Guardar resultado consolidado en:")],
                [sg.Input(default_text=RUTA_SALIDA_DEFAULT, key="-ARCHIVO_FINAL-", expand_x=True),
                 sg.SaveAs("Guardar como", file_types=(("Excel Files", "*.xlsx"),))],
                [sg.Button("Procesar Excel", key="-PROCESAR_EXCEL-")]
            ], expand_x=True)],
            [sg.Frame('Proceso Base de Datos', [
                [sg.Text("Base de datos: " + DB_CONFIG['database'])],
                [sg.Button("Procesar en BD", key="-PROCESAR_BD-"),
                 sg.Button("Ver Datos en BD", key="-VER_BD-")]
            ], expand_x=True)],
            [sg.Frame('🔄 Proceso Secuencial (Nuevo)', [
                [sg.Text("Procesa archivos paso a paso para verificar cada etapa", font=('Helvetica', 9, 'italic'))],
                [sg.Button("🔍 Proceso Secuencial", key="-PROCESO_SECUENCIAL-", button_color=('white', 'blue'))]
            ], expand_x=True)],
            [sg.Frame('Log de Proceso', [
                [sg.Output(size=(80, 25), key='-OUTPUT-', expand_x=True, expand_y=True)],  # Se expande en ambas direcciones
                [sg.Button("Limpiar Log")]
            ], expand_x=True, expand_y=True)],
            [sg.Button("Salir", expand_x=True)]
        ]

    def validar_archivos_entrada(self, archivos):
        """Valida que se hayan seleccionado archivos"""
        if not archivos or archivos[0] == '':
            sg.popup_error("Por favor selecciona archivos para procesar")
            return False
        return True

    def procesar_excel(self, archivos, archivo_final):
        """Ejecuta el proceso original de Excel con logs detallados"""
        try:
            self.window['-ESTADO-'].update("Procesando archivos...", text_color='orange')
            self.window.refresh()

            print("\n" + "="*60)
            print("🚀 INICIANDO PROCESAMIENTO EXCEL")
            print("="*60)
            print(f"📁 Archivos a procesar: {len(archivos)}")
            for i, archivo in enumerate(archivos, 1):
                print(f"   {i}. {archivo}")
            print()

            # Procesar cada archivo individualmente para mostrar detalles
            datos_consolidados = {'tabla_1': None, 'tabla_2': None}

            for i, archivo in enumerate(archivos, 1):
                print(f"🔄 Procesando archivo {i}/{len(archivos)}: {archivo}")
                print("-" * 50)

                datos_archivo = self.procesador.procesar_archivo_individual(archivo)

                # Mostrar resumen de datos extraídos
                for tabla_nombre, tabla_datos in datos_archivo.items():
                    print(f"📊 {tabla_nombre.upper()}:")
                    print(f"   - Dimensiones: {tabla_datos.shape}")
                    print(f"   - Suma total: {tabla_datos.sum().sum():.2f}")

                # Consolidar datos
                for tabla in ['tabla_1', 'tabla_2']:
                    if datos_consolidados[tabla] is None:
                        datos_consolidados[tabla] = datos_archivo[tabla]
                        print(f"   ✅ {tabla} inicializada")
                    else:
                        datos_consolidados[tabla] += datos_archivo[tabla]
                        print(f"   ➕ {tabla} sumada")

                print()

            # Mostrar resumen final
            print("📈 RESUMEN CONSOLIDADO:")
            print("-" * 30)
            for tabla_nombre, tabla_datos in datos_consolidados.items():
                print(f"🎯 {tabla_nombre.upper()}:")
                print(f"   - Dimensiones finales: {tabla_datos.shape}")
                print(f"   - Suma total consolidada: {tabla_datos.sum().sum():.2f}")
            print()

            self.window['-ESTADO-'].update("Guardando resultados...", text_color='orange')
            self.window.refresh()

            print("💾 Guardando resultados en plantilla...")
            self.procesador.guardar_resultados(datos_consolidados, archivo_final)

            self.window['-ESTADO-'].update("✅ Proceso completado exitosamente", text_color='green')

            print("\n" + "="*60)
            print("🎉 PROCESAMIENTO EXCEL COMPLETADO")
            print("="*60)
            print(f"📄 Archivo generado: {archivo_final}")
            print("="*60)

            sg.popup("Proceso Excel completado con éxito")

        except Exception as e:
            self.window['-ESTADO-'].update(f"❌ Error: {str(e)}", text_color='red')
            raise

    def procesar_bd(self, archivos):
        """Ejecuta el proceso de Base de Datos"""
        print("\n=== Iniciando Procesamiento BD ===")
        print(f"Archivos a procesar: {len(archivos)}")
        for archivo in archivos:
            print(f"- {archivo}")
        
        config = {
            'rangos': RANGOS_EXCEL,
            'hojas': NOMBRE_HOJAS,
            'conceptos_excel': self.normalizador.conceptos_excel
        }
        
        procesar_archivos_db(archivos, config)
        
        print("\n=== Procesamiento BD Completado ===")
        sg.popup("Proceso BD completado con éxito")

    def ejecutar(self):
        self.window = sg.Window(
            "Procesador de Datos Escolares",
            self.crear_layout(),
            resizable=True,
            size=(1000, 700),  # Ventana más ancha y alta
            finalize=True
        )
        
        while True:
            event, values = self.window.read()
            
            if event in (sg.WINDOW_CLOSED, "Salir"):
                break
                
            if event == "Limpiar Log":
                self.window['-OUTPUT-'].update('')
                
            if event == "-PROCESAR_EXCEL-":
                try:
                    archivos = values["-ARCHIVOS-"].split(";")
                    archivo_final = values["-ARCHIVO_FINAL-"]
                    
                    if not self.validar_archivos_entrada(archivos):
                        continue
                        
                    if not archivo_final:
                        sg.popup_error("Por favor selecciona una ubicación de salida")
                        continue
                        
                    self.procesar_excel(archivos, archivo_final)
                    
                except Exception as e:
                    print(f"ERROR en proceso Excel: {str(e)}")
                    sg.popup_error(f"Error durante el proceso Excel: {str(e)}")
            
            if event == "-PROCESAR_BD-":
                try:
                    archivos = values["-ARCHIVOS-"].split(";")
                    
                    if not self.validar_archivos_entrada(archivos):
                        continue
                        
                    self.procesar_bd(archivos)
                    
                except Exception as e:
                    print(f"ERROR en proceso BD: {str(e)}")
                    sg.popup_error(f"Error durante el proceso BD: {str(e)}")
            
            if event == "-VER_BD-":
                try:
                    from ..gui.consulta_window import ConsultaWindow
                    ventana_consulta = ConsultaWindow(DB_CONFIG['database'])
                    self.window.Hide()
                    ventana_consulta.ejecutar()
                    self.window.UnHide()
                except Exception as e:
                    print(f"ERROR al abrir ventana de consultas: {str(e)}")
                    sg.popup_error(f"Error al abrir ventana de consultas: {str(e)}")

            if event == "-PROCESO_SECUENCIAL-":
                try:
                    from ..gui.proceso_secuencial_window import ProcesoSecuencialWindow
                    ventana_proceso = ProcesoSecuencialWindow()
                    self.window.Hide()
                    ventana_proceso.ejecutar()
                    self.window.UnHide()
                except Exception as e:
                    print(f"ERROR al abrir proceso secuencial: {str(e)}")
                    sg.popup_error(f"Error al abrir proceso secuencial: {str(e)}")
        
        self.window.close()