"""
🔄 PROCESADOR SECUENCIAL DE PASOS
================================

Módulo especializado para manejar la lógica del proceso secuencial de 3 pasos:
- Paso 1: Vista Excel Original (con colores cyan/amarillo)
- Paso 2: Vista Reorganizada (con marcadores [valor])
- Paso 3: Datos Numéricos (solo números)

RESPONSABILIDADES:
✅ Navegación entre pasos (anterior/siguiente)
✅ Inicialización del proceso secuencial
✅ Coordinación con TableVisualizer para mostrar datos
✅ Gestión del estado actual del paso

SEPARACIÓN CLARA:
- Este módulo: LÓGICA de pasos
- TableVisualizer: VISUALIZACIÓN de datos
- MainWindowUI: DISEÑO de interfaz
"""

from ..config.ui_config import get_ui_config, get_step_label


class SequentialProcess:
    """
    Procesador secuencial que maneja la lógica de navegación entre los 3 pasos
    del proceso de visualización de datos Excel.
    """
    
    def __init__(self, parent_window):
        """
        Inicializar procesador secuencial.
        
        Args:
            parent_window: Referencia a la ventana principal (main.py)
                          Necesaria para acceder a:
                          - self.datos_paso1, self.datos_paso2, self.datos_paso3
                          - self.table_visualizer
                          - self.label_paso, self.btn_anterior, self.btn_siguiente
        """
        self.parent = parent_window
        self.paso_actual = 0

        # Configuración centralizada
        self.ui_config = get_ui_config()
        self.step_labels = self.ui_config.get_step_labels()

        print("🔄 SequentialProcess inicializado con configuración centralizada")
    
    # ========================================
    # MÉTODOS MOVIDOS DESDE main.py
    # ========================================

    def inicializar_proceso_secuencial(self):
        """
        MOVIDO DESDE main.py líneas 599-624
        Inicializar el proceso secuencial con los datos extraídos
        """
        print("🔄 Inicializando proceso secuencial...")

        # Verificar que todos los datos estén disponibles
        if (self.parent.datos_combinados is None or
            self.parent.datos_crudos is None or
            self.parent.datos_numericos is None):
            print("❌ Error: Datos no disponibles para proceso secuencial")
            return

        # Preparar datos para cada paso
        self.parent.datos_paso1 = self.parent.datos_combinados  # Vista Excel (combinada)
        self.parent.datos_paso2 = self.parent.datos_crudos      # Vista reorganizada (con [valor])
        self.parent.datos_paso3 = self.parent.datos_numericos   # Datos numéricos

        print(f"✅ Datos preparados:")
        print(f"   📋 Paso 1: {self.parent.datos_paso1.shape}")
        print(f"   🔧 Paso 2: {self.parent.datos_paso2.shape}")
        print(f"   🔢 Paso 3: {self.parent.datos_paso3.shape}")

        # Habilitar botones
        self.parent.btn_paso1.setEnabled(True)
        self.parent.btn_paso2.setEnabled(True)
        self.parent.btn_paso3.setEnabled(True)

        # Empezar en Paso 1
        self.mostrar_paso(1)

    def mostrar_paso(self, numero_paso):
        """
        MOVIDO DESDE main.py líneas 642-665
        Mostrar un paso específico del proceso
        """
        # Verificar que los datos estén disponibles
        if not hasattr(self.parent, 'datos_paso1') or self.parent.datos_paso1 is None:
            print("❌ Error: Datos no disponibles. Carga un archivo primero.")
            return

        self.paso_actual = numero_paso
        self.parent.paso_actual = numero_paso  # Mantener sincronizado

        # 🎨 Actualizar botones con estilo moderno
        self._actualizar_estilo_botones_pasos(numero_paso)

        # Actualizar navegación
        self.parent.btn_anterior.setEnabled(numero_paso > 1)
        self.parent.btn_siguiente.setEnabled(numero_paso < 3)

        if numero_paso == 1:
            self.mostrar_paso1()
        elif numero_paso == 2:
            self.mostrar_paso2()
        elif numero_paso == 3:
            self.mostrar_paso3()

    def mostrar_paso1(self):
        """
        MOVIDO DESDE main.py líneas 670-676
        Mostrar Paso 1: Vista Excel Original
        """
        # Usar label dinámico desde configuración
        label_paso1 = self.step_labels.get('step1', 'Paso 1: Vista Excel Original')
        self.parent.label_paso.setText(label_paso1)

        # Headers dinámicos desde configuración
        from ..config.ui_config import get_headers_for_context
        headers = get_headers_for_context('excel')
        self.parent.table_visualizer.llenar_tabla_proceso(
            self.parent.datos_paso1, headers, "Vista Excel Original", aplicar_combinacion=True
        )

    def mostrar_paso2(self):
        """
        MOVIDO DESDE main.py líneas 678-684
        Mostrar Paso 2: Vista Reorganizada
        """
        # Usar label dinámico desde configuración
        label_paso2 = self.step_labels.get('step2', 'Paso 2: Vista Reorganizada')
        self.parent.label_paso.setText(label_paso2)

        # Headers dinámicos desde configuración
        from ..config.ui_config import get_headers_for_context
        headers = get_headers_for_context('excel')
        self.parent.table_visualizer.llenar_tabla_proceso(
            self.parent.datos_paso2, headers, "Vista Reorganizada", aplicar_combinacion=False
        )

    def mostrar_paso3(self):
        """
        MOVIDO DESDE main.py líneas 686-692
        Mostrar Paso 3: Datos Numéricos
        """
        # Usar label dinámico desde configuración
        label_paso3 = self.step_labels.get('step3', 'Paso 3: Datos Numéricos')
        self.parent.label_paso.setText(label_paso3)

        # Headers dinámicos desde configuración
        from ..config.ui_config import get_headers_for_context
        headers = get_headers_for_context('numeric')
        self.parent.table_visualizer.llenar_tabla_proceso(
            self.parent.datos_paso3, headers, "Datos Numéricos", aplicar_combinacion=False
        )

    def siguiente_paso(self):
        """
        MOVIDO DESDE main.py líneas 633-637
        Ir al siguiente paso
        """
        if self.paso_actual < 3:
            self.mostrar_paso(self.paso_actual + 1)

    def anterior_paso(self):
        """
        MOVIDO DESDE main.py líneas 639-643
        Ir al paso anterior
        """
        if self.paso_actual > 1:
            self.mostrar_paso(self.paso_actual - 1)

    # ========================================
    # SEQUENTIALPROCESS COMPLETADO
    # ========================================
    
    def _validar_datos_disponibles(self):
        """
        Validar que todos los datos necesarios estén disponibles.
        """
        required_data = ['datos_paso1', 'datos_paso2', 'datos_paso3']
        for data_attr in required_data:
            if not hasattr(self.parent, data_attr) or getattr(self.parent, data_attr) is None:
                raise ValueError(f"❌ Datos no disponibles: {data_attr}")
        
        print("✅ Datos del proceso secuencial validados")
        return True

    def _actualizar_estilo_botones_pasos(self, paso_activo):
        """
        Actualizar estilo de botones de pasos con diseño moderno.

        🎨 Resaltar paso activo con estilo profesional
        """
        # Estilo base para botones inactivos
        estilo_inactivo = """
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
        """

        # Estilo para paso activo
        estilo_activo = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 10px 16px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: bold;
                font-size: 11px;
                color: white;
                min-height: 40px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #66BB6A, stop:1 #4CAF50);
            }
        """

        # Aplicar estilos según el paso activo
        botones = [
            (self.parent.btn_paso1, 1),
            (self.parent.btn_paso2, 2),
            (self.parent.btn_paso3, 3)
        ]

        for boton, numero in botones:
            if numero == paso_activo:
                boton.setStyleSheet(estilo_activo)
                print(f"🎨 Paso {numero} marcado como activo")
            else:
                boton.setStyleSheet(estilo_inactivo)

        print(f"✅ Estilos de botones actualizados para paso {paso_activo}")
