"""
🗺️ DATA MAPPER - Mapeador Especializado de Datos
===============================================

Módulo especializado únicamente en mapear datos entre formatos.
Responsabilidad única: transformación y mapeo de datos.

CARACTERÍSTICAS:
✅ Solo mapeo de datos (responsabilidad única)
✅ Configuración centralizada de rangos
✅ Mapeo dinámico según esquemas
✅ Sin lógica de Excel o plantillas
✅ Extensible y testeable
"""

import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from ..config.settings import get_config_actual
from ..config.table_schemas import get_table_schema


class DataMapper:
    """
    Mapeador especializado de datos con responsabilidad única.
    
    Solo se encarga de mapear datos entre diferentes formatos,
    sin lógica de Excel o gestión de plantillas.
    """
    
    def __init__(self):
        """Inicializar mapeador de datos."""
        self.config_actual = get_config_actual()
        self.modo_actual = self.config_actual.get('MODO', 'ESCUELAS')
        print("🗺️ DataMapper inicializado")
    
    def mapear_datos_para_inyeccion(self, datos_numericos: pd.DataFrame, 
                                   rango_destino: Dict[str, int]) -> List[Tuple[int, int, Any]]:
        """
        Mapear datos numéricos a coordenadas de inyección.
        
        Args:
            datos_numericos: DataFrame con datos a mapear
            rango_destino: Configuración del rango destino
                {
                    'fila_inicio': 6,
                    'columna_inicio': 8,  # Columna H
                    'columna_fin': 26     # Columna Z
                }
                
        Returns:
            list: Lista de tuplas (fila_excel, columna_excel, valor)
        """
        print("🗺️ Mapeando datos para inyección...")
        
        datos_mapeados = []
        filas_datos, columnas_datos = datos_numericos.shape
        
        print(f"   📊 Datos origen: {filas_datos} filas x {columnas_datos} columnas")
        print(f"   🎯 Rango destino: fila {rango_destino['fila_inicio']}, "
              f"columnas {rango_destino['columna_inicio']}-{rango_destino['columna_fin']}")
        
        # Mapear cada celda de datos a coordenadas Excel
        for fila_datos in range(filas_datos):
            for col_datos in range(columnas_datos):
                # Calcular coordenadas Excel
                fila_excel = rango_destino['fila_inicio'] + fila_datos
                columna_excel = rango_destino['columna_inicio'] + col_datos
                
                # Verificar que está dentro del rango permitido
                if columna_excel <= rango_destino['columna_fin']:
                    valor = datos_numericos.iloc[fila_datos, col_datos]
                    
                    # Solo mapear valores no nulos y no cero
                    if pd.notna(valor) and valor != 0:
                        datos_mapeados.append((fila_excel, columna_excel, valor))
        
        print(f"✅ Mapeo completado: {len(datos_mapeados)} valores mapeados")
        return datos_mapeados
    
    def mapear_con_esquema_dinamico(self, datos_numericos: pd.DataFrame, 
                                   esquema_nombre: Optional[str] = None) -> List[Tuple[int, int, Any]]:
        """
        Mapear datos usando esquema dinámico según el modo actual.
        
        Args:
            datos_numericos: DataFrame con datos a mapear
            esquema_nombre: Nombre del esquema específico (opcional)
            
        Returns:
            list: Lista de tuplas (fila_excel, columna_excel, valor)
        """
        print("🗺️ Mapeando con esquema dinámico...")
        
        # Determinar esquema a usar
        if esquema_nombre is None:
            if self.modo_actual == 'ESCUELAS':
                esquema_nombre = "ESC2_MOVIMIENTOS"
            elif self.modo_actual == 'ZONAS':
                esquema_nombre = "ZONA3_MOVIMIENTOS"
            else:
                esquema_nombre = "ESC2_MOVIMIENTOS"  # Fallback
        
        try:
            # Obtener esquema
            esquema = get_table_schema(esquema_nombre)
            estructura = esquema.get('estructura', {})
            
            # Obtener configuración de inyección del esquema
            config_inyeccion = estructura.get('rango_inyeccion', {
                'fila_inicio': 6,
                'columna_inicio': 8,
                'columna_fin': 26
            })

            # Verificar si hay configuración de celdas combinadas
            celdas_combinadas = config_inyeccion.get('celdas_combinadas', {})
            if celdas_combinadas.get('X_Z_combinadas', False):
                print("🔗 Detectadas celdas combinadas X-Z, ajustando mapeo...")
                # Para celdas combinadas X-Z, solo mapear hasta columna Y (25)
                config_inyeccion['columna_fin'] = 25  # Columna Y
            
            print(f"   📋 Usando esquema: {esquema_nombre}")
            print(f"   ⚙️ Configuración: {config_inyeccion}")
            
            # Mapear usando configuración del esquema
            return self.mapear_datos_para_inyeccion(datos_numericos, config_inyeccion)
            
        except Exception as e:
            print(f"⚠️ Error con esquema dinámico: {e}")
            print("🔄 Usando configuración por defecto...")
            
            # Fallback a configuración por defecto
            config_default = {
                'fila_inicio': 6,
                'columna_inicio': 8,
                'columna_fin': 26
            }
            return self.mapear_datos_para_inyeccion(datos_numericos, config_default)
    
    def mapear_sumatoria_total(self, datos_sumatoria: pd.DataFrame) -> List[Tuple[int, int, Any]]:
        """
        Mapear datos de sumatoria total (múltiples archivos).
        
        Args:
            datos_sumatoria: DataFrame con sumatoria de múltiples archivos
            
        Returns:
            list: Lista de tuplas (fila_excel, columna_excel, valor)
        """
        print("🗺️ Mapeando sumatoria total...")
        
        # Usar esquema dinámico para sumatoria
        return self.mapear_con_esquema_dinamico(datos_sumatoria)
    
    def validar_datos_para_mapeo(self, datos: pd.DataFrame) -> Dict[str, Any]:
        """
        Validar que los datos son apropiados para mapeo.
        
        Args:
            datos: DataFrame a validar
            
        Returns:
            dict: Resultado de validación
        """
        try:
            filas, columnas = datos.shape
            
            # Validaciones básicas
            if filas == 0:
                return {
                    'valido': False,
                    'mensaje': 'DataFrame vacío (0 filas)',
                    'detalles': {'filas': filas, 'columnas': columnas}
                }
            
            if columnas == 0:
                return {
                    'valido': False,
                    'mensaje': 'DataFrame sin columnas',
                    'detalles': {'filas': filas, 'columnas': columnas}
                }
            
            # Contar valores no nulos
            valores_no_nulos = datos.count().sum()
            total_celdas = filas * columnas
            porcentaje_datos = (valores_no_nulos / total_celdas) * 100
            
            # Validar dimensiones esperadas
            dimensiones_validas = True
            mensaje_dimensiones = ""
            
            if self.modo_actual == 'ESCUELAS':
                if columnas != 19:  # H-Z = 19 columnas
                    dimensiones_validas = False
                    mensaje_dimensiones = f"Se esperaban 19 columnas para ESCUELAS, encontradas {columnas}"
            
            return {
                'valido': dimensiones_validas,
                'mensaje': mensaje_dimensiones if not dimensiones_validas else 'Datos válidos para mapeo',
                'detalles': {
                    'filas': filas,
                    'columnas': columnas,
                    'valores_no_nulos': valores_no_nulos,
                    'porcentaje_datos': round(porcentaje_datos, 2),
                    'modo': self.modo_actual
                }
            }
            
        except Exception as e:
            return {
                'valido': False,
                'mensaje': f'Error validando datos: {str(e)}',
                'error': type(e).__name__
            }
    
    def obtener_estadisticas_mapeo(self, datos_mapeados: List[Tuple[int, int, Any]]) -> Dict[str, Any]:
        """
        Obtener estadísticas de datos mapeados.
        
        Args:
            datos_mapeados: Lista de tuplas (fila, columna, valor)
            
        Returns:
            dict: Estadísticas del mapeo
        """
        if not datos_mapeados:
            return {
                'total_valores': 0,
                'mensaje': 'No hay datos mapeados'
            }
        
        # Extraer valores para análisis
        valores = [valor for _, _, valor in datos_mapeados]
        filas = [fila for fila, _, _ in datos_mapeados]
        columnas = [col for _, col, _ in datos_mapeados]
        
        estadisticas = {
            'total_valores': len(datos_mapeados),
            'rango_filas': {
                'min': min(filas),
                'max': max(filas)
            },
            'rango_columnas': {
                'min': min(columnas),
                'max': max(columnas)
            },
            'valores': {
                'suma_total': sum(valores),
                'valor_min': min(valores),
                'valor_max': max(valores),
                'promedio': sum(valores) / len(valores)
            }
        }
        
        return estadisticas
    
    def convertir_coordenadas_excel(self, fila_pandas: int, columna_pandas: int, 
                                   offset_fila: int = 0, offset_columna: int = 0) -> Tuple[int, int]:
        """
        Convertir coordenadas de pandas (0-based) a Excel (1-based).
        
        Args:
            fila_pandas: Fila en formato pandas (0-based)
            columna_pandas: Columna en formato pandas (0-based)
            offset_fila: Offset adicional para filas
            offset_columna: Offset adicional para columnas
            
        Returns:
            tuple: (fila_excel, columna_excel) en formato 1-based
        """
        fila_excel = fila_pandas + 1 + offset_fila
        columna_excel = columna_pandas + 1 + offset_columna
        
        return (fila_excel, columna_excel)
    
    def obtener_letra_columna(self, numero_columna: int) -> str:
        """
        Convertir número de columna a letra de Excel.
        
        Args:
            numero_columna: Número de columna (1-based)
            
        Returns:
            str: Letra de columna (A, B, C, ..., Z, AA, AB, ...)
        """
        resultado = ""
        while numero_columna > 0:
            numero_columna -= 1
            resultado = chr(65 + (numero_columna % 26)) + resultado
            numero_columna //= 26
        
        return resultado
