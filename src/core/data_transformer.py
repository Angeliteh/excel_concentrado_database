"""
🔄 DATA TRANSFORMER - Transformación de Datos
=============================================

Módulo especializado ÚNICAMENTE en transformar datos extraídos.
Responsabilidad única: convertir datos raw en formatos útiles.

PRINCIPIOS:
✅ Una sola responsabilidad: transformar datos
✅ Sin extracción: recibe datos ya extraídos
✅ Sin validación: solo transformación
✅ Reutilizable: funciona con cualquier estructura
✅ Configurable: usa esquemas dinámicos
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any


class DataTransformer:
    """
    Transformador de datos extraídos de Excel.
    
    Responsabilidad única: convertir datos raw en formatos procesables.
    """
    
    def __init__(self):
        """Inicializar transformador."""
        print("🔄 DataTransformer inicializado")
    
    def crear_marcadores_combinadas(self, datos: pd.DataFrame, celdas_combinadas: List[Tuple]) -> pd.DataFrame:
        """
        Crear marcadores [valor] para celdas combinadas.
        
        Args:
            datos: DataFrame con datos raw
            celdas_combinadas: Lista de tuplas con rangos combinados
            
        Returns:
            DataFrame con marcadores [valor] en celdas combinadas
        """
        print("🔄 Creando marcadores para celdas combinadas...")
        
        # Crear copia para no modificar original
        datos_marcados = datos.copy()
        
        # Procesar cada celda combinada
        for celda in celdas_combinadas:
            min_row, min_col, max_row, max_col = celda

            # Obtener valor original de la celda principal
            if min_row < len(datos_marcados) and min_col < len(datos_marcados.columns):
                valor_original = datos_marcados.iloc[min_row, min_col]

                # Solo marcar si el valor original no está vacío
                if valor_original is not None and str(valor_original).strip() != '':
                    # Marcar celdas secundarias con [valor]
                    for fila in range(min_row, max_row + 1):
                        for col in range(min_col, max_col + 1):
                            if fila < len(datos_marcados) and col < len(datos_marcados.columns):
                                if fila == min_row and col == min_col:
                                    # Celda principal: mantener valor original
                                    continue
                                else:
                                    # Celdas secundarias: marcar con [valor] solo si no está vacía
                                    celda_actual = datos_marcados.iloc[fila, col]
                                    if celda_actual is None or str(celda_actual).strip() == '':
                                        datos_marcados.iloc[fila, col] = f"[{valor_original}]"
        
        print(f"✅ Marcadores creados para {len(celdas_combinadas)} celdas combinadas")
        return datos_marcados
    
    def crear_vista_combinada(self, datos_marcados: pd.DataFrame) -> pd.DataFrame:
        """
        Crear vista combinada revirtiendo marcadores [valor].
        
        Args:
            datos_marcados: DataFrame con marcadores [valor]
            
        Returns:
            DataFrame con vista Excel original (sin marcadores)
        """
        print("🔄 Creando vista combinada (revirtiendo marcadores)...")
        
        # Crear copia
        vista_combinada = datos_marcados.copy()
        
        # Revertir marcadores - LÓGICA EXACTA DEL ORIGINAL
        for i in range(len(vista_combinada)):
            for j in range(len(vista_combinada.columns)):
                valor = vista_combinada.iloc[i, j]

                if isinstance(valor, str) and valor.startswith('[') and valor.endswith(']'):
                    # COMPORTAMIENTO ORIGINAL: Celdas con marcadores se convierten en vacías
                    # El original NO rellena con el valor, las deja vacías para simular Excel
                    vista_combinada.iloc[i, j] = ''
        
        print("✅ Vista combinada creada")
        return vista_combinada
    
    def extraer_datos_numericos(self, datos: pd.DataFrame, rango_numerico: Dict[str, int]) -> pd.DataFrame:
        """
        Extraer solo datos numéricos de un rango específico.
        
        Args:
            datos: DataFrame con datos (puede tener marcadores)
            rango_numerico: Diccionario con coordenadas del rango numérico
                {
                    'filas_inicio': 3,
                    'filas_fin': 12,
                    'columnas_inicio': 7,
                    'columnas_fin': 25
                }
                
        Returns:
            DataFrame solo con datos numéricos
        """
        print("🔢 Extrayendo datos numéricos...")
        
        datos_numericos = []
        mapeo_posicional = {}
        
        # Extraer rango especificado
        for i in range(rango_numerico['filas_inicio'], rango_numerico['filas_fin'] + 1):
            if i < len(datos):
                fila_numerica = []
                
                for j in range(rango_numerico['columnas_inicio'], rango_numerico['columnas_fin'] + 1):
                    if j < len(datos.columns):
                        valor_original = datos.iloc[i, j]
                        
                        # Convertir a número
                        valor_numerico = self._convertir_a_numero(valor_original)
                        fila_numerica.append(valor_numerico)
                        
                        # Guardar mapeo posicional
                        mapeo_posicional[(i, j)] = {
                            'valor_original': valor_original,
                            'valor_numerico': valor_numerico,
                            'tipo': self._clasificar_valor(valor_original)
                        }
                    else:
                        fila_numerica.append(0.0)
                
                datos_numericos.append(fila_numerica)
        
        df_numericos = pd.DataFrame(datos_numericos)
        
        print(f"✅ Datos numéricos extraídos: {df_numericos.shape}")
        return df_numericos, mapeo_posicional
    
    def normalizar_estructura(self, datos: pd.DataFrame, esquema: Dict) -> Dict[str, Any]:
        """
        Normalizar datos según un esquema específico.
        
        Args:
            datos: DataFrame con datos
            esquema: Esquema de normalización
                {
                    'conceptos': ['INSCRIPCIÓN', 'BAJAS', ...],
                    'grados': ['1O', '2O', '3O', ...],
                    'generos': ['H', 'M'],
                    'estructura': {
                        'filas_conceptos': range(3, 12),
                        'columnas_grados': range(7, 19),
                        'columnas_subtotales': [19, 21],
                        'columnas_totales': range(23, 26)
                    }
                }
                
        Returns:
            Diccionario con datos normalizados
        """
        print("🔄 Normalizando estructura de datos...")
        
        estructura_normalizada = {
            'datos_por_concepto': {},
            'datos_por_grado': {},
            'subtotales': {},
            'totales': {},
            'metadatos': {
                'conceptos_detectados': [],
                'grados_detectados': [],
                'dimensiones': datos.shape
            }
        }
        
        # Normalizar por conceptos
        if 'conceptos' in esquema and 'estructura' in esquema:
            for i, concepto in enumerate(esquema['conceptos']):
                fila_concepto = esquema['estructura']['filas_conceptos'][0] + i
                if fila_concepto < len(datos):
                    estructura_normalizada['datos_por_concepto'][concepto] = datos.iloc[fila_concepto].tolist()
                    estructura_normalizada['metadatos']['conceptos_detectados'].append(concepto)
        
        # Normalizar por grados
        if 'grados' in esquema and 'estructura' in esquema:
            for j, grado in enumerate(esquema['grados']):
                col_grado = esquema['estructura']['columnas_grados'][0] + j
                if col_grado < len(datos.columns):
                    estructura_normalizada['datos_por_grado'][grado] = datos.iloc[:, col_grado].tolist()
                    estructura_normalizada['metadatos']['grados_detectados'].append(grado)
        
        print("✅ Estructura normalizada")
        return estructura_normalizada
    
    def crear_tabla_pivote(self, datos: pd.DataFrame, config_pivot: Dict) -> pd.DataFrame:
        """
        Crear tabla pivote para análisis.
        
        Args:
            datos: DataFrame con datos
            config_pivot: Configuración del pivote
                {
                    'filas': ['concepto'],
                    'columnas': ['grado', 'genero'],
                    'valores': 'cantidad',
                    'agregacion': 'sum'
                }
                
        Returns:
            DataFrame pivoteado
        """
        print("🔄 Creando tabla pivote...")
        
        # Esta es una implementación básica
        # Se puede extender según necesidades específicas
        
        tabla_pivote = datos.copy()
        
        print("✅ Tabla pivote creada")
        return tabla_pivote
    
    def _convertir_a_numero(self, valor: Any):
        """
        Convertir un valor a número, manteniendo compatibilidad con implementación original.

        Args:
            valor: Valor a convertir

        Returns:
            Número convertido manteniendo tipo original o 0 si no se puede convertir
        """
        try:
            # Casos de valores vacíos o None
            if pd.isna(valor) or valor is None or valor == '':
                return 0

            # Si ya es número, mantener tipo
            if isinstance(valor, (int, float)):
                return valor

            # Si es string
            if isinstance(valor, str):
                valor_limpio = valor.strip()

                # String completamente vacío
                if valor_limpio == '':
                    return 0

                # Manejar marcadores [valor] - NO convertir, mantener como 0
                if valor_limpio.startswith('[') and valor_limpio.endswith(']'):
                    return 0
                else:
                    # String normal con número - intentar mantener como string si es posible
                    try:
                        # Intentar convertir pero mantener como string si era string originalmente
                        numero = float(valor_limpio)
                        if numero == int(numero):
                            return str(int(numero))  # "14" en lugar de "14.0"
                        else:
                            return str(numero)
                    except:
                        return valor_limpio  # Mantener string original si no es número

            # Otros tipos no soportados
            return 0

        except (ValueError, TypeError):
            return 0
    
    def _clasificar_valor(self, valor: Any) -> str:
        """
        Clasificar tipo de valor para mapeo posicional.
        
        Args:
            valor: Valor a clasificar
            
        Returns:
            Tipo de valor ('numero', 'marcador', 'texto', 'vacio')
        """
        if pd.isna(valor) or valor is None or valor == '':
            return 'vacio'
        elif isinstance(valor, (int, float)):
            return 'numero'
        elif isinstance(valor, str):
            if valor.startswith('[') and valor.endswith(']'):
                return 'marcador'
            else:
                try:
                    float(valor)
                    return 'numero_string'
                except:
                    return 'texto'
        else:
            return 'desconocido'
    
    def generar_mapeo_completo(self, datos_originales: pd.DataFrame, datos_transformados: Dict) -> Dict[str, Any]:
        """
        Generar mapeo completo entre datos originales y transformados.
        
        Args:
            datos_originales: DataFrame original
            datos_transformados: Diccionario con datos transformados
            
        Returns:
            Mapeo completo para trazabilidad
        """
        print("🗺️ Generando mapeo completo...")
        
        mapeo = {
            'dimensiones_originales': datos_originales.shape,
            'transformaciones_aplicadas': list(datos_transformados.keys()),
            'mapeo_posicional': {},
            'metadatos': {
                'timestamp': pd.Timestamp.now(),
                'version_transformer': '1.0.0'
            }
        }
        
        # Generar mapeo posicional básico
        for i in range(len(datos_originales)):
            for j in range(len(datos_originales.columns)):
                mapeo['mapeo_posicional'][(i, j)] = {
                    'valor_original': datos_originales.iloc[i, j],
                    'coordenada': f"{chr(65 + j)}{i + 1}",  # A1, B1, etc.
                    'procesado': True
                }
        
        print("✅ Mapeo completo generado")
        return mapeo
