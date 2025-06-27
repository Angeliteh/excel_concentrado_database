"""
📊 DATA MANAGER - Gestor Modular de Datos
========================================

Gestor centralizado que coordina el procesamiento de múltiples archivos
usando la nueva arquitectura modular.

CARACTERÍSTICAS:
✅ Arquitectura modular integrada
✅ Soporte para múltiples hojas
✅ Configuración dinámica
✅ Preparado para validaciones cruzadas
✅ Extensible para IA y análisis avanzado
"""

import pandas as pd
from ..config.settings import get_config_actual
from ..config.table_schemas import get_table_schema
from .excel_processor import ExcelProcessor


class DataManager:
    """
    Gestor centralizado de datos con arquitectura modular.

    Coordina el procesamiento de múltiples archivos y mantiene
    compatibilidad total con la interfaz existente.
    """

    def __init__(self):
        """Inicializar gestor con arquitectura modular."""
        self.archivos_procesados = {}
        self.sumatoria_total = None
        self.processor = ExcelProcessor()

        # Configuración dinámica
        self.config_actual = get_config_actual()
        self.modo_actual = self.config_actual.get('MODO', 'ESCUELAS')

        print(f"📊 DataManager inicializado - Modo: {self.modo_actual}")
        
    def procesar_archivo(self, archivo_path):
        """
        COPIA EXACTA del comportamiento de main_pyqt.py

        Args:
            archivo_path: Ruta del archivo Excel

        Returns:
            dict: Datos procesados del archivo
        """
        nombre_archivo = archivo_path.split('/')[-1]

        try:
            # USAR ExcelProcessor exactamente como en main_pyqt.py
            datos_procesados = self.processor.extraer_datos_completo(archivo_path)

            # Agregar a la colección CON FORMATO EXACTO de main_pyqt.py
            self.archivos_procesados[nombre_archivo] = {
                'archivo_completo': archivo_path,
                'datos_crudos': datos_procesados['datos_crudos'].copy(),
                'datos_combinados': datos_procesados['datos_combinados'].copy(),
                'datos_numericos': datos_procesados['datos_numericos'].copy(),
                'mapeo_posicional': datos_procesados['mapeo_posicional'].copy(),
                'modo': self.modo_actual,
                'tipo_procesamiento': 'hoja_unica'
            }

            print(f"✅ Archivo procesado y agregado: {nombre_archivo}")
            return datos_procesados

        except Exception as e:
            print(f"❌ Error procesando {nombre_archivo}: {str(e)}")
            raise

    def procesar_archivo_multiples_hojas(self, archivo_path, config_hojas=None):
        """
        Procesar archivo con múltiples hojas usando configuración dinámica.

        Preparado para validaciones cruzadas ESC1 vs ESC2.

        Args:
            archivo_path: Ruta del archivo Excel
            config_hojas: Configuración opcional de hojas. Si None, usa configuración por defecto.

        Returns:
            dict: Datos de todas las hojas procesadas
        """
        nombre_archivo = archivo_path.split('/')[-1]
        print(f"📊 Procesando múltiples hojas: {nombre_archivo}")

        # Configuración por defecto si no se proporciona
        if config_hojas is None:
            config_hojas = self._obtener_config_hojas_por_defecto()

        try:
            # Usar nuevo método de múltiples hojas
            resultados_hojas = self.processor.extraer_multiples_hojas(archivo_path, config_hojas)

            # Almacenar resultados con estructura extendida
            self.archivos_procesados[nombre_archivo] = {
                'archivo_completo': archivo_path,
                'tipo_procesamiento': 'multiples_hojas',
                'hojas': resultados_hojas,
                'config_hojas': config_hojas,
                'modo': self.modo_actual
            }

            print(f"✅ Múltiples hojas procesadas: {nombre_archivo}")
            return resultados_hojas

        except Exception as e:
            print(f"❌ Error procesando múltiples hojas {nombre_archivo}: {e}")
            raise e

    def _obtener_config_hojas_por_defecto(self):
        """
        Obtener configuración de hojas por defecto según el modo actual.

        Returns:
            dict: Configuración de hojas
        """
        if self.modo_actual == 'ESCUELAS':
            return {
                "ESC2": {
                    "hoja": "ESC2",
                    "rango": "A5:Z17",
                    "tipo": "movimientos",
                    "esquema": "ESC2_MOVIMIENTOS"
                }
                # Preparado para agregar ESC1 cuando sea necesario
                # "ESC1": {
                #     "hoja": "ESC1",
                #     "rango": "A3:Z15",
                #     "tipo": "grupos",
                #     "esquema": "ESC1_GRUPOS"
                # }
            }
        elif self.modo_actual == 'ZONAS':
            return {
                "ZONA3": {
                    "hoja": "ZONA3",
                    "rango": self.config_actual['RANGO_DATOS'],
                    "tipo": "movimientos",
                    "esquema": "ZONA3_MOVIMIENTOS"
                }
            }
        else:
            # Fallback
            return {
                "DEFAULT": {
                    "hoja": self.config_actual['HOJA_DATOS'],
                    "rango": self.config_actual['RANGO_DATOS'],
                    "tipo": "movimientos",
                    "esquema": "DEFAULT_MOVIMIENTOS"
                }
            }

    def obtener_datos_para_validacion_cruzada(self, nombre_archivo):
        """
        Obtener datos preparados para validación cruzada entre hojas.

        Args:
            nombre_archivo: Nombre del archivo procesado

        Returns:
            dict: Datos estructurados para validación cruzada
        """
        if nombre_archivo not in self.archivos_procesados:
            raise ValueError(f"Archivo {nombre_archivo} no encontrado")

        archivo_data = self.archivos_procesados[nombre_archivo]

        if archivo_data.get('tipo_procesamiento') == 'multiples_hojas':
            # Datos de múltiples hojas - preparados para validación cruzada
            hojas = archivo_data['hojas']

            datos_validacion = {
                'archivo': nombre_archivo,
                'modo': archivo_data['modo'],
                'hojas_disponibles': list(hojas.keys()),
                'datos_por_hoja': {}
            }

            for nombre_hoja, datos_hoja in hojas.items():
                if 'error' not in datos_hoja:
                    datos_validacion['datos_por_hoja'][nombre_hoja] = {
                        'datos_numericos': datos_hoja['datos_numericos'],
                        'datos_crudos': datos_hoja['datos_crudos'],
                        'tipo': datos_hoja['tipo'],
                        'config': datos_hoja['config']
                    }

            return datos_validacion
        else:
            # Datos de hoja única - formato compatible
            return {
                'archivo': nombre_archivo,
                'modo': archivo_data.get('modo', self.modo_actual),
                'hojas_disponibles': ['principal'],
                'datos_por_hoja': {
                    'principal': {
                        'datos_numericos': archivo_data['datos_numericos'],
                        'datos_crudos': archivo_data['datos_crudos'],
                        'tipo': 'movimientos',
                        'config': {'hoja': 'principal'}
                    }
                }
            }
    def procesar_multiples_archivos(self, archivos_paths, callback_progreso=None):
        """
        Procesar múltiples archivos con callback de progreso
        
        Args:
            archivos_paths: Lista de rutas de archivos
            callback_progreso: Función callback para reportar progreso
            
        Returns:
            dict: Resumen del procesamiento
        """
        total_archivos = len(archivos_paths)
        archivos_exitosos = 0
        archivos_fallidos = []
        
        for i, archivo_path in enumerate(archivos_paths):
            try:
                # Reportar progreso
                if callback_progreso:
                    callback_progreso(i, total_archivos, archivo_path)
                
                # Procesar archivo
                self.procesar_archivo(archivo_path)
                archivos_exitosos += 1
                
            except Exception as e:
                archivos_fallidos.append({
                    'archivo': archivo_path,
                    'error': str(e)
                })
        
        # Reportar progreso final
        if callback_progreso:
            callback_progreso(total_archivos, total_archivos, "Completado")
        
        return {
            'total': total_archivos,
            'exitosos': archivos_exitosos,
            'fallidos': len(archivos_fallidos),
            'errores': archivos_fallidos
        }
    
    def calcular_sumatoria(self):
        """
        Calcular sumatoria de todos los archivos procesados
        
        Returns:
            pd.DataFrame: DataFrame con la sumatoria total
        """
        if len(self.archivos_procesados) < 2:
            raise ValueError("Se necesitan al menos 2 archivos para calcular sumatoria")
        
        print("➕ Calculando sumatoria total...")
        
        # Obtener todos los DataFrames numéricos
        dataframes_numericos = []
        for nombre, datos in self.archivos_procesados.items():
            df_numerico = datos['datos_numericos']
            dataframes_numericos.append(df_numerico)
            print(f"   📊 {nombre}: {df_numerico.shape}")
        
        # Sumar todos los DataFrames
        self.sumatoria_total = dataframes_numericos[0].copy()
        for df in dataframes_numericos[1:]:
            self.sumatoria_total = self.sumatoria_total.add(df, fill_value=0)
        
        print(f"✅ Sumatoria calculada: {self.sumatoria_total.shape}")
        return self.sumatoria_total
    
    def obtener_archivo(self, nombre_archivo):
        """
        Obtener datos de un archivo específico
        
        Args:
            nombre_archivo: Nombre del archivo
            
        Returns:
            dict: Datos del archivo o None si no existe
        """
        return self.archivos_procesados.get(nombre_archivo)
    
    def obtener_lista_archivos(self):
        """
        Obtener lista de archivos procesados
        
        Returns:
            list: Lista de nombres de archivos
        """
        return list(self.archivos_procesados.keys())
    
    def obtener_resumen_archivos(self):
        """
        Obtener resumen de todos los archivos procesados
        
        Returns:
            list: Lista de diccionarios con resumen de cada archivo
        """
        resumen = []
        for nombre, datos in self.archivos_procesados.items():
            df_numerico = datos['datos_numericos']
            resumen.append({
                'nombre': nombre,
                'filas': df_numerico.shape[0],
                'columnas': df_numerico.shape[1],
                'archivo_completo': datos['archivo_completo']
            })
        return resumen
    
    def limpiar_datos(self):
        """Limpiar todos los datos almacenados"""
        self.archivos_procesados.clear()
        self.sumatoria_total = None
        print("🗑️ Datos limpiados")
    
    def eliminar_archivo(self, nombre_archivo):
        """
        Eliminar un archivo específico de la colección
        
        Args:
            nombre_archivo: Nombre del archivo a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        if nombre_archivo in self.archivos_procesados:
            del self.archivos_procesados[nombre_archivo]
            # Recalcular sumatoria si había una
            if self.sumatoria_total is not None and len(self.archivos_procesados) > 1:
                self.calcular_sumatoria()
            elif len(self.archivos_procesados) <= 1:
                self.sumatoria_total = None
            print(f"🗑️ Archivo eliminado: {nombre_archivo}")
            return True
        return False
    
    def configurar_rango_extraccion(self, nuevo_rango):
        """
        Configurar rango de extracción para futuros procesamientos
        
        Args:
            nuevo_rango: Diccionario con configuración del rango
        """
        self.processor.configurar_rango(nuevo_rango)
        print(f"⚙️ Rango de extracción configurado: {nuevo_rango}")
    
    def validar_consistencia(self):
        """
        Validar que todos los archivos tengan la misma estructura
        
        Returns:
            dict: Resultado de la validación
        """
        if len(self.archivos_procesados) < 2:
            return {'valido': True, 'mensaje': 'Solo un archivo, no hay inconsistencias'}
        
        # Obtener forma del primer archivo
        primer_archivo = list(self.archivos_procesados.values())[0]
        forma_esperada = primer_archivo['datos_numericos'].shape
        
        inconsistencias = []
        for nombre, datos in self.archivos_procesados.items():
            forma_actual = datos['datos_numericos'].shape
            if forma_actual != forma_esperada:
                inconsistencias.append({
                    'archivo': nombre,
                    'forma_esperada': forma_esperada,
                    'forma_actual': forma_actual
                })
        
        if inconsistencias:
            return {
                'valido': False,
                'mensaje': f'Se encontraron {len(inconsistencias)} inconsistencias',
                'inconsistencias': inconsistencias
            }
        else:
            return {
                'valido': True,
                'mensaje': f'Todos los {len(self.archivos_procesados)} archivos son consistentes'
            }
