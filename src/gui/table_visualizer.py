"""
🎨 VISUALIZADOR DE TABLAS PYQT
=============================

Módulo especializado para visualización de tablas con funcionalidad crítica:
- Colores cyan/amarillo para celdas combinadas
- Sombreado gris para marcadores [valor]
- Combinación de celdas (setSpan)

FUNCIONALIDAD CRÍTICA - NO MODIFICAR SIN VALIDAR:
✅ Detección de tipos pandas (int64, float64)
✅ Colores: Qt.yellow (números), Qt.cyan (texto), Qt.lightGray (marcadores)
✅ Algoritmo de combinación de celdas
"""

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont  # Para configuración de fuentes
import numpy as np  # CRÍTICO: Para tipos pandas (int64, float64)
from ..config.ui_config import get_ui_config, get_headers_for_context, get_color


class TableVisualizer:
    """
    Visualizador especializado de tablas PyQt con funcionalidad crítica preservada.
    
    Responsabilidades:
    - Llenar tablas del proceso secuencial
    - Aplicar combinación de celdas
    - Aplicar colores críticos (cyan/amarillo/gris)
    - Manejar tipos de pandas correctamente
    """
    
    def __init__(self, parent_window):
        """
        Inicializar visualizador de tablas con configuración centralizada.

        Args:
            parent_window: Referencia a la ventana principal (main.py)
                          Necesaria para acceder a:
                          - self.tabla_proceso
                          - self.datos_crudos
                          - self.table_marcadores, etc.
        """
        self.parent = parent_window

        # Configuración centralizada
        self.ui_config = get_ui_config()
        self.colors_config = self.ui_config.get_colors_config()
        self.table_config = self.ui_config.get_table_config()

        print("🎨 TableVisualizer inicializado con configuración centralizada")
    
    # ========================================
    # MÉTODOS MOVIDOS DESDE main.py
    # ========================================

    def llenar_tabla_proceso(self, dataframe, headers, nombre, aplicar_combinacion=False):
        """
        MOVIDO DESDE main.py líneas 675-710
        Llenar la tabla del proceso secuencial con configuración optimizada por paso
        """
        print(f"   📋 Mostrando {nombre}...")

        # Validar que dataframe no sea None
        if dataframe is None:
            print(f"❌ Error: dataframe es None para {nombre}")
            return

        # Configurar dimensiones
        filas, columnas = dataframe.shape
        self.parent.tabla_proceso.setRowCount(filas)
        self.parent.tabla_proceso.setColumnCount(columnas)

        # Configurar encabezados
        self.parent.tabla_proceso.setHorizontalHeaderLabels(headers[:columnas])

        # Limpiar combinaciones anteriores
        self.parent.tabla_proceso.clearSpans()

        # 🎨 CONFIGURACIÓN ESPECÍFICA POR PASO
        self._configurar_por_paso(nombre)

        # Llenar datos con optimización para Paso 2
        for i in range(filas):
            for j in range(columnas):
                valor = dataframe.iloc[i, j]

                # 🔧 OPTIMIZACIÓN PARA PASO 2: Truncar valores repetidos
                texto_mostrar = self._optimizar_texto_celda(valor, nombre)
                item = QTableWidgetItem(texto_mostrar)

                # 🎨 ALINEACIÓN PROFESIONAL - Centrar todos los valores
                item.setTextAlignment(Qt.AlignCenter)

                # 🎨 COLORES CRÍTICOS: Aplicar con máxima prioridad
                if isinstance(valor, str) and valor.startswith('[') and valor.endswith(']'):
                    # CRÍTICO: Sombreado gris para marcadores [valor] usando configuración centralizada
                    from PyQt5.QtGui import QColor
                    color_hex = self.colors_config['marker_background']
                    item.setBackground(QColor(color_hex))
                    # FORZAR con stylesheet individual para máxima prioridad
                    item.setData(Qt.UserRole + 1, "gray_marker")  # Marcar para identificar
                    # Tooltip con valor completo para celdas truncadas
                    if len(str(valor)) > 15:
                        item.setToolTip(str(valor))

                self.parent.tabla_proceso.setItem(i, j, item)

        # Aplicar combinación si es necesario
        if aplicar_combinacion:
            self.aplicar_combinacion_celdas_proceso(dataframe)

        # Ajustar columnas según el paso
        self._ajustar_columnas_por_paso(nombre)

        # 🎨 APLICAR COLORES CRÍTICOS AL FINAL (máxima prioridad)
        self._aplicar_colores_criticos_finales()

        print(f"   ✅ {nombre} mostrado: {filas}x{columnas}")

    def aplicar_combinacion_celdas_proceso(self, dataframe):
        """
        MOVIDO DESDE main.py líneas 684-729 - MÉTODO CRÍTICO
        Aplicar combinación de celdas en la tabla del proceso

        ⚠️ FUNCIONALIDAD CRÍTICA:
        - Colores cyan/amarillo para celdas combinadas
        - Detección correcta de tipos pandas
        - Algoritmo de combinación de celdas
        """
        print("   🔗 Aplicando combinación de celdas en proceso...")

        # Usar datos originales (con marcadores) para saber qué combinar
        datos_originales = self.parent.datos_crudos

        for i in range(len(datos_originales)):
            j = 0
            while j < len(datos_originales.columns):
                valor_original = datos_originales.iloc[i, j]

                # CRÍTICO: Detección correcta de tipos pandas
                es_numero = (isinstance(valor_original, (int, float)) or
                           isinstance(valor_original, (np.integer, np.floating)))

                # Si encontramos un valor sin [valor], buscar cuántas celdas [valor] le siguen
                if ((isinstance(valor_original, str) and
                     not valor_original.startswith('[') and
                     valor_original != "") or
                    (es_numero and valor_original != 0)):

                    # Contar cuántas celdas consecutivas tienen [valor_original]
                    span_count = 1
                    valor_a_buscar = f"[{valor_original}]"

                    for k in range(j + 1, len(datos_originales.columns)):
                        siguiente_valor = datos_originales.iloc[i, k]
                        if (isinstance(siguiente_valor, str) and
                            siguiente_valor == valor_a_buscar):
                            span_count += 1
                        else:
                            break

                    # Si hay más de 1 celda, combinar
                    if span_count > 1:
                        self.parent.tabla_proceso.setSpan(i, j, 1, span_count)

                        # 🎨 CRÍTICO: Color especial para celdas combinadas
                        item = self.parent.tabla_proceso.item(i, j)
                        if item:
                            from PyQt5.QtGui import QColor
                            if es_numero:
                                # AMARILLO más explícito para números
                                item.setBackground(QColor(255, 255, 0))  # Amarillo puro
                            else:
                                # CYAN más explícito para texto
                                item.setBackground(QColor(0, 255, 255))  # Cyan puro

                    j += span_count
                else:
                    j += 1

    def llenar_tabla(self, table, dataframe, headers=None, nombre="Tabla"):
        """
        MOVIDO DESDE main.py líneas 686-717
        Llenar una tabla con datos (para tabs de datos) usando configuración centralizada.

        ⚠️ FUNCIONALIDAD CRÍTICA:
        - Sombreado gris para marcadores [valor]
        - Llamada a aplicar_combinacion_celdas para vista combinada
        - Headers dinámicos según contexto
        """
        print(f"   📋 Llenando {nombre}...")

        # Configurar dimensiones
        filas, columnas = dataframe.shape
        table.setRowCount(filas)
        table.setColumnCount(columnas)

        # Configurar encabezados dinámicos
        if headers is None:
            # Determinar contexto automáticamente
            if columnas == 19:
                headers = get_headers_for_context('numeric')  # H-Z para datos numéricos
            else:
                headers = get_headers_for_context('excel')    # A-Z para datos completos

        table.setHorizontalHeaderLabels(headers[:columnas])

        # Llenar datos
        for i in range(filas):
            for j in range(columnas):
                valor = dataframe.iloc[i, j]
                item = QTableWidgetItem(str(valor) if valor is not None else "")

                # CRÍTICO: Estilo para celdas combinadas (solo en vista con marcadores)
                if isinstance(valor, str) and valor.startswith('[') and valor.endswith(']'):
                    from PyQt5.QtGui import QColor
                    color_hex = self.colors_config['marker_background']
                    item.setBackground(QColor(color_hex))

                table.setItem(i, j, item)

        # Si es la vista combinada, aplicar combinación real de celdas
        if "Combinada" in nombre:
            # MICRO-PASO 4.2: Usar método local en lugar del de main.py
            self.aplicar_combinacion_celdas(table, dataframe)

        # Ajustar columnas
        table.resizeColumnsToContents()

        print(f"   ✅ {nombre} llenada: {filas}x{columnas}")

    def aplicar_combinacion_celdas(self, table, dataframe):
        """
        MOVIDO DESDE main.py líneas 722-770 - MÉTODO CRÍTICO
        Aplicar combinación real de celdas en PyQt (para tabs)

        ⚠️ FUNCIONALIDAD CRÍTICA:
        - Colores cyan/amarillo para celdas combinadas
        - Detección correcta de tipos pandas
        - Algoritmo de combinación de celdas
        - Debug detallado de combinaciones
        """
        print("   🔗 Aplicando combinación de celdas...")

        # Analizar datos originales (con marcadores) para saber qué combinar
        datos_originales = self.parent.datos_crudos

        for i in range(len(datos_originales)):
            j = 0
            while j < len(datos_originales.columns):
                valor_original = datos_originales.iloc[i, j]

                # CRÍTICO: Detección correcta de tipos pandas
                es_numero = (isinstance(valor_original, (int, float)) or
                           isinstance(valor_original, (np.integer, np.floating)))

                # Si encontramos un valor sin [valor] (texto o número), buscar cuántas celdas [valor] le siguen
                if ((isinstance(valor_original, str) and
                     not valor_original.startswith('[') and
                     valor_original != "") or
                    (es_numero and valor_original != 0)):

                    # Contar cuántas celdas consecutivas tienen [valor_original]
                    span_count = 1
                    valor_a_buscar = f"[{valor_original}]"

                    for k in range(j + 1, len(datos_originales.columns)):
                        siguiente_valor = datos_originales.iloc[i, k]
                        if (isinstance(siguiente_valor, str) and
                            siguiente_valor == valor_a_buscar):
                            span_count += 1
                        else:
                            break

                    # Si hay más de 1 celda, combinar
                    if span_count > 1:
                        tipo_valor = "NÚMERO" if es_numero else "TEXTO"
                        print(f"     🔗 Combinando {tipo_valor} fila {i}, columnas {j}-{j+span_count-1}: '{valor_original}' (span={span_count})")
                        table.setSpan(i, j, 1, span_count)

                        # 🎨 CRÍTICO: Actualizar el contenido de la celda combinada
                        item = table.item(i, j)
                        if item:
                            from PyQt5.QtGui import QColor
                            # Color diferente para números vs texto
                            if es_numero:
                                # AMARILLO más explícito para números combinados
                                item.setBackground(QColor(255, 255, 0))  # Amarillo puro
                            else:
                                # CYAN más explícito para texto combinado
                                item.setBackground(QColor(0, 255, 255))  # Cyan puro

                    j += span_count
                else:
                    j += 1

        print("   ✅ Combinación de celdas aplicada")

        # 🎨 APLICAR COLORES DESPUÉS DE COMBINACIÓN
        self._aplicar_colores_criticos_finales()
    
    def _validar_funcionalidad_critica(self):
        """
        Método de validación para asegurar que la funcionalidad crítica funciona.
        Se ejecutará después de cada método movido.
        """
        print("🔍 Validando funcionalidad crítica...")
        
        # Verificar que parent tiene las propiedades necesarias
        required_attrs = ['tabla_proceso', 'datos_crudos']
        for attr in required_attrs:
            if not hasattr(self.parent, attr):
                raise AttributeError(f"❌ Parent no tiene atributo crítico: {attr}")
        
        print("✅ Funcionalidad crítica validada")
        return True

    def _configurar_por_paso(self, nombre_paso):
        """
        Configuración específica según el paso del proceso.

        🎯 OPTIMIZACIÓN ESPECIAL PARA PASO 2
        """
        if "Reorganizada" in nombre_paso:  # Paso 2
            # Configuración para Paso 2: más compacto
            self.parent.tabla_proceso.setFont(QFont("Segoe UI", 8))
            print("🎨 Configuración compacta aplicada para Paso 2")
        elif "Excel Original" in nombre_paso:  # Paso 1
            # Configuración para Paso 1: más legible
            self.parent.tabla_proceso.setFont(QFont("Segoe UI", 10))
            print("🎨 Configuración legible aplicada para Paso 1")
        else:  # Paso 3
            # Configuración para Paso 3: enfoque en números
            self.parent.tabla_proceso.setFont(QFont("Consolas", 9))
            print("🎨 Configuración numérica aplicada para Paso 3")

    def _optimizar_texto_celda(self, valor, nombre_paso):
        """
        Optimizar texto de celda según el paso.

        🔧 ESPECIAL PARA PASO 2: Truncar valores repetidos [valor]
        """
        if "Reorganizada" in nombre_paso and isinstance(valor, str):
            if valor.startswith('[') and valor.endswith(']'):
                # Truncar valores largos en Paso 2
                if len(valor) > 15:
                    return valor[:12] + "...]"
                return valor
            return str(valor)

        # Para otros pasos, mostrar valor completo
        return str(valor) if valor is not None else ""

    def _ajustar_columnas_por_paso(self, nombre_paso):
        """
        Ajustar anchos de columnas según el paso.

        🎯 PASO 2: Anchos más pequeños para mejor visualización
        """
        if "Reorganizada" in nombre_paso:  # Paso 2
            # Anchos más pequeños para Paso 2
            for i in range(self.parent.tabla_proceso.columnCount()):
                self.parent.tabla_proceso.setColumnWidth(i, 60)
            print("🎨 Anchos compactos aplicados para Paso 2")
        elif "Excel Original" in nombre_paso:  # Paso 1
            # Ajuste automático para Paso 1
            self.parent.tabla_proceso.resizeColumnsToContents()
            print("🎨 Ajuste automático aplicado para Paso 1")
        else:  # Paso 3
            # Anchos optimizados para números
            self.parent.tabla_proceso.resizeColumnsToContents()
            # Ancho mínimo para números
            for i in range(self.parent.tabla_proceso.columnCount()):
                if self.parent.tabla_proceso.columnWidth(i) < 50:
                    self.parent.tabla_proceso.setColumnWidth(i, 50)
            print("🎨 Anchos numéricos aplicados para Paso 3")

    def _aplicar_colores_criticos_finales(self):
        """
        Aplicar colores críticos al final con máxima prioridad.

        🎯 SOLUCIÓN DEFINITIVA para preservar colores cyan/amarillo/gris
        """
        from PyQt5.QtGui import QColor

        tabla = self.parent.tabla_proceso

        # Recorrer todas las celdas y aplicar colores según marcadores
        for i in range(tabla.rowCount()):
            for j in range(tabla.columnCount()):
                item = tabla.item(i, j)
                if item:
                    texto = item.text()

                    # 🔍 PASO 2: Sombreado gris para marcadores [valor]
                    if isinstance(texto, str) and texto.startswith('[') and texto.endswith(']'):
                        color_hex = self.colors_config['marker_background']
                        item.setBackground(QColor(color_hex))  # Gris para [valor]
                        print(f"🎨 Gris aplicado en ({i},{j}): {texto[:20]}...")

                    # 🔍 PASO 1: Verificar si la celda está combinada (span > 1)
                    span_row = tabla.rowSpan(i, j)
                    span_col = tabla.columnSpan(i, j)

                    if span_row > 1 or span_col > 1:
                        # Es una celda combinada, aplicar cyan o amarillo
                        try:
                            # Verificar si es número
                            float(texto.replace(',', ''))
                            item.setBackground(QColor(255, 255, 0))  # Amarillo para números
                            print(f"🎨 Amarillo aplicado en ({i},{j}): {texto}")
                        except (ValueError, AttributeError):
                            item.setBackground(QColor(0, 255, 255))  # Cyan para texto
                            print(f"🎨 Cyan aplicado en ({i},{j}): {texto}")

        print("✅ Colores críticos aplicados al final")
