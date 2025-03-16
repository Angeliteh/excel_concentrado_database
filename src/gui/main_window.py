import PySimpleGUI as sg
import pandas as pd
from ..config.settings import RUTA_SALIDA_DEFAULT
from ..procesador.procesador import ProcesadorDatosEscolares
from ..utils.db_utils import verificar_datos

class MainWindow:
    def __init__(self):
        self.procesador = ProcesadorDatosEscolares()
        sg.theme('DefaultNoMoreNagging')
        self.window = None

    def crear_layout(self):
        return [
            [sg.Frame('Procesamiento de Archivos Excel', [
                [sg.Text("Selecciona los archivos Excel:")],
                [sg.Input(key="-ARCHIVOS-"), 
                 sg.FilesBrowse("Buscar", file_types=(("Excel Files", "*.xlsx"),))],
                [sg.Text("Guardar resultado en:")],
                [sg.Input(default_text=RUTA_SALIDA_DEFAULT, key="-ARCHIVO_FINAL-"), 
                 sg.SaveAs("Guardar como", file_types=(("Excel Files", "*.xlsx"),))],
                [sg.Button("Procesar Excel", key="-PROCESAR_EXCEL-")]
            ])],
            [sg.Frame('Procesamiento con Base de Datos', [
                [sg.Text("Periodo:")],
                [sg.Input(key="-PERIODO-")],
                [sg.Button("Procesar en BD", key="-PROCESAR_BD-")]
            ])],
            [sg.Output(size=(60, 20), key='-OUTPUT-')],  # Área para mostrar la depuración
            [sg.Button("Limpiar Log"), sg.Button("Salir")]
        ]

    def ejecutar(self):
        self.window = sg.Window("Procesador de Datos Escolares", self.crear_layout(), resizable=True)
        
        while True:
            event, values = self.window.read()
            
            if event == sg.WINDOW_CLOSED or event == "Salir":
                break
                
            if event == "Limpiar Log":
                self.window['-OUTPUT-'].update('')
                
            if event == "-PROCESAR_EXCEL-":
                try:
                    print("=== Iniciando Procesamiento Excel ===")
                    archivos = values["-ARCHIVOS-"].split(";")
                    archivo_final = values["-ARCHIVO_FINAL-"]
                    
                    if not archivos or not archivo_final:
                        sg.popup_error("Por favor selecciona archivos y una ubicación de salida")
                        continue
                        
                    datos = self.procesador.procesar_archivos(archivos)
                    self.procesador.guardar_resultados(datos, archivo_final)
                    
                    print("=== Procesamiento Excel Completado ===")
                    sg.popup("Proceso Excel completado con éxito")
                except Exception as e:
                    print(f"ERROR: {str(e)}")
                    sg.popup_error(f"Error durante el proceso Excel: {str(e)}")
            
            if event == "-PROCESAR_BD-":
                try:
                    print("=== Iniciando Procesamiento BD ===")
                    archivos = values["-ARCHIVOS-"].split(";")
                    periodo = values["-PERIODO-"]
                    
                    if not archivos or not periodo:
                        sg.popup_error("Por favor selecciona archivos e ingresa el periodo")
                        continue
                        
                    verificar_datos(archivos, periodo)
                    
                    print("=== Procesamiento BD Completado ===")
                    sg.popup("Proceso BD completado con éxito")
                except Exception as e:
                    print(f"ERROR: {str(e)}")
                    sg.popup_error(f"Error durante el proceso BD: {str(e)}")
        
        self.window.close()
