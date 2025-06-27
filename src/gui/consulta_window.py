import PySimpleGUI as sg
import pandas as pd
from ..utils.db_utils import ejecutar_consulta
from ..utils.excel_utils import extraer_tabla_y_limpiar, cargar_excel
from ..procesador.procesador import ProcesadorDatosEscolares
import traceback

class ConsultaWindow:
    def __init__(self, db_path):
        print("Iniciando ConsultaWindow...")
        self.db_path = db_path
        self.window = None
        self.datos_crudos = None  # Datos tal como están en Excel
        self.datos_procesados = None  # Datos ya normalizados
        self.datos_normalizados = None  # Datos para BD
        self.procesador = ProcesadorDatosEscolares()  # Usar el mismo procesador
        sg.theme('DefaultNoMoreNagging')

    def procesar_celdas_combinadas(self, datos_crudos):
        """
        PASO 2: Procesa celdas combinadas usando los datos del PASO 1
        """
        try:
            print("🔧 Procesando celdas combinadas...")

            # Aquí usaríamos la lógica del procesador pero aplicada a los datos ya extraídos
            # Por ahora, simulamos el proceso
            datos_procesados = datos_crudos.copy()

            print(f"✅ Celdas combinadas procesadas")
            return datos_procesados

        except Exception as e:
            print(f"❌ Error procesando celdas: {str(e)}")
            return datos_crudos

    def extraer_datos_numericos(self, datos_estructurados):
        """
        PASO 3: Extrae solo las columnas numéricas para sumatoria
        Los datos estructurados ya tienen el formato correcto, solo quitamos CONCEPTO para visualización
        """
        try:
            print("🔢 Extrayendo datos numéricos...")

            # Los datos estructurados ya están listos, solo separamos para visualización
            # Mantener CONCEPTO para normalización, pero crear vista solo numérica
            columnas_numericas = [col for col in datos_estructurados.columns if col != 'CONCEPTO']
            datos_numericos_vista = datos_estructurados[columnas_numericas].copy()

            print(f"✅ Vista numérica creada: {datos_numericos_vista.shape}")
            print("📊 Columnas numéricas:", list(datos_numericos_vista.columns))

            return datos_numericos_vista

        except Exception as e:
            print(f"❌ Error extrayendo datos numéricos: {str(e)}")
            return datos_estructurados

    def crear_vista_excel_combinada(self, datos_crudos):
        """
        Crea vista Excel REAL - combina visualmente las celdas marcadas con [valor]
        """
        try:
            print("🎨 Creando vista Excel combinada (como Excel real)...")

            # Convertir DataFrame a lista
            datos_lista = datos_crudos.values.tolist()
            datos_excel_combinados = []

            for fila in datos_lista:
                fila_combinada = []
                for celda in fila:
                    if isinstance(celda, str) and celda.startswith('[') and celda.endswith(']'):
                        # Es una celda combinada, mostrar VACÍO (como Excel)
                        fila_combinada.append("")
                    else:
                        # Celda normal, mostrar valor
                        fila_combinada.append(celda if celda is not None else "")

                datos_excel_combinados.append(fila_combinada)

            print(f"✅ Vista Excel combinada creada: {len(datos_excel_combinados)} filas")
            print("🎯 Esta vista simula cómo se ve en Excel (celdas combinadas vacías)")
            return datos_excel_combinados

        except Exception as e:
            print(f"❌ Error creando vista Excel combinada: {str(e)}")
            return datos_crudos.values.tolist()

    def extraer_datos_crudos(self, archivo_excel):
        """
        Extrae datos TAL COMO ESTÁN en Excel, pero mostrando celdas combinadas de forma más clara
        """
        try:
            print(f"🔍 Extrayendo datos CRUDOS de: {archivo_excel}")

            # Cargar Excel
            hoja = cargar_excel(archivo_excel, 'ZONA3')

            # Extraer el rango COMPLETO tal como está
            rango_completo = (3, 1, 14, 26)  # A3:Z14
            tabla_cruda = []

            min_row, min_col, max_row, max_col = rango_completo

            # Obtener información de celdas combinadas
            rangos_combinados = list(hoja.merged_cells.ranges)

            # Extraer datos mostrando celdas combinadas de forma más clara
            for fila in range(min_row, max_row + 1):
                fila_datos = []
                for col in range(min_col, max_col + 1):
                    celda = hoja.cell(row=fila, column=col)
                    valor = celda.value

                    # Si es None, verificar si es parte de una celda combinada
                    if valor is None:
                        # Buscar si esta celda es parte de un rango combinado
                        for rango_combinado in rangos_combinados:
                            if (fila >= rango_combinado.min_row and fila <= rango_combinado.max_row and
                                col >= rango_combinado.min_col and col <= rango_combinado.max_col):
                                # Obtener el valor de la celda principal del rango combinado
                                valor_principal = hoja.cell(rango_combinado.min_row, rango_combinado.min_col).value
                                if valor_principal is not None:
                                    valor = f"[{valor_principal}]"  # Marcar como celda combinada
                                break

                        # Si sigue siendo None, mostrar como celda vacía
                        if valor is None:
                            valor = ""

                    fila_datos.append(valor)

                tabla_cruda.append(fila_datos)

            # Crear DataFrame con datos crudos
            df_crudo = pd.DataFrame(tabla_cruda)

            print("📋 DATOS CRUDOS (con celdas combinadas marcadas con []):")
            print(df_crudo.to_string())
            print(f"Dimensiones: {df_crudo.shape}")

            return df_crudo

        except Exception as e:
            print(f"❌ Error en extraer_datos_crudos: {str(e)}")
            print(traceback.format_exc())
            raise

    def extraer_datos_con_procesador(self, archivo_excel):
        """
        Extrae datos usando exactamente la misma lógica del procesador principal
        """
        try:
            print(f"🔍 Extrayendo datos con procesador unificado de: {archivo_excel}")

            # Usar el procesador principal para extraer datos
            datos = self.procesador.procesar_archivo_individual(archivo_excel)

            # Obtener tabla_1 (movimiento de alumnos)
            df_tabla1 = datos['tabla_1']

            print("📊 Datos extraídos (DataFrame procesado):")
            print(df_tabla1.to_string())
            print(f"Dimensiones: {df_tabla1.shape}")

            # Convertir a formato estructurado para visualización
            datos_estructurados = self.convertir_a_formato_estructurado(df_tabla1)

            return datos_estructurados

        except Exception as e:
            print(f"❌ Error en extraer_datos_con_procesador: {str(e)}")
            print(traceback.format_exc())
            raise

    def convertir_a_formato_estructurado(self, df_procesado):
        """
        Convierte el DataFrame procesado al formato estructurado para visualización
        """
        try:
            # Conceptos en el orden correcto según el procesador
            conceptos = [
                'PREINSCRIPCIÓN 1ER. GRADO', 'INSCRIPCIÓN', 'BAJAS', 'EXISTENCIA',
                'ALTAS', 'BECADOS MUNICIPIO', 'BECADOS SEED', 'BIENESTAR', 'GRUPOS'
            ]

            # Crear columnas para la tabla estructurada
            columnas = ['CONCEPTO']
            for grado in ['1o.', '2o.', '3o.', '4o.', '5o.', '6o.']:
                columnas.extend([f'{grado}_H', f'{grado}_M'])
            columnas.extend(['SUBTOTAL_H', 'SUBTOTAL_M', 'TOTAL'])

            # Convertir datos del DataFrame procesado
            datos_finales = []

            for i, concepto in enumerate(conceptos):
                if i < len(df_procesado):
                    fila_datos = [concepto]

                    # Extraer valores directamente del DataFrame procesado
                    fila_df = df_procesado.iloc[i]

                    print(f"🔍 Procesando {concepto} (fila {i}):")
                    print(f"   Datos originales: {fila_df.values.tolist()}")

                    # Agregar valores por grado (H, M) - primeros 12 valores
                    valores_extraidos = []
                    for j in range(min(12, len(fila_df))):
                        valor = float(fila_df.iloc[j]) if pd.notna(fila_df.iloc[j]) else 0.0
                        valores_extraidos.append(valor)
                        fila_datos.append(valor)

                    # Rellenar con ceros si faltan valores
                    while len(valores_extraidos) < 12:
                        valores_extraidos.append(0.0)
                        fila_datos.append(0.0)

                    # Calcular subtotales y total CORRECTAMENTE
                    # Analizar el patrón de datos para GRUPOS vs otros conceptos
                    if concepto == "GRUPOS":
                        # Para GRUPOS: en los datos crudos solo hay valores H, M está vacío
                        # Pero el procesador duplica los valores, así que tomamos solo los H
                        # Datos procesados: [7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8]
                        # Interpretación correcta: H=[7, 7, 8, 8, 8, 8], M=[0, 0, 0, 0, 0, 0]
                        valores_h = [valores_extraidos[j] for j in range(0, 12, 2)]  # Posiciones H
                        valores_m = [0.0] * 6  # GRUPOS no diferencia por género

                        # Actualizar fila_datos para mostrar correctamente
                        fila_datos = [concepto]
                        for i in range(6):  # 6 grados
                            fila_datos.append(valores_h[i])  # H
                            fila_datos.append(0.0)          # M = 0

                        subtotal_h = sum(valores_h)
                        subtotal_m = 0.0
                        total = subtotal_h  # Solo contar H

                        print(f"   🔍 {concepto} (ESPECIAL): H={valores_h} (suma={subtotal_h}), M=0 (no aplica), Total={total}")
                    else:
                        # Para otros conceptos: H y M alternados normalmente
                        valores_h = [valores_extraidos[j] for j in range(0, 12, 2)]  # Índices pares (0,2,4,6,8,10)
                        valores_m = [valores_extraidos[j] for j in range(1, 12, 2)]  # Índices impares (1,3,5,7,9,11)

                        subtotal_h = sum(valores_h)
                        subtotal_m = sum(valores_m)
                        total = subtotal_h + subtotal_m

                        print(f"   🔍 {concepto}: H={valores_h} (suma={subtotal_h}), M={valores_m} (suma={subtotal_m}), Total={total}")

                    fila_datos.extend([subtotal_h, subtotal_m, total])
                    datos_finales.append(fila_datos)
                else:
                    # Fila vacía si no hay datos
                    fila_vacia = [concepto] + [0.0] * (len(columnas) - 1)
                    datos_finales.append(fila_vacia)

            df_estructurado = pd.DataFrame(datos_finales, columns=columnas)

            print("📋 Datos convertidos a formato estructurado:")
            print(df_estructurado.to_string())

            return df_estructurado

        except Exception as e:
            print(f"❌ Error en convertir_a_formato_estructurado: {str(e)}")
            print(traceback.format_exc())
            raise

    def limpiar_y_estructurar_datos_OLD(self, df):
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
            [sg.Text("Datos Almacenados", font=('Helvetica', 12, 'bold'), expand_x=True, justification='center')],
            [sg.Button("Cargar Archivo", key='-CARGAR-', expand_x=True)],
            [sg.TabGroup([
                [sg.Tab('1. Vista Excel (Como Excel Real)', [
                    [sg.Text("📋 Cómo se ve en Excel - Celdas combinadas visualmente", font=('Helvetica', 10, 'italic'))],
                    [sg.Text("🎨 Representación fiel del Excel original", font=('Helvetica', 9))],
                    [sg.Table(
                        values=[],
                        headings=[f"Col_{i+1}" for i in range(26)],  # Encabezados como Col_1, Col_2, etc.
                        auto_size_columns=False,
                        col_widths=[18] * 26,  # Columnas más anchas
                        justification='left',
                        num_rows=15,
                        key='-TABLA_CRUDOS-',
                        font='Courier 10',  # Fuente más grande
                        alternating_row_color='lightblue',
                        header_font='Helvetica 10 bold',
                        enable_events=True,
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                        vertical_scroll_only=False,  # Permitir scroll horizontal
                        hide_vertical_scroll=False
                    )]
                ], expand_x=True, expand_y=True),
                sg.Tab('2. Datos Descombinados (Con [valor])', [
                    [sg.Text("🔧 Misma tabla pero con [valor] para mostrar celdas combinadas", font=('Helvetica', 10, 'italic'))],
                    [sg.Text("✅ Para debugging - ver qué estaba combinado", font=('Helvetica', 9))],
                    [sg.Table(
                        values=[],
                        headings=[f"Col_{i+1}" for i in range(16)],  # Encabezados genéricos como datos crudos
                        auto_size_columns=False,
                        col_widths=[18] * 16,  # Columnas consistentes
                        justification='center',
                        num_rows=15,
                        key='-TABLA_PROCESADOS-',
                        font='Courier 10',  # Fuente más grande
                        alternating_row_color='lightgreen',
                        header_font='Helvetica 10 bold',
                        enable_events=True,
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                        vertical_scroll_only=False,  # Permitir scroll horizontal
                        hide_vertical_scroll=False
                    )]
                ], expand_x=True, expand_y=True),

                sg.Tab('3. Datos Numéricos (Para Sumatoria)', [
                    [sg.Text("🔢 Solo datos numéricos listos para sumar", font=('Helvetica', 10, 'italic'))],
                    [sg.Text("➕ Estos son los valores que se consolidan en el proceso Excel", font=('Helvetica', 9))],
                    [sg.Table(
                        values=[],
                        headings=[f"Col_{i+1}" for i in range(16)],  # Encabezados genéricos
                        auto_size_columns=False,
                        col_widths=[18] * 16,
                        justification='center',
                        num_rows=15,
                        key='-TABLA_NUMERICOS-',
                        font='Courier 10',
                        alternating_row_color='lightcyan',
                        header_font='Helvetica 10 bold',
                        enable_events=True,
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                        vertical_scroll_only=False,
                        hide_vertical_scroll=False
                    )]
                ], expand_x=True, expand_y=True),

                sg.Tab('4. Datos Normalizados (Para BD)', [
                    [sg.Text("🗃️ Datos normalizados para base de datos", font=('Helvetica', 10, 'italic'))],
                    [sg.Table(
                        values=[[]],
                        headings=['GRADO', 'GENERO', 'CONCEPTO', 'VALOR', 'TIPO'],
                        auto_size_columns=False,
                        col_widths=[15, 12, 45, 15, 18],  # Columnas más anchas
                        justification='center',
                        num_rows=15,
                        key='-TABLA_NORMALIZADOS-',
                        font='Courier 10',  # Fuente más grande
                        alternating_row_color='lightyellow',
                        header_font='Helvetica 10 bold',
                        enable_events=True,
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                        vertical_scroll_only=False,  # Permitir scroll horizontal
                        hide_vertical_scroll=False
                    )]
                ], expand_x=True, expand_y=True)]
            ], key='-TABGROUP-', expand_x=True, expand_y=True)],
            [
                sg.Button("Exportar Crudos", key='-EXPORTAR_CRUDOS-'),
                sg.Button("Exportar Procesados", key='-EXPORTAR_PROCESADOS-'),
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
            finalize=True,
            size=(1400, 700)  # Aún más ancho y un poco más alto
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
                            print(f"🔄 Procesando archivo: {archivo_excel}")
                            print("="*60)

                            # PROCESO SECUENCIAL REAL
                            print("🔄 INICIANDO PROCESO SECUENCIAL...")
                            print("="*60)

                            # PASO 1: Extraer UNA VEZ del Excel
                            print("📋 PASO 1: Extrayendo datos del Excel...")
                            self.datos_crudos = self.extraer_datos_crudos(archivo_excel)
                            print(f"✅ Datos extraídos: {self.datos_crudos.shape}")

                            # PASO 2: Procesar y estructurar datos (usando procesador real)
                            print("\n🔧 PASO 2: Procesando y estructurando datos...")
                            self.datos_procesados = self.extraer_datos_con_procesador(archivo_excel)
                            print(f"✅ Datos estructurados: {self.datos_procesados.shape}")

                            # PASO 3: Crear vista numérica (solo para visualización)
                            print("\n🔢 PASO 3: Creando vista numérica...")
                            self.datos_numericos = self.extraer_datos_numericos(self.datos_procesados)
                            print(f"✅ Vista numérica creada: {self.datos_numericos.shape}")

                            # PASO 4: Normalizar para BD (usando datos estructurados completos)
                            print("\n🗃️ PASO 4: Normalizando para BD...")
                            self.datos_normalizados = self.normalizar_datos_movimiento(self.datos_procesados)
                            print(f"✅ Datos normalizados: {len(self.datos_normalizados)} registros")

                            # Actualizar las cuatro tablas secuencialmente
                            print("\n📊 ACTUALIZANDO VISUALIZACIÓN SECUENCIAL...")

                            # Tab 1: Vista Excel COMBINADA (como Excel real)
                            print("   🎨 Tab 1: Vista Excel combinada (como Excel real)...")
                            datos_excel_combinados = self.crear_vista_excel_combinada(self.datos_crudos)
                            self.window['-TABLA_CRUDOS-'].update(values=datos_excel_combinados)

                            # Tab 2: Datos DESCOMBINADOS con [valor] (para debugging)
                            print("   🔧 Tab 2: Datos descombinados con [valor] (para debugging)...")
                            datos_descombinados = self.datos_crudos.values.tolist()
                            self.window['-TABLA_PROCESADOS-'].update(values=datos_descombinados)

                            # Tab 3: Datos estructurados (CONCEPTO, 1o._H, etc.)
                            print("   🔢 Actualizando Tab 3: Datos estructurados...")
                            datos_estructurados_lista = self.datos_procesados.values.tolist()
                            self.window['-TABLA_NUMERICOS-'].update(values=datos_estructurados_lista)

                            # Tab 4: Datos normalizados (para BD)
                            print("   🗃️ Actualizando Tab 4: Datos normalizados...")
                            datos_norm_lista = self.datos_normalizados.values.tolist()
                            self.window['-TABLA_NORMALIZADOS-'].update(values=datos_norm_lista)

                            print("✅ Datos cargados y visualizados exitosamente")
                            print("="*60)
                            print("📊 RESUMEN:")
                            print(f"   🎨 Vista Excel: {self.datos_crudos.shape[0]} filas x {self.datos_crudos.shape[1]} columnas")
                            print(f"   🔧 Datos procesados: {self.datos_crudos.shape[0]} filas x {self.datos_crudos.shape[1]} columnas")
                            print(f"   🗃️ Datos normalizados: {self.datos_normalizados.shape[0]} registros")
                            print("="*60)

                            sg.popup("✅ Datos cargados exitosamente\n\n🎨 Tab 1: Vista Excel (celdas combinadas como en Excel)\n🔧 Tab 2: Datos procesados (celdas descombiandas)\n🗃️ Tab 3: Datos normalizados (para BD)\n\n💡 Compara Tab 1 vs Tab 2 para ver el proceso")
                        
                    except Exception as e:
                        print(f"Error al cargar archivo: {str(e)}")
                        print(traceback.format_exc())
                        sg.popup_error(f"Error al cargar archivo: {str(e)}")
                        
                elif event == '-EXPORTAR_CRUDOS-':
                    if self.datos_crudos is not None:
                        try:
                            filename = sg.popup_get_file(
                                'Guardar Datos Crudos como',
                                save_as=True,
                                file_types=(('Excel Files', '*.xlsx'),)
                            )
                            if filename:
                                # Exportar SIN índices del DataFrame y SIN encabezados de columnas
                                self.datos_crudos.to_excel(filename, index=False, header=False)
                                sg.popup("📋 Datos crudos guardados exitosamente")
                        except Exception as e:
                            print(f"Error al exportar datos crudos: {str(e)}")
                            sg.popup_error(f"Error al exportar: {str(e)}")
                    else:
                        sg.popup_error("No hay datos crudos para exportar. Por favor cargue un archivo primero.")

                elif event == '-EXPORTAR_PROCESADOS-':
                    if self.datos_procesados is not None:
                        try:
                            filename = sg.popup_get_file(
                                'Guardar Datos Procesados como',
                                save_as=True,
                                file_types=(('Excel Files', '*.xlsx'),)
                            )
                            if filename:
                                # Exportar SIN índices del DataFrame pero CON encabezados
                                self.datos_procesados.to_excel(filename, index=False, header=True)
                                sg.popup("🔧 Datos procesados guardados exitosamente")
                        except Exception as e:
                            print(f"Error al exportar datos procesados: {str(e)}")
                            sg.popup_error(f"Error al exportar: {str(e)}")
                    else:
                        sg.popup_error("No hay datos procesados para exportar. Por favor cargue un archivo primero.")
                        
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