"""
💉 TEMPLATE INJECTOR - Coordinador de Inyección Modular
======================================================

Coordinador que orquesta la inyección de datos en plantillas Excel
usando módulos especializados con responsabilidades únicas.

ARQUITECTURA MODULAR:
✅ TemplateManager: Gestión de plantillas
✅ DataMapper: Mapeo de datos
✅ ExcelWriter: Escritura en Excel
✅ TemplateInjector: Solo coordinación

CARACTERÍSTICAS:
✅ Responsabilidad única: coordinación
✅ Sin hardcodeo de configuración
✅ Configuración dinámica por esquemas
✅ Extensible y mantenible
"""

from typing import Dict, Any, Optional
from ..config.settings import get_config_actual
from ..config.table_schemas import get_table_schema
from .template_manager import TemplateManager
from .data_mapper import DataMapper
from .excel_writer import ExcelWriter


class TemplateInjector:
    """
    Coordinador de inyección con arquitectura modular.

    Responsabilidad única: coordinar la inyección usando módulos especializados.
    """

    def __init__(self, esquema_nombre: Optional[str] = None):
        """
        Inicializar coordinador de inyección.

        Args:
            esquema_nombre: Nombre del esquema a usar (opcional, se detecta automáticamente)
        """
        # Configuración dinámica
        self.config_actual = get_config_actual()
        self.modo_actual = self.config_actual.get('MODO', 'ESCUELAS')

        # Determinar esquema
        if esquema_nombre is None:
            if self.modo_actual == 'ESCUELAS':
                self.esquema_nombre = "ESC2_MOVIMIENTOS"
            elif self.modo_actual == 'ZONAS':
                self.esquema_nombre = "ZONA3_MOVIMIENTOS"
            else:
                self.esquema_nombre = "ESC2_MOVIMIENTOS"
        else:
            self.esquema_nombre = esquema_nombre

        # Inicializar módulos especializados
        self.template_manager = TemplateManager()
        self.data_mapper = DataMapper()
        self.excel_writer = ExcelWriter()

        # Cargar configuración del esquema
        self.esquema = self._cargar_esquema()

        print(f"💉 TemplateInjector inicializado - Modo: {self.modo_actual}, Esquema: {self.esquema_nombre}")

    def _cargar_esquema(self) -> Dict[str, Any]:
        """
        Cargar esquema de configuración.

        Returns:
            dict: Esquema de configuración
        """
        try:
            esquema = get_table_schema(self.esquema_nombre)
            print(f"✅ Esquema cargado: {self.esquema_nombre}")
            return esquema
        except Exception as e:
            print(f"⚠️ Error cargando esquema {self.esquema_nombre}: {e}")
            print("🔄 Usando configuración por defecto...")

            # Esquema por defecto
            return {
                'estructura': {
                    'rango_inyeccion': {
                        'fila_inicio': 6,
                        'columna_inicio': 8,
                        'columna_fin': 26
                    }
                }
            }
    
    def inyectar_en_plantilla(self, datos_sumatoria, plantilla_path, archivo_destino):
        """
        Inyectar datos de sumatoria en plantilla Excel
        
        Args:
            datos_sumatoria: DataFrame con datos a inyectar
            plantilla_path: Ruta de la plantilla base
            archivo_destino: Ruta donde guardar el resultado
            
        Returns:
            bool: True si la inyección fue exitosa
        """
        try:
            print(f"💉 Iniciando inyección modular...")
            print(f"📋 Plantilla: {plantilla_path}")
            print(f"📤 Destino: {archivo_destino}")
            print(f"📊 Datos: {datos_sumatoria.shape}")

            # PASO 1: Validar plantilla usando TemplateManager
            validacion = self.template_manager.validar_plantilla(plantilla_path)
            if not validacion['valida']:
                print(f"❌ Plantilla inválida: {validacion['mensaje']}")
                return False

            print(f"✅ Plantilla válida: {validacion['hoja_principal']}")

            # PASO 2: Validar datos usando DataMapper
            validacion_datos = self.data_mapper.validar_datos_para_mapeo(datos_sumatoria)
            if not validacion_datos['valido']:
                print(f"❌ Datos inválidos: {validacion_datos['mensaje']}")
                return False

            print(f"✅ Datos válidos: {validacion_datos['detalles']}")

            # PASO 3: Mapear datos usando DataMapper con esquema dinámico
            datos_mapeados = self.data_mapper.mapear_con_esquema_dinamico(
                datos_sumatoria, self.esquema_nombre
            )

            if not datos_mapeados:
                print("⚠️ No hay datos para inyectar")
                return False

            # PASO 4: Crear backup solo si está configurado
            backup_path = None
            crear_backup = self.config_actual.get('CREAR_BACKUP', False)
            if crear_backup:
                backup_path = self.excel_writer.crear_backup(plantilla_path)
            else:
                print("⏭️ Backup deshabilitado en configuración")

            # PASO 5: Copiar plantilla a destino
            import shutil
            shutil.copy2(plantilla_path, archivo_destino)
            print(f"📋 Plantilla copiada a destino: {archivo_destino}")

            # PASO 6: Determinar hoja de destino desde configuración
            hoja_destino = self._obtener_hoja_destino()
            print(f"🎯 Hoja de destino: '{hoja_destino}'")

            # PASO 7: Escribir datos usando ExcelWriter
            exito_escritura = self.excel_writer.escribir_datos_en_hoja(
                archivo_destino, hoja_destino, datos_mapeados, preservar_combinadas=True
            )

            if exito_escritura:
                # PASO 8: Obtener estadísticas
                estadisticas = self.data_mapper.obtener_estadisticas_mapeo(datos_mapeados)
                print(f"📊 Estadísticas de inyección: {estadisticas}")

                print(f"✅ Inyección modular completada exitosamente")
                if backup_path:
                    print(f"💾 Backup disponible en: {backup_path}")
                return True
            else:
                print("❌ Error en escritura de datos")
                return False

        except Exception as e:
            print(f"❌ Error en inyección modular: {str(e)}")
            raise

    def _obtener_hoja_destino(self) -> str:
        """
        Obtener hoja de destino desde configuración dinámica.

        Returns:
            str: Nombre de la hoja de destino
        """
        try:
            # Intentar obtener desde esquema
            estructura = self.esquema.get('estructura', {})
            rango_inyeccion = estructura.get('rango_inyeccion', {})
            hoja_destino = rango_inyeccion.get('hoja_destino')

            if hoja_destino:
                print(f"✅ Hoja destino desde esquema: '{hoja_destino}'")
                return hoja_destino

            # Fallback: obtener desde configuración de modo
            hoja_destino = self.config_actual.get('HOJA_INYECCION')
            if hoja_destino:
                print(f"✅ Hoja destino desde configuración: '{hoja_destino}'")
                return hoja_destino

            # Fallback final: usar hoja de datos
            hoja_destino = self.config_actual.get('HOJA_DATOS', 'Sheet1')
            print(f"⚠️ Usando hoja de datos como destino: '{hoja_destino}'")
            return hoja_destino

        except Exception as e:
            print(f"❌ Error obteniendo hoja destino: {e}")
            return "Sheet1"  # Fallback absoluto

    def _obtener_plantilla_dinamica(self) -> str:
        """
        Obtener ruta de plantilla desde configuración dinámica.

        Returns:
            str: Ruta de la plantilla
        """
        try:
            # Intentar obtener desde configuración de modo
            plantilla = self.config_actual.get('PLANTILLA')
            if plantilla:
                print(f"✅ Plantilla desde configuración: '{plantilla}'")
                return plantilla

            # Fallback: usar plantilla por defecto del template manager
            plantilla_default = self.template_manager.obtener_plantilla_por_defecto()
            if plantilla_default:
                print(f"✅ Plantilla por defecto: '{plantilla_default}'")
                return plantilla_default

            # Fallback final
            print("⚠️ Usando plantilla_base.xlsx como fallback")
            return "plantilla_base.xlsx"

        except Exception as e:
            print(f"❌ Error obteniendo plantilla: {e}")
            return "plantilla_base.xlsx"

    def configurar_esquema(self, nuevo_esquema_nombre: str):
        """
        Configurar nuevo esquema de inyección.

        Args:
            nuevo_esquema_nombre: Nombre del nuevo esquema
        """
        self.esquema_nombre = nuevo_esquema_nombre
        self.esquema = self._cargar_esquema()
        print(f"⚙️ Esquema configurado: {nuevo_esquema_nombre}")

    def obtener_configuracion_actual(self) -> Dict[str, Any]:
        """
        Obtener configuración actual del inyector.

        Returns:
            dict: Configuración actual
        """
        return {
            'modo': self.modo_actual,
            'esquema_nombre': self.esquema_nombre,
            'esquema': self.esquema,
            'rango_inyeccion': self.esquema.get('estructura', {}).get('rango_inyeccion', {})
        }

    # MÉTODOS LEGACY ELIMINADOS - Ahora se usan módulos especializados:
    # - _inyectar_datos() -> ExcelWriter.escribir_datos_en_hoja()
    # - _crear_mapa_combinadas() -> ExcelWriter._crear_mapa_combinadas()
    # - _inyectar_valor() -> ExcelWriter._escribir_valor_en_celda()
    # - configurar_rango_inyeccion() -> DataMapper.mapear_con_esquema_dinamico()
    # - validar_plantilla() -> TemplateManager.validar_plantilla()
    # - obtener_info_plantilla() -> TemplateManager.obtener_info_plantilla()
