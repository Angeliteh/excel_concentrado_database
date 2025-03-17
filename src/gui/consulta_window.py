import PySimpleGUI as sg
import pandas as pd
from ..utils.db_utils import ejecutar_consulta
from ..utils.excel_utils import extraer_tabla_y_limpiar, cargar_excel
import traceback

class ConsultaWindow:
    def __init__(self, db_path):
        print("Iniciando ConsultaWindow...")
        self.db_path = db_path
        self.window = None
        self.datos_estructurados = None
        self.datos_normalizados = None
        sg.theme('DefaultNoMoreNagging')

    def limpiar_y_estructurar_datos(self, df):
        """Limpia y estructura los datos para que se parezcan al Excel original"""
        try:
            # Mapeo de columnas del DataFrame original a las columnas deseadas
            mapeo_columnas = {
                '1o._H': 7,    '1o._M': 8,
                '2o._H': 9,    '2o._M': 10,
                '3o._H': 11,   '3o._M': 12,
                '4o._H': 13,   '4o._M': 14,
                '5o._H': 15,   '5o._M': 16,
                '6o._H': 17,   '6o._M': 18,
                'SUBTOTAL_H': 19, 'SUBTOTAL_M': 20,
                'TOTAL': 21
            }
            
            # Definir conceptos y columnas
            conceptos = [
                'PREINSCRIPCIÓN 1ER. GRADO', 'INSCRIPCIÓN', 'BAJAS', 'EXISTENCIA',
                'ALTAS', 'BECADOS MUNICIPIO', 'BECADOS SEED', 'BIENESTAR', 'GRUPOS'
            ]
            
            columnas = ['CONCEPTO']
            for grado in ['1o.', '2o.', '3o.', '4o.', '5o.', '6o.']:
                columnas.extend([f'{grado}_H', f'{grado}_M'])
            columnas.extend(['SUBTOTAL_H', 'SUBTOTAL_M', 'TOTAL'])
            
            # Crear DataFrame final
            datos_finales = []
            
            for concepto in conceptos:
                fila = df[df.iloc[:, 0] == concepto]
                if len(fila) > 0:
                    fila = fila.iloc[0]
                    valores = [concepto]
                    
                    # Extraer valores usando el mapeo
                    for columna in columnas[1:]:  # Skip 'CONCEPTO'
                        idx = mapeo_columnas.get(columna)
                        if idx is not None and idx < len(fila):
                            valor = fila[idx]
                            valores.append(float(valor) if pd.notna(valor) else 0)
                        else:
                            valores.append(0)
                    
                    datos_finales.append(valores)
            
            datos_limpios = pd.DataFrame(datos_finales, columns=columnas)
            
            return None, datos_limpios
        
        except Exception as e:
            print(f"Error en limpiar_y_estructurar_datos: {str(e)}")
            print(traceback.format_exc())
            raise

    def normalizar_datos_movimiento(self, df):
        """Normaliza los datos de movimiento de alumnos"""
        print("Normalizando datos de movimiento...")
        try:
            datos_normalizados = []
            
            for _, row in df.iterrows():
                concepto = row['CONCEPTO']
                
                for grado in ['1o.', '2o.', '3o.', '4o.', '5o.', '6o.']:
                    # Procesar datos para hombres
                    valor_h = float(row[f'{grado}_H']) if pd.notna(row[f'{grado}_H']) else 0
                    datos_normalizados.append({
                        'grado': grado,
                        'genero': 'H',
                        'concepto': concepto,
                        'valor': valor_h,
                        'tipo': 'MOVIMIENTO'
                    })
                    
                    # Procesar datos para mujeres
                    valor_m = float(row[f'{grado}_M']) if pd.notna(row[f'{grado}_M']) else 0
                    datos_normalizados.append({
                        'grado': grado,
                        'genero': 'M',
                        'concepto': concepto,
                        'valor': valor_m,
                        'tipo': 'MOVIMIENTO'
                    })
            
            df_normalizado = pd.DataFrame(datos_normalizados)
            print(f"Datos normalizados creados con forma: {df_normalizado.shape}")
            return df_normalizado
            
        except Exception as e:
            print(f"Error en normalizar_datos_movimiento: {str(e)}")
            print(traceback.format_exc())
            raise

    def crear_layout(self):
        print("Creando layout...")
        return [
            [sg.Text("Datos Almacenados", font=('Helvetica', 12, 'bold'))],
            [sg.Button("Cargar Archivo", key='-CARGAR-')],
            [sg.TabGroup([
                [sg.Tab('Datos Estructurados', [
                    [sg.Multiline(
                        size=(80, 20),
                        key='-DATOS_ESTRUCTURADOS-',
                        disabled=True,
                        font='Courier 10'
                    )]
                ]),
                sg.Tab('Datos Normalizados', [
                    [sg.Multiline(
                        size=(80, 20),
                        key='-DATOS_NORMALIZADOS-',
                        disabled=True,
                        font='Courier 10'
                    )]
                ])]
            ], key='-TABGROUP-')],
            [
                sg.Button("Exportar Estructurados", key='-EXPORTAR_ESTRUCTURADOS-'),
                sg.Button("Exportar Normalizados", key='-EXPORTAR_NORMALIZADOS-'),
                sg.Button("Cerrar")
            ]
        ]

    def obtener_archivo_seleccionado(self):
        """Muestra un diálogo para seleccionar archivo"""
        print("Solicitando selección de archivo...")
        try:
            archivo = sg.popup_get_file(
                'Seleccionar archivo Excel',
                file_types=(('Excel Files', '*.xlsx'),),
                no_window=True
            )
            if archivo:
                print(f"Archivo seleccionado: {archivo}")
            else:
                print("No se seleccionó ningún archivo")
            return archivo
        except Exception as e:
            print(f"Error al seleccionar archivo: {str(e)}")
            print(traceback.format_exc())
            raise

    def ejecutar(self):
        print("Iniciando ejecución de la ventana...")
        self.window = sg.Window(
            "Visualización de Datos",
            self.crear_layout(),
            resizable=True,
            finalize=True
        )

        while True:
            try:
                event, values = self.window.read()
                print(f"Evento recibido: {event}")
                
                if event in (sg.WINDOW_CLOSED, "Cerrar"):
                    print("Cerrando ventana...")
                    break
                    
                elif event == '-CARGAR-':
                    try:
                        archivo_excel = self.obtener_archivo_seleccionado()
                        if archivo_excel:
                            print(f"Procesando archivo: {archivo_excel}")
                            hoja = cargar_excel(archivo_excel, 'ZONA3')
                            tabla_cruda = extraer_tabla_y_limpiar(hoja, (3, 1, 15, 26))
                            df = pd.DataFrame(tabla_cruda)
                            
                            titulo, self.datos_estructurados = self.limpiar_y_estructurar_datos(df)
                            self.datos_normalizados = self.normalizar_datos_movimiento(self.datos_estructurados)
                            
                            # Actualizar visualización
                            self.window['-DATOS_ESTRUCTURADOS-'].update(
                                self.datos_estructurados.to_string(index=False)
                            )
                            self.window['-DATOS_NORMALIZADOS-'].update(
                                self.datos_normalizados.to_string(index=False)
                            )
                            sg.popup("Datos cargados exitosamente")
                            
                    except Exception as e:
                        print(f"Error al cargar archivo: {str(e)}")
                        print(traceback.format_exc())
                        sg.popup_error(f"Error al cargar archivo: {str(e)}")
                        
                elif event == '-EXPORTAR_ESTRUCTURADOS-':
                    if self.datos_estructurados is not None:
                        try:
                            filename = sg.popup_get_file(
                                'Guardar como',
                                save_as=True,
                                file_types=(('Excel Files', '*.xlsx'),)
                            )
                            if filename:
                                self.datos_estructurados.to_excel(filename, index=False)
                                sg.popup("Archivo guardado exitosamente")
                        except Exception as e:
                            print(f"Error al exportar: {str(e)}")
                            sg.popup_error(f"Error al exportar: {str(e)}")
                    else:
                        sg.popup_error("No hay datos para exportar. Por favor cargue un archivo primero.")
                        
                elif event == '-EXPORTAR_NORMALIZADOS-':
                    if self.datos_normalizados is not None:
                        try:
                            filename = sg.popup_get_file(
                                'Guardar como',
                                save_as=True,
                                file_types=(('Excel Files', '*.xlsx'),)
                            )
                            if filename:
                                self.datos_normalizados.to_excel(filename, index=False)
                                sg.popup("Archivo guardado exitosamente")
                        except Exception as e:
                            print(f"Error al exportar: {str(e)}")
                            sg.popup_error(f"Error al exportar: {str(e)}")
                    else:
                        sg.popup_error("No hay datos para exportar. Por favor cargue un archivo primero.")

            except Exception as e:
                print(f"Error en el loop principal: {str(e)}")
                print(traceback.format_exc())
                sg.popup_error(f"Error inesperado: {str(e)}")

        print("Cerrando ventana final...")
        self.window.close()