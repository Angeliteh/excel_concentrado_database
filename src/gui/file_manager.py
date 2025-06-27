"""
📁 GESTOR DE ARCHIVOS UI
=======================

Módulo especializado para gestión de archivos en la interfaz:
- Carga de archivos individuales y múltiples
- Procesamiento con barra de progreso
- Gestión de lista de archivos
- Selección y limpieza de archivos

RESPONSABILIDADES:
✅ Diálogos de selección de archivos
✅ Procesamiento con feedback visual
✅ Gestión de lista de archivos procesados
✅ Coordinación con DataManager para persistencia

SEPARACIÓN CLARA:
- Este módulo: INTERFAZ de gestión de archivos
- DataManager: LÓGICA de datos y persistencia
- main.py: Solo coordinación

BENEFICIO:
🔄 Reutilizable para otras interfaces (web, CLI)
🎨 Modificar UI de archivos sin tocar lógica
"""

from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class FileManager:
    """
    Gestor especializado de archivos para la interfaz PyQt.
    
    Maneja toda la interacción de archivos sin lógica de procesamiento.
    """
    
    def __init__(self, parent_window):
        """
        Inicializar gestor de archivos.
        
        Args:
            parent_window: Referencia a la ventana principal (main.py)
                          Necesaria para:
                          - Acceder a widgets (progress_bar, lista_archivos)
                          - Llamar métodos de procesamiento
                          - Actualizar interfaz
        """
        self.parent = parent_window
        print("📁 FileManager inicializado")
    
    # ========================================
    # MÉTODOS MOVIDOS DESDE main.py
    # ========================================

    def cargar_archivo_individual(self):
        """
        MOVIDO DESDE main.py líneas 75-81
        Cargar un archivo individual
        """
        archivo = self._mostrar_dialogo_archivo(multiple=False)
        if archivo:
            self.parent.procesar_archivo(archivo)

    def cargar_archivos_multiples(self):
        """
        MOVIDO DESDE main.py líneas 79-85
        Cargar múltiples archivos
        """
        archivos = self._mostrar_dialogo_archivo(multiple=True)
        if archivos:
            self.procesar_multiples_archivos(archivos)

    def procesar_multiples_archivos(self, archivos):
        """
        MOVIDO DESDE main.py líneas 87-100
        Procesar múltiples archivos con barra de progreso
        """
        from PyQt5.QtWidgets import QApplication

        self._actualizar_progreso(0, len(archivos))

        for i, archivo in enumerate(archivos):
            self.parent.statusBar().showMessage(f"Procesando {i+1}/{len(archivos)}: {archivo.split('/')[-1]}")
            self.parent.procesar_archivo(archivo, mostrar_proceso=False)
            self._actualizar_progreso(i + 1, len(archivos))
            QApplication.processEvents()  # Actualizar interfaz

        self.parent.statusBar().showMessage(f"✅ {len(archivos)} archivos procesados")

    def agregar_archivo_a_lista_con_datos(self, nombre_archivo: str, datos_procesados: dict):
        """
        Agregar archivo a la lista con datos procesados proporcionados.

        Args:
            nombre_archivo: Nombre del archivo
            datos_procesados: Diccionario con datos procesados
        """
        try:
            datos_numericos = datos_procesados['datos_numericos']
            datos_crudos = datos_procesados['datos_crudos']

            # 🎨 Información más rica y visual
            filas_num, cols_num = datos_numericos.shape
            filas_total, cols_total = datos_crudos.shape

            # Calcular estadísticas básicas
            total_celdas = filas_num * cols_num
            celdas_con_datos = datos_numericos.count().sum()

            # Crear texto enriquecido
            resumen = f"📄 {nombre_archivo}\n"
            resumen += f"📊 Tabla: {filas_total}×{cols_total} | Datos: {filas_num}×{cols_num}\n"
            resumen += f"✅ Celdas procesadas: {celdas_con_datos}/{total_celdas}"

            item = QListWidgetItem(resumen)
            item.setData(Qt.UserRole, nombre_archivo)

            self._finalizar_item_lista(item, nombre_archivo, filas_total, cols_total, filas_num, cols_num, celdas_con_datos, total_celdas)

        except Exception as e:
            print(f"❌ Error agregando archivo con datos: {e}")
            # Fallback a método simple
            self.agregar_archivo_simple(nombre_archivo)

    def agregar_archivo_a_lista(self, nombre_archivo):
        """
        MOVIDO DESDE main.py líneas 112-119
        Agregar archivo a la lista con vista previa mejorada (método legacy)
        """
        try:
            datos_numericos = self.parent.archivos_procesados[nombre_archivo]['datos_numericos']
            datos_crudos = self.parent.archivos_procesados[nombre_archivo]['datos_crudos']

            # 🎨 Información más rica y visual
            filas_num, cols_num = datos_numericos.shape
            filas_total, cols_total = datos_crudos.shape

            # Calcular estadísticas básicas
            total_celdas = filas_num * cols_num
            celdas_con_datos = datos_numericos.count().sum()

            # Crear texto enriquecido
            resumen = f"📄 {nombre_archivo}\n"
            resumen += f"📊 Tabla: {filas_total}×{cols_total} | Datos: {filas_num}×{cols_num}\n"
            resumen += f"✅ Celdas procesadas: {celdas_con_datos}/{total_celdas}"

            item = QListWidgetItem(resumen)
            item.setData(Qt.UserRole, nombre_archivo)

            self._finalizar_item_lista(item, nombre_archivo, filas_total, cols_total, filas_num, cols_num, celdas_con_datos, total_celdas)

        except Exception as e:
            print(f"❌ Error agregando archivo (método legacy): {e}")
            # Fallback a método simple
            self.agregar_archivo_simple(nombre_archivo)

    def _finalizar_item_lista(self, item, nombre_archivo, filas_total, cols_total, filas_num, cols_num, celdas_con_datos, total_celdas):
        """Finalizar configuración del item de lista."""

        # 🎨 Agregar tooltip con información adicional
        tooltip = f"Archivo: {nombre_archivo}\n"
        tooltip += f"Dimensiones originales: {filas_total} filas × {cols_total} columnas\n"
        tooltip += f"Datos numéricos extraídos: {filas_num} filas × {cols_num} columnas\n"
        tooltip += f"Celdas con datos: {celdas_con_datos} de {total_celdas}\n"
        tooltip += f"Completitud: {(celdas_con_datos/total_celdas*100):.1f}%\n\n"
        tooltip += "💡 Haz clic para ver el proceso completo de 3 pasos"
        item.setToolTip(tooltip)

        self.parent.lista_archivos.addItem(item)

        # 🎨 Actualizar contador en el título
        self._actualizar_contador_archivos()

    def agregar_archivo_simple(self, nombre_archivo: str):
        """
        Agregar archivo a la lista de forma simple (sin estadísticas).

        Args:
            nombre_archivo: Nombre del archivo
        """
        try:
            resumen = f"📄 {nombre_archivo}\n📊 Archivo procesado\n✅ Listo para visualizar"

            item = QListWidgetItem(resumen)
            item.setData(Qt.UserRole, nombre_archivo)
            item.setToolTip(f"Archivo: {nombre_archivo}\n💡 Haz clic para ver el proceso completo")

            self.parent.lista_archivos.addItem(item)
            self._actualizar_contador_archivos()

            print(f"📁 Archivo agregado (modo simple): {nombre_archivo}")

        except Exception as e:
            print(f"❌ Error agregando archivo simple: {e}")

    def seleccionar_archivo(self, item):
        """
        MOVIDO DESDE main.py líneas 121-124
        Seleccionar archivo de la lista para ver su proceso
        """
        nombre_archivo = item.data(Qt.UserRole)

        # Usar UIManager si está disponible
        if hasattr(self.parent, 'ui_manager') and hasattr(self.parent, 'app_controller'):
            self.parent.ui_manager.seleccionar_archivo_desde_lista(nombre_archivo, self.parent.app_controller)
        else:
            # Fallback al método legacy
            self.seleccionar_archivo_por_nombre(nombre_archivo)

    def seleccionar_archivo_por_nombre(self, nombre_archivo):
        """
        MOVIDO DESDE main.py líneas 126-143
        Seleccionar archivo por nombre y mostrar su proceso
        """
        if nombre_archivo not in self.parent.archivos_procesados:
            return

        # Cargar datos del archivo seleccionado
        datos_archivo = self.parent.archivos_procesados[nombre_archivo]
        self.parent.datos_crudos = datos_archivo['datos_crudos']
        self.parent.datos_combinados = datos_archivo['datos_combinados']
        self.parent.datos_numericos = datos_archivo['datos_numericos']
        self.parent.mapeo_posicional = datos_archivo['mapeo_posicional']
        self.parent.archivo_seleccionado = nombre_archivo

        # 🎨 Actualizar indicador visual en la lista
        self._actualizar_indicador_archivo_activo(nombre_archivo)

        # Inicializar proceso secuencial
        self.parent.sequential_process.inicializar_proceso_secuencial()

        # Actualizar título con mejor formato
        self.parent.label_paso.setText(f"📁 {nombre_archivo} - Selecciona un paso para visualizar")

    def _actualizar_indicador_archivo_activo(self, nombre_archivo_activo):
        """
        Actualizar indicador visual del archivo actualmente activo.

        🎨 Agregar icono especial al archivo seleccionado
        """
        for i in range(self.parent.lista_archivos.count()):
            item = self.parent.lista_archivos.item(i)
            nombre_item = item.data(Qt.UserRole)
            texto_original = item.text()

            # Remover indicador anterior si existe
            if texto_original.startswith("🔍 "):
                texto_original = texto_original[2:]  # Remover "🔍 "

            # Agregar indicador al archivo activo
            if nombre_item == nombre_archivo_activo:
                item.setText(f"🔍 {texto_original}")
                # Hacer scroll para que sea visible
                self.parent.lista_archivos.scrollToItem(item)
            else:
                item.setText(texto_original)

    def _actualizar_contador_archivos(self):
        """
        Actualizar el contador de archivos en el título de la sección.

        🎨 Mostrar cuántos archivos están procesados
        """
        total_archivos = len(self.parent.archivos_procesados)

        # Buscar el label de archivos procesados y actualizar su texto
        # Nota: Esto requiere acceso al label, lo implementaremos de forma simple
        if hasattr(self.parent, 'label_archivos_procesados'):
            if total_archivos == 0:
                texto = "📋 ARCHIVOS PROCESADOS"
            elif total_archivos == 1:
                texto = "📋 ARCHIVOS PROCESADOS (1 archivo)"
            else:
                texto = f"📋 ARCHIVOS PROCESADOS ({total_archivos} archivos)"

            self.parent.label_archivos_procesados.setText(texto)

    def limpiar_archivos(self):
        """
        MOVIDO DESDE main.py líneas 114-132
        Limpiar todos los archivos cargados usando gestión modular
        """
        # USAR DataManager
        self.parent.data_manager.limpiar_datos()

        # Limpiar interfaz
        self.parent.lista_archivos.clear()
        self.parent.tabla_sumatoria.clear()
        self.parent.grupo_sumatoria.setVisible(False)  # Ocultar sumatoria
        self.parent.btn_calcular_suma.setEnabled(False)
        self.parent.btn_calcular_suma.setText("🧮 CALCULAR")  # Resetear texto
        self.parent.btn_exportar.setEnabled(False)  # Deshabilitar exportar
        self.parent.sumatoria_total = None

        # Limpiar proceso secuencial
        self.parent.datos_paso1 = None
        self.parent.datos_paso2 = None
        self.parent.datos_paso3 = None
        self.parent.tabla_proceso.clear()
        self.parent.label_paso.setText("🔄 Carga archivos para comenzar")

        # 🎨 Actualizar contador de archivos
        self._actualizar_contador_archivos()

    # ========================================
    # FILEMANAGER COMPLETADO
    # ========================================
    
    def _mostrar_dialogo_archivo(self, multiple=False):
        """
        Mostrar diálogo de selección de archivos.
        
        Args:
            multiple: Si True, permite selección múltiple
            
        Returns:
            str o list: Ruta(s) de archivo(s) seleccionado(s)
        """
        if multiple:
            archivos, _ = QFileDialog.getOpenFileNames(
                self.parent, 
                "Seleccionar archivos Excel", 
                "", 
                "Archivos Excel (*.xlsx *.xls)"
            )
            return archivos
        else:
            archivo, _ = QFileDialog.getOpenFileName(
                self.parent, 
                "Seleccionar archivo Excel", 
                "", 
                "Archivos Excel (*.xlsx *.xls)"
            )
            return archivo
    
    def _actualizar_progreso(self, valor, maximo=100):
        """
        Actualizar barra de progreso.
        
        Args:
            valor: Valor actual del progreso
            maximo: Valor máximo del progreso
        """
        if hasattr(self.parent, 'progress_bar'):
            self.parent.progress_bar.setMaximum(maximo)
            self.parent.progress_bar.setValue(valor)
            self.parent.progress_bar.setVisible(valor < maximo)
    
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
