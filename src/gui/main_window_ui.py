"""
🏗️ CONSTRUCTOR DE INTERFAZ PRINCIPAL
===================================

Módulo especializado para construcción de la interfaz PyQt:
- Layout principal y paneles
- Creación de botones y controles
- Configuración de tablas y tabs
- Estilos y diseño visual

RESPONSABILIDADES:
✅ Construcción completa de la interfaz
✅ Configuración de layouts y paneles
✅ Creación de widgets (botones, tablas, etc.)
✅ Aplicación de estilos y diseño

SEPARACIÓN CLARA:
- Este módulo: CONSTRUCCIÓN de interfaz
- SequentialProcess: LÓGICA de navegación
- TableVisualizer: VISUALIZACIÓN de datos
- main.py: Solo coordinación

BENEFICIO PRINCIPAL:
🎨 Modificar diseño de tablas SIN tocar lógica
🎨 Cambiar tamaño de tabla Paso 2 fácilmente
🎨 Agregar opciones de diseño sin riesgo
"""

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QPushButton, 
                             QTableWidget, QLabel, QHeaderView, QListWidget, 
                             QProgressBar, QGroupBox, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class MainWindowUI:
    """
    Constructor especializado de la interfaz principal PyQt.
    
    Maneja toda la construcción visual sin lógica de negocio.
    """
    
    def __init__(self, parent_window):
        """
        Inicializar constructor de interfaz.
        
        Args:
            parent_window: Referencia a la ventana principal (main.py)
                          Necesaria para:
                          - Asignar widgets creados
                          - Conectar señales
                          - Configurar propiedades
        """
        self.parent = parent_window
        print("🏗️ MainWindowUI inicializado")

    def _crear_panel_validaciones(self, parent_layout):
        """
        Crear panel discreto para mostrar alertas de validación.

        🔍 Solo visible cuando hay discrepancias
        """
        # Grupo de validaciones (inicialmente oculto)
        self.parent.grupo_validaciones = QGroupBox("🔍 VALIDACIONES INTERNAS")
        self.parent.grupo_validaciones.setVisible(False)

        # Estilo para el panel de validaciones
        self.parent.grupo_validaciones.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #d32f2f;
                border: 2px solid #f44336;
                border-radius: 6px;
                margin-top: 5px;
                padding-top: 5px;
                background-color: #ffebee;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px 0 6px;
                background-color: white;
            }
        """)

        validaciones_layout = QVBoxLayout(self.parent.grupo_validaciones)
        validaciones_layout.setContentsMargins(6, 4, 6, 4)
        validaciones_layout.setSpacing(3)

        # Label para mostrar resumen de validaciones
        self.parent.label_validaciones = QLabel("No hay discrepancias")
        self.parent.label_validaciones.setStyleSheet("""
            QLabel {
                font-size: 9px;
                color: #d32f2f;
                padding: 2px;
                background-color: transparent;
            }
        """)
        self.parent.label_validaciones.setWordWrap(True)
        validaciones_layout.addWidget(self.parent.label_validaciones)

        # Botón para ver detalles (opcional)
        self.parent.btn_ver_validaciones = QPushButton("📋 Ver Detalles")
        self.parent.btn_ver_validaciones.setStyleSheet("""
            QPushButton {
                background-color: #ffcdd2;
                border: 1px solid #f44336;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 8px;
                font-weight: bold;
                color: #d32f2f;
                max-height: 25px;
            }
            QPushButton:hover {
                background-color: #ffb3ba;
            }
        """)
        validaciones_layout.addWidget(self.parent.btn_ver_validaciones)

        parent_layout.addWidget(self.parent.grupo_validaciones)

        print("🔍 Panel de validaciones creado (oculto)")
    
    # ========================================
    # MÉTODOS MOVIDOS DESDE main.py
    # ========================================

    def init_ui(self):
        """
        MOVIDO DESDE main.py líneas 73-92
        Inicializar la interfaz de usuario mejorada
        """
        self.parent.setWindowTitle("📊 Procesador Excel Múltiple - PyQt")
        self.parent.setGeometry(100, 100, 1600, 900)

        # Widget central
        central_widget = QWidget()
        self.parent.setCentralWidget(central_widget)

        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)

        # Panel izquierdo: Gestión de archivos
        self.create_panel_archivos(main_layout)

        # Panel derecho: Proceso secuencial
        self.create_panel_proceso(main_layout)

        # Barra de estado
        self.parent.statusBar().showMessage("Listo - Carga archivos Excel para comenzar")

    # PRÓXIMOS MÉTODOS A MOVER:
    # MICRO-PASO 6.3: create_panel_archivos() - Panel izquierdo
    # MICRO-PASO 6.4: create_panel_proceso() - Panel derecho
    # MICRO-PASO 6.5: create_file_section() - Sección archivos
    # MICRO-PASO 6.6: create_proceso_secuencial() - Proceso secuencial
    # MICRO-PASO 6.7: create_table_tab() - Creación de tabs
    
    def _aplicar_estilos_base(self):
        """
        Aplicar estilos base consistentes.
        Aquí podrás modificar fácilmente el diseño de las tablas.
        """
        # Configuraciones base que se aplicarán a todas las tablas
        base_style = {
            'font_family': 'Arial',
            'font_size': 10,
            'header_color': '#f0f0f0',
            'border_style': '1px solid #ccc'
        }
        
        print("🎨 Estilos base aplicados")
        return base_style
    
    def _configurar_tabla_proceso(self, tabla):
        """
        Configuración específica para la tabla del proceso secuencial.

        🎯 CONFIGURACIÓN MEJORADA PARA MEJOR EXPERIENCIA VISUAL
        """
        # Configuración base mejorada
        tabla.setAlternatingRowColors(True)
        tabla.setGridStyle(Qt.SolidLine)
        tabla.setShowGrid(True)

        # Configuración de scroll más suave
        tabla.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        tabla.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        # Configuración de headers más moderna con alineación centrada
        tabla.horizontalHeader().setDefaultSectionSize(80)  # Ancho por defecto más pequeño
        tabla.horizontalHeader().setMinimumSectionSize(50)   # Mínimo más pequeño
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        tabla.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)  # Centrar headers
        tabla.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        tabla.verticalHeader().setDefaultAlignment(Qt.AlignCenter)  # Centrar headers

        # Estilo moderno SOLO para headers y grid, SIN tocar items
        tabla.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: #fafafa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 4px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
            }
        """)

        print("🎨 Tabla de proceso configurada con diseño mejorado")
        return tabla

    def create_panel_archivos(self, parent_layout):
        """
        MOVIDO DESDE main.py líneas 80-139
        Crear panel izquierdo de gestión de archivos
        """
        # Contenedor del panel (optimizado para menos espacio)
        panel_archivos = QGroupBox("📁 Gestión de Archivos")
        panel_archivos.setFixedWidth(280)  # Reducido de 400 a 280 para más espacio a las tablas
        panel_layout = QVBoxLayout(panel_archivos)
        panel_layout.setContentsMargins(8, 8, 8, 8)  # Márgenes más pequeños
        panel_layout.setSpacing(6)  # Espaciado más compacto

        # Botones de carga
        botones_layout = QHBoxLayout()

        # 🎨 Botones modernos optimizados para panel más estrecho
        self.parent.btn_cargar_uno = QPushButton("📄 Archivo")
        self.parent.btn_cargar_multiples = QPushButton("📁 Múltiples")
        self.parent.btn_limpiar = QPushButton("🗑️ Limpiar")

        # 🎨 Estilo moderno y profesional para botones de carga (compatible PyQt)
        estilo_botones_carga = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 8px 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: bold;
                font-size: 9px;
                color: #495057;
                min-height: 30px;
                max-height: 35px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e3f2fd, stop:1 #bbdefb);
                border-color: #2196F3;
                color: #1565C0;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bbdefb, stop:1 #90caf9);
                border-color: #1976D2;
            }
        """

        for btn in [self.parent.btn_cargar_uno, self.parent.btn_cargar_multiples, self.parent.btn_limpiar]:
            btn.setStyleSheet(estilo_botones_carga)

        self.parent.btn_cargar_uno.clicked.connect(self.parent.file_manager.cargar_archivo_individual)
        self.parent.btn_cargar_multiples.clicked.connect(self.parent.file_manager.cargar_archivos_multiples)
        self.parent.btn_limpiar.clicked.connect(self.parent.file_manager.limpiar_archivos)

        botones_layout.addWidget(self.parent.btn_cargar_uno)
        botones_layout.addWidget(self.parent.btn_cargar_multiples)
        botones_layout.addWidget(self.parent.btn_limpiar)
        panel_layout.addLayout(botones_layout)

        # Barra de progreso
        self.parent.progress_bar = QProgressBar()
        self.parent.progress_bar.setVisible(False)
        panel_layout.addWidget(self.parent.progress_bar)

        # Lista de archivos procesados con diseño moderno
        self.parent.label_archivos_procesados = QLabel("📋 ARCHIVOS PROCESADOS")
        self.parent.label_archivos_procesados.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 12px;
                color: #2c3e50;
                padding: 5px 0px;
                border-bottom: 2px solid #3498db;
                margin-bottom: 5px;
            }
        """)
        panel_layout.addWidget(self.parent.label_archivos_procesados)

        self.parent.lista_archivos = QListWidget()
        self.parent.lista_archivos.itemClicked.connect(self.parent.file_manager.seleccionar_archivo)

        # 🎨 Estilo moderno tipo "card" para la lista
        self.parent.lista_archivos.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 5px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 8px;
                margin: 3px;
                min-height: 45px;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
                border-color: #2196F3;
                transform: translateY(-1px);
            }
            QListWidget::item:selected {
                background-color: #bbdefb;
                border-color: #1976D2;
                color: #1565C0;
                font-weight: bold;
            }
        """)

        panel_layout.addWidget(self.parent.lista_archivos)

        # 🎨 SECCIÓN DE BOTONES REORGANIZADA - Uno encima del otro para aprovechar espacio
        botones_layout = QVBoxLayout()
        botones_layout.setSpacing(10)  # Espaciado entre botones

        # Botón de calcular sumatoria (compacto)
        self.parent.btn_calcular_suma = QPushButton("🧮 CALCULAR")
        self.parent.btn_calcular_suma.setFont(QFont("Arial", 10, QFont.Bold))
        self.parent.btn_calcular_suma.setMinimumHeight(40)
        self.parent.btn_calcular_suma.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #45a049;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
                border: 2px solid #999999;
            }
        """)
        # La conexión se hará después desde UIManager cuando esté disponible
        # self.parent.btn_calcular_suma.clicked.connect(self.parent.data_processor.calcular_sumatoria_total)
        self.parent.btn_calcular_suma.setEnabled(False)

        # Botón de exportar (inicialmente deshabilitado, compacto)
        self.parent.btn_exportar = QPushButton("📤 EXPORTAR")
        self.parent.btn_exportar.setFont(QFont("Arial", 10, QFont.Bold))
        self.parent.btn_exportar.setMinimumHeight(40)
        self.parent.btn_exportar.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: 2px solid #1976D2;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
                border: 2px solid #999999;
            }
        """)
        self.parent.btn_exportar.clicked.connect(self.parent.data_processor.exportar_a_plantilla)
        self.parent.btn_exportar.setEnabled(False)  # Deshabilitado hasta tener sumatoria

        # Agregar botones al layout horizontal
        botones_layout.addWidget(self.parent.btn_calcular_suma)
        botones_layout.addWidget(self.parent.btn_exportar)

        # Agregar el layout de botones al panel
        panel_layout.addLayout(botones_layout)

        # 🔍 Panel de validaciones (inicialmente oculto)
        self._crear_panel_validaciones(panel_layout)

        # 🎨 Agregar espaciador flexible para aprovechar mejor el espacio vertical
        from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        panel_layout.addItem(spacer)

        parent_layout.addWidget(panel_archivos)

    def create_panel_proceso(self, parent_layout):
        """
        MOVIDO DESDE main.py líneas 82-164
        Crear panel derecho de proceso secuencial

        🎯 AQUÍ ESTÁ LA TABLA DEL PROCESO QUE QUIERES MODIFICAR
        """
        # Contenedor del panel
        panel_proceso = QGroupBox("🔄 Proceso Secuencial")
        panel_layout = QVBoxLayout(panel_proceso)
        panel_layout.setContentsMargins(10, 10, 10, 5)  # Reducir margen inferior
        panel_layout.setSpacing(8)  # Reducir espaciado entre elementos

        # Panel de control del proceso
        control_layout = QHBoxLayout()

        # 🎨 Botones de pasos modernos
        self.parent.btn_paso1 = QPushButton("📋 Paso 1: Vista Excel")
        self.parent.btn_paso2 = QPushButton("🔧 Paso 2: Reorganizar")
        self.parent.btn_paso3 = QPushButton("🔢 Paso 3: Extraer Números")
        self.parent.btn_siguiente = QPushButton("▶️ Siguiente")
        self.parent.btn_anterior = QPushButton("◀️ Anterior")

        # 🎨 Estilo moderno para botones de pasos (compatible PyQt)
        estilo_botones_pasos = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 2px solid #dee2e6;
                border-radius: 10px;
                padding: 10px 16px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: bold;
                font-size: 11px;
                color: #495057;
                min-height: 40px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e8f4fd, stop:1 #d1ecf1);
                border-color: #17a2b8;
                color: #0c5460;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d1ecf1, stop:1 #bee5eb);
                border-color: #138496;
            }
            QPushButton:disabled {
                background: #f8f9fa;
                border-color: #e9ecef;
                color: #6c757d;
            }
        """

        # Estilo especial para botones de navegación (compatible PyQt)
        estilo_navegacion = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fff3cd, stop:1 #ffeaa7);
                border: 2px solid #ffc107;
                border-radius: 8px;
                padding: 8px 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: bold;
                font-size: 10px;
                color: #856404;
                min-height: 35px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fff3cd, stop:1 #fdcb6e);
                border-color: #e0a800;
            }
            QPushButton:disabled {
                background: #f8f9fa;
                border-color: #e9ecef;
                color: #6c757d;
            }
        """

        # Aplicar estilos
        for btn in [self.parent.btn_paso1, self.parent.btn_paso2, self.parent.btn_paso3]:
            btn.setStyleSheet(estilo_botones_pasos)

        for btn in [self.parent.btn_siguiente, self.parent.btn_anterior]:
            btn.setStyleSheet(estilo_navegacion)

        # Configurar botones
        for btn in [self.parent.btn_paso1, self.parent.btn_paso2, self.parent.btn_paso3]:
            btn.setEnabled(False)
            btn.setFont(QFont("Arial", 10, QFont.Bold))

        # Conectar botones de navegación
        self.parent.btn_siguiente.clicked.connect(self.parent.sequential_process.siguiente_paso)
        self.parent.btn_anterior.clicked.connect(self.parent.sequential_process.anterior_paso)

        control_layout.addWidget(self.parent.btn_anterior)
        control_layout.addWidget(self.parent.btn_paso1)
        control_layout.addWidget(self.parent.btn_paso2)
        control_layout.addWidget(self.parent.btn_paso3)
        control_layout.addWidget(self.parent.btn_siguiente)
        control_layout.addStretch()

        panel_layout.addLayout(control_layout)

        # Descripción del paso actual
        self.parent.label_paso = QLabel("🔄 Selecciona un archivo de la lista para ver su proceso")
        self.parent.label_paso.setFont(QFont("Arial", 12, QFont.Bold))
        self.parent.label_paso.setStyleSheet("padding: 10px; background-color: #f0f0f0; border: 1px solid #ccc;")
        panel_layout.addWidget(self.parent.label_paso)

        # 🎯 TABLA DEL PROCESO - AQUÍ PUEDES MODIFICAR EL DISEÑO
        self.parent.tabla_proceso = QTableWidget()

        # 🎨 CONFIGURACIÓN ACTUAL DE LA TABLA (MODIFICABLE)
        self.parent.tabla_proceso.setFont(QFont("Courier", 9))
        self.parent.tabla_proceso.setAlternatingRowColors(True)
        self.parent.tabla_proceso.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.parent.tabla_proceso.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.parent.tabla_proceso.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.parent.tabla_proceso.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        # 🎯 APLICAR CONFIGURACIÓN ESPECIALIZADA
        self._configurar_tabla_proceso(self.parent.tabla_proceso)

        panel_layout.addWidget(self.parent.tabla_proceso)

        # Sección de sumatoria (debajo de la tabla principal)
        self.parent.grupo_sumatoria = QGroupBox("🔢 SUMATORIA TOTAL DE ARCHIVOS")
        self.parent.grupo_sumatoria.setVisible(False)  # Oculto hasta que se calcule

        # Estilo mejorado para el grupo de sumatoria con mejor aprovechamiento del espacio
        self.parent.grupo_sumatoria.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2e7d32;
                border: 2px solid #4caf50;
                border-radius: 8px;
                margin-top: 5px;
                padding-top: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: white;
            }
        """)

        sumatoria_layout = QVBoxLayout(self.parent.grupo_sumatoria)
        sumatoria_layout.setContentsMargins(8, 5, 8, 5)  # Reducir márgenes internos
        sumatoria_layout.setSpacing(5)  # Reducir espaciado entre elementos

        self.parent.tabla_sumatoria = QTableWidget()
        self.parent.tabla_sumatoria.setMaximumHeight(300)  # Más espacio para la tabla
        self.parent.tabla_sumatoria.setMinimumHeight(150)  # Altura mínima garantizada
        self.parent.tabla_sumatoria.setFont(QFont("Courier", 9))
        sumatoria_layout.addWidget(self.parent.tabla_sumatoria)

        # Botón de exportar movido al panel de archivos

        panel_layout.addWidget(self.parent.grupo_sumatoria)

        parent_layout.addWidget(panel_proceso)

    def create_table_tab(self, tab_widget, table_name):
        """
        MOVIDO DESDE main.py líneas 300-335
        Crear una tab con tabla
        """
        layout = QVBoxLayout(tab_widget)

        # Descripción según el tipo de tab
        if table_name == "vista_marcadores":
            desc = QLabel("🔧 Datos con [valor] para mostrar qué celdas estaban combinadas")
        elif table_name == "vista_combinada":
            desc = QLabel("📋 Vista combinada - Como se ve realmente en Excel")
        else:  # datos_numericos
            desc = QLabel("🔢 Solo datos numéricos relevantes - Listos para sumatoria")

        desc.setFont(QFont("Arial", 9))
        desc.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(desc)

        # Tabla
        table = QTableWidget()
        table.setFont(QFont("Courier", 9))
        table.setAlternatingRowColors(True)

        # Configurar tabla
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        # Guardar referencia según el tipo
        if table_name == "vista_marcadores":
            self.parent.table_marcadores = table
        elif table_name == "vista_combinada":
            self.parent.table_combinada = table
        else:  # datos_numericos
            self.parent.table_numericos = table

        layout.addWidget(table)
