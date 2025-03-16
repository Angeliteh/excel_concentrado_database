import PySimpleGUI as sg
from ..utils.db_utils import ejecutar_consulta

class ConsultaWindow:
    def __init__(self, nombre_bd):
        self.nombre_bd = nombre_bd
        self.consultas_predefinidas = {
            "Total de alumnos por periodo": """
                SELECT p.nombre_periodo, 
                       SUM(m.cantidad_h) as total_hombres, 
                       SUM(m.cantidad_m) as total_mujeres,
                       SUM(m.cantidad_h + m.cantidad_m) as total
                FROM movimiento_alumnos m
                JOIN periodos p ON m.id_periodo = p.id_periodo
                GROUP BY m.id_periodo
                ORDER BY m.id_periodo
            """,
            "Estadísticas por concepto": """
                SELECT c.nombre_concepto,
                       SUM(m.cantidad_h) as total_hombres,
                       SUM(m.cantidad_m) as total_mujeres,
                       SUM(m.cantidad_h + m.cantidad_m) as total
                FROM movimiento_alumnos m
                JOIN conceptos c ON m.id_concepto = c.id_concepto
                GROUP BY c.nombre_concepto
            """
        }

    def crear_layout(self):
        return [
            [sg.Text("Consultas predefinidas:")],
            [sg.Combo(list(self.consultas_predefinidas.keys()), 
                     key="-CONSULTA-", size=(40, 1))],
            [sg.Button("Ejecutar consulta"), 
             sg.Button("Consulta personalizada")],
            [sg.Output(size=(80, 20), key="-OUTPUT-")],
            [sg.Button("Salir")]
        ]

    def ejecutar(self):
        window = sg.Window("Consultas a Base de Datos", self.crear_layout())

        while True:
            event, values = window.read()

            if event in (sg.WINDOW_CLOSED, "Salir"):
                break

            if event == "Ejecutar consulta":
                self._ejecutar_consulta_predefinida(values["-CONSULTA-"])

            if event == "Consulta personalizada":
                self._ejecutar_consulta_personalizada()

        window.close()

    def _ejecutar_consulta_predefinida(self, consulta_seleccionada):
        if not consulta_seleccionada:
            sg.popup_error("Selecciona una consulta")
            return

        try:
            sql = self.consultas_predefinidas[consulta_seleccionada]
            resultado = ejecutar_consulta(self.nombre_bd, sql)
            print(f"\n--- {consulta_seleccionada} ---\n")
            print(resultado)
        except Exception as e:
            print(f"Error al ejecutar la consulta: {str(e)}")

    def _ejecutar_consulta_personalizada(self):
        sql = sg.popup_get_text(
            "Ingresa tu consulta SQL:",
            title="Consulta personalizada"
        )
        if sql:
            try:
                resultado = ejecutar_consulta(self.nombre_bd, sql)
                print("\n--- Consulta personalizada ---\n")
                print(resultado)
            except Exception as e:
                print(f"Error al ejecutar la consulta: {str(e)}")