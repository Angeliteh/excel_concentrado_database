import PySimpleGUI as sg
import pandas as pd
from ..utils.excel_utils import cargar_excel
from ..procesador.procesador import ProcesadorDatosEscolares
from ..config.settings import NOMBRE_HOJAS, RANGOS_EXCEL
import traceback

class ProcesoSecuencialWindow:
    def __init__(self):
        self.procesador = ProcesadorDatosEscolares()
        self.archivo_actual = None
        self.datos_paso1 = None  # Vista Excel
        self.datos_paso2 = None  # Datos procesados
        self.datos_paso3 = None  # Datos numéricos
        self.paso_actual = 0
        sg.theme('DefaultNoMoreNagging')
        self.window = None

    def crear_layout(self):
        """Crear layout para proceso secuencial"""
        return [
            [sg.Text("🔄 Proceso Secuencial de Extracción", font=('Helvetica', 16, 'bold'))],
            [sg.Text("Procesa un archivo paso a paso para verificar cada etapa", font=('Helvetica', 10, 'italic'))],
            [sg.HSeparator()],
            
            # Sección de carga de archivo
            [sg.Text("📁 Paso 1: Seleccionar Archivo", font=('Helvetica', 12, 'bold'))],
            [
                sg.Input(key='-ARCHIVO-', size=(50, 1), readonly=True, enable_events=True),
                sg.FileBrowse("Seleccionar", file_types=(("Excel Files", "*.xlsx"), ("All Files", "*.*")), target='-ARCHIVO-'),
                sg.Button("✅ Verificar", key='-VERIFICAR-')
            ],
            [sg.Button("🔄 Iniciar Proceso", key='-INICIAR-', disabled=True)],
            [sg.HSeparator()],
            
            # Indicador de progreso
            [sg.Text("📊 Progreso del Proceso:", font=('Helvetica', 12, 'bold'))],
            [
                sg.Text("○", key='-PASO1-', font=('Helvetica', 14)), sg.Text("Paso 1: Vista Excel"),
                sg.Text("○", key='-PASO2-', font=('Helvetica', 14)), sg.Text("Paso 2: Procesar Datos"),
                sg.Text("○", key='-PASO3-', font=('Helvetica', 14)), sg.Text("Paso 3: Extraer Números"),
            ],
            [sg.HSeparator()],
            
            # Área de visualización
            [sg.Text("👁️ Visualización del Paso Actual:", font=('Helvetica', 12, 'bold'))],
            [sg.Text("", key='-PASO_DESCRIPCION-', font=('Helvetica', 10, 'italic'))],
            [
                sg.Table(
                    values=[],
                    headings=[f"Col_{i+1}" for i in range(26)],
                    auto_size_columns=False,
                    col_widths=[12] * 26,
                    justification='left',
                    num_rows=15,
                    key='-TABLA_PASO-',
                    font='Courier 9',
                    alternating_row_color='lightblue',
                    header_font='Helvetica 9 bold',
                    enable_events=True,
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    expand_x=True,
                    expand_y=True,
                    vertical_scroll_only=False
                )
            ],
            
            # Controles de navegación
            [sg.HSeparator()],
            [
                sg.Button("⬅️ Paso Anterior", key='-ANTERIOR-', disabled=True),
                sg.Button("➡️ Siguiente Paso", key='-SIGUIENTE-', disabled=True),
                sg.Button("🔄 Reiniciar", key='-REINICIAR-', disabled=True),
                sg.Push(),
                sg.Button("Cerrar")
            ]
        ]

    def actualizar_progreso(self, paso):
        """Actualizar indicadores de progreso"""
        # Resetear todos los indicadores
        for i in range(1, 4):
            self.window[f'-PASO{i}-'].update("○")
        
        # Marcar pasos completados
        for i in range(1, paso + 1):
            self.window[f'-PASO{i}-'].update("●", text_color='green')
        
        # Marcar paso actual
        if paso <= 3:
            self.window[f'-PASO{paso}-'].update("●", text_color='blue')

    def extraer_vista_excel_pura(self, archivo):
        """PASO 1: Extraer tabla aislada tal como se ve en Excel (SIN marcadores [valor])"""
        try:
            print(f"📋 PASO 1: Extrayendo tabla aislada de Excel...")

            hoja = cargar_excel(archivo, NOMBRE_HOJAS['entrada'])
            print(f"✅ Hoja cargada: {NOMBRE_HOJAS['entrada']}")

            # Extraer rango de la tabla (A3:Z14)
            rango_inicio = (3, 1)  # A3
            rango_fin = (14, 26)   # Z14

            print(f"🔍 Aislando tabla del rango: A{rango_inicio[0]}:Z{rango_fin[0]}")

            datos_tabla = []
            for fila in range(rango_inicio[0], rango_fin[0] + 1):
                fila_datos = []
                for col in range(rango_inicio[1], rango_fin[1] + 1):
                    try:
                        celda = hoja.cell(row=fila, column=col)
                        valor = celda.value

                        # VISTA EXCEL PURA: mostrar tal como aparece en Excel
                        # Si la celda tiene valor, mostrarlo
                        # Si es parte de una celda combinada sin valor, mostrar vacío
                        if valor is not None:
                            fila_datos.append(valor)
                        else:
                            fila_datos.append("")  # Celda vacía o parte de combinada

                    except Exception as e:
                        print(f"⚠️ Error en celda {fila},{col}: {e}")
                        fila_datos.append("")

                datos_tabla.append(fila_datos)

            df_tabla = pd.DataFrame(datos_tabla)
            print(f"✅ Tabla aislada extraída: {df_tabla.shape}")
            print(f"📋 Vista previa de la tabla aislada (primeras 8 filas):")
            print(df_tabla.head(8).to_string())
            print(f"🎯 Esta tabla ahora está aislada y lista para procesar")

            return df_tabla

        except Exception as e:
            print(f"❌ Error extrayendo tabla de Excel: {str(e)}")
            raise

    def extraer_datos_con_marcadores(self, archivo):
        """PASO 2: Extraer datos con marcadores [valor] (como consulta_window)"""
        try:
            print("🔧 PASO 2: Extrayendo datos con marcadores [valor]...")

            # Usar la misma función que consulta_window
            from ..gui.consulta_window import ConsultaWindow
            consulta_temp = ConsultaWindow(None)
            datos_con_marcadores = consulta_temp.extraer_datos_crudos(archivo)

            print(f"✅ Datos con marcadores extraídos: {datos_con_marcadores.shape}")
            print(f"📋 Vista previa de datos con [valor] (primeras 8 filas):")
            print(datos_con_marcadores.head(8).to_string())
            print(f"🎯 Estos datos muestran [valor] donde había celdas combinadas")

            return datos_con_marcadores

        except Exception as e:
            print(f"❌ Error extrayendo datos con marcadores: {str(e)}")
            raise

    def _es_celda_combinada_probable(self, tabla, fila, col, valor):
        """Detectar si una celda probablemente era combinada basándose en patrones"""
        try:
            # Reglas para detectar celdas combinadas:

            # 1. Si es la primera fila (títulos principales) y hay columnas vacías después
            if fila <= 2:  # Primeras 3 filas suelen tener títulos combinados
                # Verificar si hay celdas vacías a la derecha que podrían ser parte de la combinación
                celdas_vacias_derecha = 0
                for c in range(col + 1, min(col + 6, len(tabla.columns))):  # Verificar hasta 6 columnas
                    if tabla.iloc[fila, c] == "" or pd.isna(tabla.iloc[fila, c]):
                        celdas_vacias_derecha += 1
                    else:
                        break

                # Si hay 2 o más celdas vacías a la derecha, probablemente era combinada
                if celdas_vacias_derecha >= 2:
                    return True

            # 2. Si es un concepto (columna 0) y se repite en varias columnas
            if col == 0 and isinstance(valor, str):
                # Los conceptos en la primera columna suelen estar combinados
                return True

            return False

        except:
            return False

    def extraer_solo_numeros(self, tabla_paso2):
        """PASO 3: Extraer solo valores numéricos de la tabla procesada (ignorar [valor])"""
        try:
            print("🔢 PASO 3: Extrayendo solo valores numéricos...")
            print(f"📊 Tabla recibida: {tabla_paso2.shape}")

            # Trabajar con la tabla del Paso 2
            tabla_numerica = tabla_paso2.copy()

            print("🔍 Filtrando solo valores numéricos (ignorando [valor])...")

            # Procesar cada celda
            for fila_idx in range(len(tabla_numerica)):
                for col_idx in range(len(tabla_numerica.columns)):
                    valor = tabla_numerica.iloc[fila_idx, col_idx]

                    # Si es un marcador [valor], convertir a 0 o vacío
                    if isinstance(valor, str) and valor.startswith('[') and valor.endswith(']'):
                        tabla_numerica.iloc[fila_idx, col_idx] = ""  # Ignorar celdas combinadas

                    # Si es un valor numérico, mantenerlo
                    elif isinstance(valor, (int, float)):
                        tabla_numerica.iloc[fila_idx, col_idx] = valor

                    # Si es texto que puede ser número, convertir
                    elif isinstance(valor, str) and valor.strip():
                        try:
                            numero = float(valor.replace(',', ''))  # Manejar comas en números
                            tabla_numerica.iloc[fila_idx, col_idx] = numero
                        except:
                            # Si no es número, dejar vacío para cálculos
                            tabla_numerica.iloc[fila_idx, col_idx] = ""

                    # Cualquier otra cosa, dejar vacío
                    else:
                        tabla_numerica.iloc[fila_idx, col_idx] = ""

            print(f"✅ Valores numéricos extraídos: {tabla_numerica.shape}")
            print(f"📋 Vista previa de valores numéricos (primeras 8 filas):")
            print(tabla_numerica.head(8).to_string())

            # Contar cuántos números reales hay
            numeros_encontrados = 0
            for i in range(len(tabla_numerica)):
                for j in range(len(tabla_numerica.columns)):
                    valor = tabla_numerica.iloc[i, j]
                    if isinstance(valor, (int, float)) and valor != 0:
                        numeros_encontrados += 1

            print(f"🔢 Números reales encontrados: {numeros_encontrados}")
            print(f"🎯 Estos son los valores que se usarían para sumatoria")

            return tabla_numerica

        except Exception as e:
            print(f"❌ Error extrayendo números: {str(e)}")
            raise

    def ejecutar_paso(self, numero_paso):
        """Ejecutar un paso específico del proceso"""
        try:
            print(f"🔄 Ejecutando Paso {numero_paso}...")

            if numero_paso == 1:
                # Paso 1: Extraer tabla aislada (vista Excel pura)
                print("📋 Iniciando extracción de tabla aislada...")
                self.datos_paso1 = self.extraer_vista_excel_pura(self.archivo_actual)
                self.window['-PASO_DESCRIPCION-'].update("📋 Paso 1: Tabla Aislada - Extraída tal como aparece en Excel")
                self.window['-TABLA_PASO-'].update(values=self.datos_paso1.values.tolist())
                self.paso_actual = 1
                print("✅ Paso 1 completado - Tabla aislada lista")

            elif numero_paso == 2:
                # Paso 2: Extraer datos con marcadores [valor] (como consulta_window)
                print("🔧 Iniciando extracción con marcadores [valor]...")
                self.datos_paso2 = self.extraer_datos_con_marcadores(self.archivo_actual)
                self.window['-PASO_DESCRIPCION-'].update("🔧 Paso 2: Datos con [valor] - Celdas combinadas marcadas")
                self.window['-TABLA_PASO-'].update(values=self.datos_paso2.values.tolist())
                self.paso_actual = 2
                print("✅ Paso 2 completado - Datos con marcadores [valor] extraídos")

            elif numero_paso == 3:
                # Paso 3: Extraer solo números (del Paso 2)
                if self.datos_paso2 is None:
                    raise Exception("Debes completar el Paso 2 primero")

                print("🔢 Iniciando extracción de valores numéricos...")
                self.datos_paso3 = self.extraer_solo_numeros(self.datos_paso2)
                self.window['-PASO_DESCRIPCION-'].update("🔢 Paso 3: Solo Números - Valores listos para sumatoria")
                self.window['-TABLA_PASO-'].update(values=self.datos_paso3.values.tolist())
                self.paso_actual = 3
                print("✅ Paso 3 completado - Números extraídos para cálculos")

            # Actualizar progreso y controles
            self.actualizar_progreso(self.paso_actual)
            self.window['-ANTERIOR-'].update(disabled=(self.paso_actual <= 1))
            self.window['-SIGUIENTE-'].update(disabled=(self.paso_actual >= 3))

        except Exception as e:
            error_msg = f"Error en Paso {numero_paso}: {str(e)}"
            print(f"❌ {error_msg}")
            sg.popup_error(error_msg)

    def ejecutar(self):
        """Ejecutar la ventana de proceso secuencial"""
        self.window = sg.Window(
            "Proceso Secuencial de Extracción",
            self.crear_layout(),
            resizable=True,
            finalize=True,
            size=(1200, 800)
        )
        
        while True:
            event, values = self.window.read()

            # Debug: mostrar todos los eventos
            print(f"🔍 Evento: {event}")
            if values and '-ARCHIVO-' in values:
                print(f"📁 Archivo actual: '{values['-ARCHIVO-']}'")

            if event in (sg.WINDOW_CLOSED, "Cerrar"):
                break

            elif event == '-ARCHIVO-':
                # Habilitar botón iniciar si hay archivo
                archivo = values['-ARCHIVO-'].strip()
                print(f"📁 Archivo seleccionado: '{archivo}'")
                if archivo:
                    self.archivo_actual = archivo
                    self.window['-INICIAR-'].update(disabled=False)
                    print("✅ Botón Iniciar habilitado")
                else:
                    self.window['-INICIAR-'].update(disabled=True)
                    print("❌ Botón Iniciar deshabilitado")
            
            elif event == '-INICIAR-':
                # Verificar archivo tanto de la variable como del input
                archivo = self.archivo_actual or values['-ARCHIVO-'].strip()
                print(f"🔄 Iniciando proceso con archivo: '{archivo}'")
                if archivo:
                    self.archivo_actual = archivo
                    self.ejecutar_paso(1)
                    self.window['-REINICIAR-'].update(disabled=False)
                else:
                    sg.popup_error("Por favor selecciona un archivo primero")
            
            elif event == '-SIGUIENTE-':
                if self.paso_actual < 3:
                    self.ejecutar_paso(self.paso_actual + 1)
            
            elif event == '-ANTERIOR-':
                if self.paso_actual > 1:
                    self.ejecutar_paso(self.paso_actual - 1)
            
            elif event == '-REINICIAR-':
                self.paso_actual = 0
                self.datos_paso1 = None
                self.datos_paso2 = None
                self.datos_paso3 = None
                self.actualizar_progreso(0)
                self.window['-TABLA_PASO-'].update(values=[])
                self.window['-PASO_DESCRIPCION-'].update("")
                self.window['-ANTERIOR-'].update(disabled=True)
                self.window['-SIGUIENTE-'].update(disabled=True)
        
        self.window.close()
