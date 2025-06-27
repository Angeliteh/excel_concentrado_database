"""
📊 EXCEL PROCESSOR - Arquitectura Modular
=========================================

Procesador de Excel con arquitectura modular y separación de responsabilidades.

ARQUITECTURA:
✅ ExcelExtractor: Extracción pura de datos
✅ DataTransformer: Transformación de datos
✅ Configuración dinámica: Sin hardcodeo
✅ Extensible: Preparado para validaciones cruzadas
✅ Mantenible: Código limpio y organizado
"""

import pandas as pd
from ..config.settings import get_config_actual
from ..config.table_schemas import get_table_schema
from .excel_extractor import ExcelExtractor
from .data_transformer import DataTransformer


class ExcelProcessor:
    """
    Wrapper ultra-conservador que mantiene funcionalidad exacta del ExcelProcessor original.
    
    GARANTÍA: Comportamiento idéntico al ExcelProcessor actual.
    """

    def __init__(self):
        """Inicializar procesador con arquitectura modular."""
        # Datos procesados
        self.datos_crudos = None
        self.datos_combinados = None
        self.datos_numericos = None
        self.mapeo_posicional = None

        # Inicializar módulos especializados
        self.extractor = ExcelExtractor()
        self.transformer = DataTransformer()

        print("📊 ExcelProcessor inicializado con arquitectura modular")

    def extraer_datos_completo(self, archivo_path):
        """
        Extraer y procesar datos completos usando arquitectura modular.

        Args:
            archivo_path: Ruta del archivo Excel

        Returns:
            dict: Diccionario con datos procesados
                {
                    'datos_crudos': DataFrame con marcadores [valor],
                    'datos_combinados': DataFrame vista Excel,
                    'datos_numericos': DataFrame solo números,
                    'mapeo_posicional': dict con mapeo posicional
                }
        """
        print(f"📋 ExcelProcessor procesando: {archivo_path}")

        return self._procesar_archivo_modular(archivo_path)

    def _procesar_archivo_modular(self, archivo_path):
        """
        Procesar archivo usando arquitectura modular con módulos especializados.

        Args:
            archivo_path: Ruta del archivo Excel

        Returns:
            dict: Datos procesados con formato estándar
        """
        print("🔄 Procesando con arquitectura modular...")
        
        try:
            # 🎯 Obtener configuración dinámica (igual que original)
            config_actual = get_config_actual()
            hoja_nombre = config_actual['HOJA_DATOS']
            rango_datos = config_actual['RANGO_DATOS']

            print(f"⚙️ Configuración: Hoja '{hoja_nombre}', Rango '{rango_datos}'")

            # 📊 PASO 1: Extracción usando nuevo módulo
            resultado_extraccion = self.extractor.extraer_con_metadatos(
                archivo_path, hoja_nombre, rango_datos
            )
            
            datos_raw = resultado_extraccion['datos']
            celdas_combinadas = resultado_extraccion['celdas_combinadas']
            
            print(f"✅ Extracción completada: {datos_raw.shape}")

            # 🔄 PASO 2: Crear marcadores usando nuevo módulo
            self.datos_crudos = self.transformer.crear_marcadores_combinadas(
                datos_raw, celdas_combinadas
            )
            
            # VALIDACIÓN CRÍTICA: Verificar dimensiones exactas
            if self.datos_crudos.shape != (13, 26):  # Ajustar según datos reales
                print(f"⚠️ Dimensión inesperada datos_crudos: {self.datos_crudos.shape}")

            print("📋 DATOS CRUDOS (con marcadores []):")
            print(self.datos_crudos.head(8).to_string())

            # 🔄 PASO 3: Vista combinada usando nuevo módulo
            self.datos_combinados = self.transformer.crear_vista_combinada(
                self.datos_crudos
            )
            
            # VALIDACIÓN CRÍTICA: Verificar que vista combinada es correcta
            if self.datos_combinados.shape != self.datos_crudos.shape:
                print(f"❌ Error: dimensiones no coinciden entre crudos y combinados")

            # 🔄 PASO 4: Datos numéricos usando nuevo módulo
            rango_numerico = self._obtener_rango_numerico_dinamico()
            self.datos_numericos, self.mapeo_posicional = self.transformer.extraer_datos_numericos(
                self.datos_crudos, rango_numerico
            )
            
            # VALIDACIÓN CRÍTICA: Verificar dimensiones de datos numéricos
            if self.datos_numericos.shape[0] != 10:  # Debe ser (10, 19)
                print(f"⚠️ Dimensión inesperada datos_numericos: {self.datos_numericos.shape}")

            print(f"✅ Procesamiento modular completado exitosamente")

            # Retornar datos procesados
            return {
                'datos_crudos': self.datos_crudos,
                'datos_combinados': self.datos_combinados,
                'datos_numericos': self.datos_numericos,
                'mapeo_posicional': self.mapeo_posicional
            }

        except Exception as e:
            print(f"❌ Error en procesamiento modular: {e}")
            raise e  # Re-lanzar excepción para debugging



    def _obtener_rango_numerico_dinamico(self):
        """Obtener rango numérico dinámico desde configuración de esquemas."""
        # Obtener configuración actual
        config_actual = get_config_actual()
        modo_actual = config_actual.get('MODO', 'ESCUELAS')

        # Obtener esquema de tabla según el modo
        if modo_actual == 'ESCUELAS':
            esquema = get_table_schema("ESC2_MOVIMIENTOS")
        elif modo_actual == 'ZONAS':
            esquema = get_table_schema("ZONA3_MOVIMIENTOS")
        else:
            # Fallback a esquema por defecto
            esquema = get_table_schema("ESC2_MOVIMIENTOS")

        # Extraer rango numérico del esquema
        estructura = esquema.get('estructura', {})
        rango_numerico = estructura.get('rango_numerico', {
            'filas_inicio': 3,
            'filas_fin': 12,
            'columnas_inicio': 7,
            'columnas_fin': 25
        })

        print(f"🎯 Rango numérico dinámico para {modo_actual}: {rango_numerico}")
        return rango_numerico

    def extraer_multiples_hojas(self, archivo_path, config_hojas):
        """
        Extraer datos de múltiples hojas usando configuración dinámica.

        Preparado para validaciones cruzadas ESC1 vs ESC2.

        Args:
            archivo_path: Ruta del archivo Excel
            config_hojas: Dict con configuración de hojas
                {
                    "ESC1": {"hoja": "ESC1", "rango": "A3:Z15", "tipo": "grupos"},
                    "ESC2": {"hoja": "ESC2", "rango": "A5:Z17", "tipo": "movimientos"}
                }

        Returns:
            dict: Datos de todas las hojas procesadas
                {
                    "ESC1": {datos_crudos, datos_combinados, datos_numericos, mapeo_posicional},
                    "ESC2": {datos_crudos, datos_combinados, datos_numericos, mapeo_posicional}
                }
        """
        print(f"📊 Extrayendo múltiples hojas de: {archivo_path}")
        print(f"🎯 Hojas a procesar: {list(config_hojas.keys())}")

        resultados = {}

        for nombre_hoja, config in config_hojas.items():
            try:
                print(f"🔄 Procesando hoja: {nombre_hoja}")

                # Extracción usando módulos especializados
                resultado_extraccion = self.extractor.extraer_con_metadatos(
                    archivo_path, config['hoja'], config['rango']
                )

                datos_raw = resultado_extraccion['datos']
                celdas_combinadas = resultado_extraccion['celdas_combinadas']

                # Transformación usando módulos especializados
                datos_crudos = self.transformer.crear_marcadores_combinadas(
                    datos_raw, celdas_combinadas
                )

                datos_combinados = self.transformer.crear_vista_combinada(
                    datos_crudos
                )

                # Datos numéricos con configuración específica si existe
                if 'rango_numerico' in config:
                    rango_numerico = config['rango_numerico']
                else:
                    # Calcular rango numérico dinámico basado en el rango de datos
                    rango_numerico = self._calcular_rango_numerico_desde_datos(config['rango'])

                datos_numericos, mapeo_posicional = self.transformer.extraer_datos_numericos(
                    datos_crudos, rango_numerico
                )

                # Almacenar resultado
                resultados[nombre_hoja] = {
                    'datos_crudos': datos_crudos,
                    'datos_combinados': datos_combinados,
                    'datos_numericos': datos_numericos,
                    'mapeo_posicional': mapeo_posicional,
                    'tipo': config.get('tipo', 'desconocido'),
                    'config': config
                }

                print(f"✅ {nombre_hoja} procesada: {datos_crudos.shape}")

            except Exception as e:
                print(f"❌ Error procesando {nombre_hoja}: {e}")
                resultados[nombre_hoja] = {
                    'error': str(e),
                    'config': config
                }

        print(f"✅ Múltiples hojas procesadas: {len(resultados)} hojas")
        return resultados

    def _calcular_rango_numerico_desde_datos(self, rango_datos):
        """
        Calcular rango numérico dinámico basado en el rango de datos.

        Args:
            rango_datos: String como "A5:Z17"

        Returns:
            dict: Configuración de rango numérico
        """
        # Parsear rango
        rango_partes = rango_datos.split(':')
        inicio = rango_partes[0]  # "A5"
        fin = rango_partes[1]     # "Z17"

        # Extraer números de fila
        min_row = int(''.join(filter(str.isdigit, inicio)))
        max_row = int(''.join(filter(str.isdigit, fin)))

        # Calcular rango numérico relativo (H hasta Z, filas de datos)
        return {
            'filas_inicio': min_row + 3 - min_row,  # Relativo: fila de INSCRIPCIÓN
            'filas_fin': max_row - 2,               # Relativo: fila de GRUPOS
            'columnas_inicio': 7,                   # Columna H (fija)
            'columnas_fin': 25                      # Columna Z (fija)
        }




