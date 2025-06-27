"""
🎯 SELECTOR DE MODO DEL SISTEMA
==============================

Ventana inicial para seleccionar el modo de operación:
- 🏫 ESCUELAS: Validación completa + configuración específica
- 🌍 ZONAS: Sumatoria de escuelas validadas
- 🏛️ SECTORES: Sumatoria de zonas validadas

Cada modo configura automáticamente:
- Hoja de búsqueda en archivos Excel
- Rango de extracción de datos
- Conceptos a validar
- Plantilla de inyección
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class ModeSelector(QDialog):
    """
    Selector de modo de operación del sistema.
    
    Permite elegir entre ESCUELAS, ZONAS o SECTORES con
    configuración automática específica para cada nivel.
    """
    
    def __init__(self):
        super().__init__()
        self.selected_mode = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializar interfaz del selector de modo."""
        self.setWindowTitle("🎯 Selector de Modo")
        self.resize(600, 450)  # Tamaño inicial, pero redimensionable
        self.setMinimumSize(500, 400)  # Tamaño mínimo
        self.setModal(True)

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Más espacio entre elementos
        layout.setContentsMargins(30, 25, 30, 25)

        # Título principal
        title = QLabel("🎯 SELECCIONA EL MODO DE OPERACIÓN")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 8px;
                background-color: #ecf0f1;
                border-radius: 6px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title)

        # Descripción
        desc = QLabel("Selecciona el nivel jerárquico que deseas procesar:")
        desc.setAlignment(Qt.AlignCenter)
        desc.setFont(QFont("Arial", 9))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Botones de modo con espaciado
        self.create_mode_buttons(layout)

        # Espaciador flexible
        layout.addStretch()
        
        # Botón cancelar
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 9px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        cancel_layout = QHBoxLayout()
        cancel_layout.addStretch()
        cancel_layout.addWidget(cancel_btn)
        layout.addLayout(cancel_layout)
        
        self.setLayout(layout)
        
        # Centrar ventana
        self.center_window()
    
    def create_mode_buttons(self, layout):
        """Crear botones para cada modo de operación."""
        
        # 🏫 MODO ESCUELAS
        escuelas_btn = self.create_mode_button(
            "🏫 ESCUELAS",
            "Validación completa individual",
            "Hoja: ESC2 | Rango: A5:Z17 | 10 conceptos",
            "#27ae60",
            lambda: self.select_mode("ESCUELAS")
        )
        layout.addWidget(escuelas_btn)
        layout.addSpacing(10)  # Espacio entre botones

        # 🌍 MODO ZONAS
        zonas_btn = self.create_mode_button(
            "🌍 ZONAS",
            "Sumatoria de escuelas validadas",
            "Hoja: ZONA3 | Rango: A3:Z14 | 9 conceptos",
            "#3498db",
            lambda: self.select_mode("ZONAS")
        )
        layout.addWidget(zonas_btn)
        layout.addSpacing(10)  # Espacio entre botones

        # 🏛️ MODO SECTORES
        sectores_btn = self.create_mode_button(
            "🏛️ SECTORES",
            "Sumatoria de zonas validadas",
            "Hoja: SECTOR3 | Rango: A3:Z14 | 9 conceptos",
            "#9b59b6",
            lambda: self.select_mode("SECTORES")
        )
        layout.addWidget(sectores_btn)
    
    def create_mode_button(self, title, subtitle, details, color, callback):
        """Crear un botón de modo simple y compacto."""

        # Botón principal
        btn = QPushButton()
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 15px;
                text-align: left;
                min-height: 80px;
            }}
            QPushButton:hover {{
                background-color: #f8f9fa;
                border-width: 3px;
            }}
            QPushButton:pressed {{
                background-color: #e9ecef;
            }}
        """)

        # Layout interno del botón
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(15, 12, 15, 12)

        # Información del modo
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 11, QFont.Bold))
        title_label.setStyleSheet(f"color: {color};")
        info_layout.addWidget(title_label)

        # Subtítulo
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Arial", 9))
        subtitle_label.setStyleSheet("color: #7f8c8d;")
        info_layout.addWidget(subtitle_label)

        # Detalles
        details_label = QLabel(details)
        details_label.setFont(QFont("Arial", 8))
        details_label.setStyleSheet("color: #34495e;")
        info_layout.addWidget(details_label)

        btn_layout.addLayout(info_layout)
        btn_layout.addStretch()

        # Icono de selección
        select_label = QLabel("→")
        select_label.setFont(QFont("Arial", 16, QFont.Bold))
        select_label.setStyleSheet(f"color: {color};")
        select_label.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(select_label)

        btn.clicked.connect(callback)
        return btn
    
    def darken_color(self, color):
        """Oscurecer un color para efecto hover."""
        color_map = {
            "#27ae60": "#229954",
            "#3498db": "#2980b9", 
            "#9b59b6": "#8e44ad"
        }
        return color_map.get(color, color)
    
    def select_mode(self, mode):
        """Seleccionar modo y cerrar ventana."""
        self.selected_mode = mode
        print(f"🎯 Modo seleccionado: {mode}")
        self.accept()
    
    def center_window(self):
        """Centrar ventana en la pantalla."""
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    @staticmethod
    def get_selected_mode():
        """Mostrar selector y retornar modo seleccionado."""
        dialog = ModeSelector()
        if dialog.exec_() == QDialog.Accepted:
            return dialog.selected_mode
        return None


if __name__ == "__main__":
    # Prueba del selector
    app = QApplication([])
    mode = ModeSelector.get_selected_mode()
    print(f"Modo seleccionado: {mode}")
