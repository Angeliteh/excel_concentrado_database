import PySimpleGUI as sg
import pandas as pd
from ..utils.db_utils import ejecutar_consulta

class ConsultaWindow:
    def __init__(self, db_path):
        self.db_path = db_path
        self.window = None
        sg.theme('DefaultNoMoreNagging')

    def crear_layout(self):
        return [
            [sg.Text("Datos Almacenados", font=('Helvetica', 12, 'bold'))],
            [sg.TabGroup([
                [sg.Tab('Movimiento Alumnos', [
                    [sg.Table(
                        values=[[]],
                        headings=[],
                        auto_size_columns=True,
                        num_rows=15,
                        key='-TABLA_ALUMNOS-',
                        justification='right'
                    )]
                ]),
                sg.Tab('Periodos Proceso', [
                    [sg.Table(
                        values=[[]],
                        headings=[],
                        auto_size_columns=True,
                        num_rows=15,
                        key='-TABLA_PERIODOS-',
                        justification='right'
                    )]
                ])]
            ], key='-TABGROUP-', enable_events=True)],
            [sg.Button("Actualizar"), sg.Button("Cerrar")]
        ]

    def ejecutar(self):
        self.window = sg.Window(
            "Visualización de Datos",
            self.crear_layout(),
            resizable=True,
            finalize=True
        )
        
        self.actualizar_datos()

        while True:
            event, values = self.window.read()
            if event in (sg.WINDOW_CLOSED, "Cerrar"):
                break
            elif event == "Actualizar":
                self.actualizar_datos()

        self.window.close()

    def actualizar_datos(self):
        try:
            # Consultar datos de alumnos
            df_alumnos = ejecutar_consulta("SELECT * FROM datos_alumnos")
            if len(df_alumnos) > 0:
                self.window['-TABLA_ALUMNOS-'].update(
                    values=df_alumnos.values.tolist(),
                    headings=df_alumnos.columns.tolist()
                )
            
            # Consultar datos de periodos
            df_periodos = ejecutar_consulta("SELECT * FROM datos_periodos")
            if len(df_periodos) > 0:
                self.window['-TABLA_PERIODOS-'].update(
                    values=df_periodos.values.tolist(),
                    headings=df_periodos.columns.tolist()
                )
                
        except Exception as e:
            sg.popup_error(f"Error al consultar datos: {str(e)}")
