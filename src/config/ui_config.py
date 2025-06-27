"""
🎨 UI CONFIGURATION - Configuración Centralizada de Interfaz
===========================================================

Configuración centralizada para todos los elementos de la interfaz gráfica.
Elimina hardcodeo y permite personalización dinámica por modo.

CARACTERÍSTICAS:
✅ Headers dinámicos por contexto
✅ Labels de pasos configurables
✅ Dimensiones de tablas centralizadas
✅ Estilos y colores configurables
✅ Configuración por modo (ESCUELAS/ZONAS)
"""

from typing import Dict, List, Any
from .settings import get_config_actual


class UIConfig:
    """
    Configuración centralizada de interfaz de usuario.
    
    Proporciona configuración dinámica para todos los elementos UI
    según el modo actual y contexto de uso.
    """
    
    def __init__(self):
        """Inicializar configuración UI."""
        self.config_actual = get_config_actual()
        self.modo_actual = self.config_actual.get('MODO', 'ESCUELAS')
        
    def get_headers_config(self) -> Dict[str, List[str]]:
        """
        Obtener configuración de headers para tablas.
        
        Returns:
            dict: Configuración de headers por contexto
        """
        return {
            'excel_columns': [chr(65 + i) for i in range(26)],  # A-Z
            'numeric_columns': [chr(72 + i) for i in range(19)],  # H-Z (19 columnas)
            'grade_columns': ['1o.', '2o.', '3o.', '4o.', '5o.', '6o.'],
            'gender_columns': ['H', 'M'],
            'summary_columns': ['SUBTOTAL', 'TOTAL']
        }
    
    def get_step_labels(self) -> Dict[str, str]:
        """
        Obtener labels para pasos del proceso secuencial.
        
        Returns:
            dict: Labels de pasos configurables
        """
        if self.modo_actual == 'ESCUELAS':
            return {
                'step1': '📋 Paso 1: Vista Excel Original - Así está en el archivo Excel',
                'step2': '🔍 Paso 2: Datos Separados - Celdas combinadas marcadas con []',
                'step3': '🔢 Paso 3: Datos Numéricos - Solo números para sumatoria'
            }
        elif self.modo_actual == 'ZONAS':
            return {
                'step1': '📋 Paso 1: Vista Zona Original - Datos de zona consolidados',
                'step2': '🔍 Paso 2: Datos Procesados - Estructura normalizada',
                'step3': '🔢 Paso 3: Datos Numéricos - Totales por zona'
            }
        else:
            return {
                'step1': '📋 Paso 1: Vista Original',
                'step2': '🔍 Paso 2: Datos Procesados', 
                'step3': '🔢 Paso 3: Datos Numéricos'
            }
    
    def get_table_config(self) -> Dict[str, Any]:
        """
        Obtener configuración de tablas.
        
        Returns:
            dict: Configuración de dimensiones y comportamiento de tablas
        """
        return {
            'default_row_height': 25,
            'default_column_width': 80,
            'header_height': 30,
            'resize_columns_to_contents': True,
            'show_grid': True,
            'alternating_row_colors': True,
            'selection_behavior': 'SelectRows'
        }
    
    def get_colors_config(self) -> Dict[str, str]:
        """
        Obtener configuración de colores.
        
        Returns:
            dict: Configuración de colores para diferentes elementos
        """
        return {
            'marker_background': '#D3D3D3',  # lightGray para marcadores [valor]
            'combined_cell_text': '#008B8B',  # DarkCyan para texto combinado
            'combined_cell_number': '#FFD700',  # Gold para números combinados
            'header_background': '#F0F0F0',
            'selected_row': '#E6F3FF',
            'error_background': '#FFE6E6',
            'success_background': '#E6FFE6',
            'warning_background': '#FFF2E6'
        }
    
    def get_button_config(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtener configuración de botones.
        
        Returns:
            dict: Configuración de botones por tipo
        """
        return {
            'primary': {
                'style': '''
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                    QPushButton:pressed {
                        background-color: #3d8b40;
                    }
                    QPushButton:disabled {
                        background-color: #cccccc;
                        color: #666666;
                    }
                ''',
                'min_width': 120,
                'min_height': 35
            },
            'secondary': {
                'style': '''
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                    QPushButton:pressed {
                        background-color: #1565C0;
                    }
                    QPushButton:disabled {
                        background-color: #cccccc;
                        color: #666666;
                    }
                ''',
                'min_width': 100,
                'min_height': 35
            },
            'danger': {
                'style': '''
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #d32f2f;
                    }
                    QPushButton:pressed {
                        background-color: #b71c1c;
                    }
                ''',
                'min_width': 100,
                'min_height': 35
            }
        }
    
    def get_window_config(self) -> Dict[str, Any]:
        """
        Obtener configuración de ventanas.
        
        Returns:
            dict: Configuración de ventanas principales
        """
        return {
            'main_window': {
                'title': f'Excel Concentrado Database - {self.modo_actual}',
                'min_width': 1200,
                'min_height': 800,
                'default_width': 1400,
                'default_height': 900
            },
            'dialog': {
                'min_width': 400,
                'min_height': 300,
                'modal': True
            }
        }
    
    def get_layout_config(self) -> Dict[str, Any]:
        """
        Obtener configuración de layouts.
        
        Returns:
            dict: Configuración de espaciado y márgenes
        """
        return {
            'main_layout': {
                'margin': 10,
                'spacing': 10
            },
            'button_layout': {
                'margin': 5,
                'spacing': 8
            },
            'table_layout': {
                'margin': 0,
                'spacing': 5
            }
        }


# Instancia global para acceso fácil
ui_config = UIConfig()


def get_ui_config() -> UIConfig:
    """
    Obtener instancia de configuración UI.
    
    Returns:
        UIConfig: Instancia de configuración
    """
    return ui_config


def get_headers_for_context(context: str) -> List[str]:
    """
    Obtener headers específicos para un contexto.
    
    Args:
        context: Contexto ('excel', 'numeric', 'grade', etc.)
        
    Returns:
        list: Lista de headers para el contexto
    """
    headers_config = ui_config.get_headers_config()
    
    context_map = {
        'excel': 'excel_columns',
        'numeric': 'numeric_columns', 
        'grade': 'grade_columns',
        'gender': 'gender_columns',
        'summary': 'summary_columns'
    }
    
    key = context_map.get(context, 'excel_columns')
    return headers_config.get(key, [])


def get_step_label(step_number: int) -> str:
    """
    Obtener label para un paso específico.
    
    Args:
        step_number: Número de paso (1, 2, 3)
        
    Returns:
        str: Label del paso
    """
    step_labels = ui_config.get_step_labels()
    step_key = f'step{step_number}'
    return step_labels.get(step_key, f'Paso {step_number}')


def get_color(color_name: str) -> str:
    """
    Obtener color específico por nombre.
    
    Args:
        color_name: Nombre del color
        
    Returns:
        str: Código de color hexadecimal
    """
    colors = ui_config.get_colors_config()
    return colors.get(color_name, '#000000')
