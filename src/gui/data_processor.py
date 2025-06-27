"""
🔢 PROCESADOR DE DATOS UI
========================

Módulo especializado para procesamiento de datos en la interfaz:
- Cálculo de sumatoria total
- Visualización de resultados
- Exportación a plantilla base
- Gestión de datos procesados

RESPONSABILIDADES:
✅ Cálculos de sumatoria con feedback visual
✅ Mostrar resultados en tabla de sumatoria
✅ Exportación a plantilla Excel
✅ Coordinación con DataManager para lógica

SEPARACIÓN CLARA:
- Este módulo: INTERFAZ de procesamiento
- DataManager: LÓGICA pura de cálculos
- main.py: Solo coordinación

BENEFICIO:
🔄 Reutilizable para otras interfaces
🎨 Modificar UI de resultados sin tocar lógica
📊 Procesamiento visual independiente
"""

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import Qt


class DataProcessor:
    """
    Procesador especializado de datos para la interfaz PyQt.
    
    Maneja cálculos y visualización sin lógica de negocio pura.
    """
    
    def __init__(self, parent_window):
        """
        Inicializar procesador de datos.
        
        Args:
            parent_window: Referencia a la ventana principal (main.py)
                          Necesaria para:
                          - Acceder a widgets (tabla_sumatoria, btn_calcular_suma)
                          - Usar DataManager para cálculos
                          - Actualizar interfaz
        """
        self.parent = parent_window
        print("🔢 DataProcessor inicializado")
    
    # ========================================
    # MÉTODOS MOVIDOS DESDE main.py
    # ========================================

    def calcular_sumatoria_total(self):
        """
        MOVIDO DESDE main.py líneas 116-133
        Calcular sumatoria de todos los archivos usando gestión modular
        """
        if len(self.parent.archivos_procesados) < 2:
            self._mostrar_mensaje("Advertencia", "Necesitas al menos 2 archivos para sumar", "warning")
            return

        try:
            # USAR DataManager pero mantener logs exactos
            self.parent.sumatoria_total = self.parent.data_manager.calcular_sumatoria()

            # Actualizar texto del botón
            self._actualizar_boton_calcular(f"🔄 RECALCULAR SUMATORIA ({len(self.parent.archivos_procesados)} archivos)")

            # Mostrar resultado
            self.mostrar_sumatoria_total()

            # 🎨 HABILITAR BOTÓN DE EXPORTAR cuando hay sumatoria
            self.parent.btn_exportar.setEnabled(True)
            print("✅ Botón de exportar habilitado")

        except Exception as e:
            self._mostrar_mensaje("Error", str(e), "warning")

    def mostrar_sumatoria_total(self):
        """
        MOVIDO DESDE main.py líneas 120-147
        Mostrar la sumatoria total en la tabla
        """
        from PyQt5.QtWidgets import QTableWidgetItem
        from PyQt5.QtGui import QColor

        if self.parent.sumatoria_total is None:
            return

        # 🎨 APLICAR ESTILO MODERNO A TABLA SUMATORIA
        self._configurar_estilo_sumatoria()

        # Configurar tabla
        filas, columnas = self.parent.sumatoria_total.shape
        self.parent.tabla_sumatoria.setRowCount(filas)
        self.parent.tabla_sumatoria.setColumnCount(columnas)

        # Encabezados
        headers = [chr(72 + i) for i in range(columnas)]  # H, I, J...
        self.parent.tabla_sumatoria.setHorizontalHeaderLabels(headers)

        # Llenar datos con estilo mejorado
        for i in range(filas):
            for j in range(columnas):
                valor = self.parent.sumatoria_total.iloc[i, j]
                item = QTableWidgetItem(str(valor) if valor is not None else "0")

                # 🎨 ALINEACIÓN PROFESIONAL - Centrar valores numéricos
                from PyQt5.QtCore import Qt
                item.setTextAlignment(Qt.AlignCenter)

                # 🎨 Color verde más moderno para sumatoria
                item.setBackground(QColor(200, 255, 200))  # Verde más suave
                self.parent.tabla_sumatoria.setItem(i, j, item)

        # Ajuste moderno de columnas
        self.parent.tabla_sumatoria.resizeColumnsToContents()

        # Ancho mínimo para mejor visualización
        for i in range(columnas):
            if self.parent.tabla_sumatoria.columnWidth(i) < 60:
                self.parent.tabla_sumatoria.setColumnWidth(i, 60)

        # Mostrar el grupo de sumatoria
        self.parent.grupo_sumatoria.setVisible(True)

        print("✅ Sumatoria mostrada en tabla con diseño moderno")

    def exportar_a_plantilla(self):
        """
        MOVIDO DESDE main.py líneas 122-161
        Exportar sumatoria a plantilla usando inyector modular
        """
        if self.parent.sumatoria_total is None:
            self._mostrar_mensaje("Advertencia", "No hay sumatoria calculada para exportar", "warning")
            return

        try:
            # Seleccionar archivo de destino (MANTENER DIÁLOGO EXACTO)
            archivo_destino, _ = QFileDialog.getSaveFileName(
                self.parent,
                "Guardar plantilla con datos",
                "plantilla_concentrado.xlsx",
                "Archivos Excel (*.xlsx)"
            )

            if not archivo_destino:
                return

            print("📤 Iniciando exportación a plantilla...")
            self.parent.statusBar().showMessage("🔄 Exportando a plantilla...")

            # USAR TemplateInjector con configuración dinámica
            from src.core.template_injector import TemplateInjector

            # Crear injector que detecta configuración automáticamente
            injector = TemplateInjector()

            # Obtener plantilla desde configuración dinámica
            plantilla_path = injector._obtener_plantilla_dinamica()
            print(f"📋 Plantilla dinámica: {plantilla_path}")

            # Inyectar usando configuración modular
            exito = injector.inyectar_en_plantilla(self.parent.sumatoria_total, plantilla_path, archivo_destino)

            if not exito:
                self._mostrar_mensaje("Error", "Error durante la exportación", "error")
                return

            print(f"✅ Archivo guardado: {archivo_destino}")

            self.parent.statusBar().showMessage("✅ Exportación completada")
            self._mostrar_mensaje("Éxito", f"Datos exportados exitosamente a:\n{archivo_destino}")

        except FileNotFoundError:
            self._mostrar_mensaje("Error", "No se encontró el archivo de plantilla", "error")
        except Exception as e:
            self._mostrar_mensaje("Error", f"Error al exportar:\n{str(e)}", "error")
            self.parent.statusBar().showMessage("❌ Error en exportación")

    def _configurar_estilo_sumatoria(self):
        """
        Configurar estilo moderno para la tabla de sumatoria.

        🎨 MISMO ESTILO QUE LAS TABLAS DEL PROCESO
        """
        from PyQt5.QtGui import QFont
        from PyQt5.QtWidgets import QHeaderView

        tabla = self.parent.tabla_sumatoria

        # Fuente moderna para números
        tabla.setFont(QFont("Consolas", 10))

        # Configuración moderna
        from PyQt5.QtCore import Qt
        tabla.setAlternatingRowColors(True)
        tabla.setGridStyle(Qt.SolidLine)
        tabla.setShowGrid(True)

        # Scroll suave
        tabla.setHorizontalScrollMode(tabla.ScrollPerPixel)
        tabla.setVerticalScrollMode(tabla.ScrollPerPixel)

        # Headers modernos con alineación centrada
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        tabla.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        tabla.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        tabla.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Estilo CSS moderno para sumatoria

        tabla.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: #f8fff8;
                font-family: 'Consolas', monospace;
            }
            QHeaderView::section {
                background-color: #e8f5e8;
                padding: 4px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
                color: #2e7d32;
            }
        """)

        print("🎨 Estilo moderno aplicado a tabla sumatoria")

    # ========================================
    # DATAPROCESSOR COMPLETADO
    # ========================================
    
    def _mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        """
        Mostrar mensaje al usuario.
        
        Args:
            titulo: Título del mensaje
            mensaje: Contenido del mensaje
            tipo: Tipo de mensaje ("info", "warning", "error")
        """
        if tipo == "error":
            QMessageBox.critical(self.parent, titulo, mensaje)
        elif tipo == "warning":
            QMessageBox.warning(self.parent, titulo, mensaje)
        else:
            QMessageBox.information(self.parent, titulo, mensaje)
    
    def _actualizar_boton_calcular(self, texto=None, habilitado=None):
        """
        Actualizar estado del botón de calcular.
        
        Args:
            texto: Nuevo texto del botón (opcional)
            habilitado: Estado habilitado/deshabilitado (opcional)
        """
        if texto is not None:
            self.parent.btn_calcular_suma.setText(texto)
        if habilitado is not None:
            self.parent.btn_calcular_suma.setEnabled(habilitado)
