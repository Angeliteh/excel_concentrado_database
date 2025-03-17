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
            [sg.Text("=== Procesador de Datos Escolares ===", font=('Helvetica', 12, 'bold'))],
            [sg.Frame('Selección de Archivos', [
                [sg.Text("Selecciona los archivos Excel:")],
                [sg.Input(key="-ARCHIVOS-"), 
                 sg.FilesBrowse("Buscar", file_types=(("Excel Files", "*.xlsx"),))]
            ])],
            [sg.Frame('Proceso Excel (Método Original)', [
                [sg.Text("Guardar resultado consolidado en:")],
                [sg.Input(default_text=RUTA_SALIDA_DEFAULT, key="-ARCHIVO_FINAL-"), 
                 sg.SaveAs("Guardar como", file_types=(("Excel Files", "*.xlsx"),))],
                [sg.Button("Procesar Excel", key="-PROCESAR_EXCEL-")]
            ])],
            [sg.Frame('Proceso Base de Datos', [
                [sg.Text("Base de datos: " + DB_CONFIG['database'])],
                [sg.Button("Procesar en BD", key="-PROCESAR_BD-"),
                 sg.Button("Ver Datos en BD", key="-VER_BD-")]
            ])],
            [sg.Frame('Log de Proceso', [
                [sg.Output(size=(60, 20), key='-OUTPUT-')],
                [sg.Button("Limpiar Log")]
            ])],
            [sg.Button("Salir")]
        ]

    def validar_archivos_entrada(self, archivos):
        """Valida que se hayan seleccionado archivos"""
        if not archivos or archivos[0] == '':
            sg.popup_error("Por favor selecciona archivos para procesar")
            return False
        return True

    def procesar_excel(self, archivos, archivo_final):
        """Ejecuta el proceso original de Excel"""
        print("\n=== Iniciando Procesamiento Excel ===")
        print(f"Archivos a procesar: {len(archivos)}")
        for archivo in archivos:
            print(f"- {archivo}")
        
        datos = self.procesador.procesar_archivos(archivos)
        self.procesador.guardar_resultados(datos, archivo_final)
        
        print("\n=== Procesamiento Excel Completado ===")
        print(f"Archivo generado: {archivo_final}")
        sg.popup("Proceso Excel completado con éxito")

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
            resizable=True
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
        
        self.window.close()