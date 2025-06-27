"""
🎮 APP CONTROLLER - Controlador Principal de Aplicación
======================================================

Controlador principal que coordina toda la lógica de la aplicación
sin mezclarse con la interfaz gráfica.

RESPONSABILIDADES:
✅ Coordinación de procesamiento de datos
✅ Gestión de estado de la aplicación
✅ Orquestación de validaciones
✅ Control de flujo de trabajo
✅ Sin lógica de interfaz gráfica
"""

from typing import Dict, List, Any, Optional
from ..core.data_manager import DataManager
from ..core.data_validator import DataValidator
from ..core.template_injector import TemplateInjector
from ..config.settings import get_config_actual, configurar_modo


class AppController:
    """
    Controlador principal de la aplicación.
    
    Coordina toda la lógica sin mezclarse con la interfaz gráfica.
    """
    
    def __init__(self):
        """Inicializar controlador de aplicación."""
        # Gestores principales
        self.data_manager = DataManager()
        self.data_validator = DataValidator()
        self.template_injector = TemplateInjector()
        
        # Estado de la aplicación
        self.archivos_procesados = {}
        self.sumatoria_total = None
        self.modo_actual = None
        self.validaciones_activas = True
        
        # Configuración
        self.config_actual = get_config_actual()
        self.modo_actual = self.config_actual.get('MODO', 'ESCUELAS')
        
        print(f"🎮 AppController inicializado - Modo: {self.modo_actual}")
    
    def cambiar_modo(self, nuevo_modo: str) -> bool:
        """
        Cambiar modo de operación de la aplicación.
        
        Args:
            nuevo_modo: Nuevo modo ('ESCUELAS' o 'ZONAS')
            
        Returns:
            bool: True si el cambio fue exitoso
        """
        try:
            configurar_modo(nuevo_modo)
            self.modo_actual = nuevo_modo
            self.config_actual = get_config_actual()
            
            # Reinicializar gestores con nueva configuración
            self.data_manager = DataManager()
            self.data_validator = DataValidator()
            self.template_injector = TemplateInjector()
            
            print(f"✅ Modo cambiado a: {nuevo_modo}")
            return True
            
        except Exception as e:
            print(f"❌ Error cambiando modo: {e}")
            return False
    
    def procesar_archivo(self, archivo_path: str) -> Dict[str, Any]:
        """
        Procesar un archivo Excel completo.
        
        Args:
            archivo_path: Ruta del archivo a procesar
            
        Returns:
            dict: Resultado del procesamiento
        """
        try:
            print(f"🎮 Procesando archivo: {archivo_path}")
            
            # Procesar usando DataManager
            datos_procesados = self.data_manager.procesar_archivo(archivo_path)
            
            # Validar si está habilitado
            reporte_validacion = None
            if self.validaciones_activas:
                reporte_validacion = self._validar_archivo(archivo_path, datos_procesados)
            
            # Actualizar estado
            nombre_archivo = archivo_path.split('/')[-1]
            self.archivos_procesados[nombre_archivo] = {
                'datos': datos_procesados,
                'validacion': reporte_validacion,
                'archivo_completo': archivo_path
            }
            
            return {
                'exito': True,
                'datos': datos_procesados,
                'validacion': reporte_validacion,
                'archivo': nombre_archivo
            }
            
        except Exception as e:
            print(f"❌ Error procesando archivo: {e}")
            return {
                'exito': False,
                'error': str(e),
                'archivo': archivo_path
            }
    
    def _validar_archivo(self, archivo_path: str, datos_procesados: Dict) -> Dict[str, Any]:
        """
        Validar un archivo procesado.
        
        Args:
            archivo_path: Ruta del archivo
            datos_procesados: Datos ya procesados
            
        Returns:
            dict: Reporte de validación
        """
        try:
            nombre_archivo = archivo_path.split('/')[-1]
            print(f"🔍 Validando: {nombre_archivo}")
            
            # Validar usando DataValidator
            reporte = self.data_validator.validar_tabla_completa(
                datos_procesados['datos_numericos'],
                datos_procesados['datos_crudos']
            )
            
            # Agregar información del archivo
            reporte['archivo'] = nombre_archivo
            reporte['archivo_completo'] = archivo_path
            
            return reporte
            
        except Exception as e:
            print(f"❌ Error validando archivo: {e}")
            return {
                'archivo': archivo_path,
                'error': str(e),
                'validacion_exitosa': False
            }
    
    def calcular_sumatoria(self) -> Dict[str, Any]:
        """
        Calcular sumatoria total de todos los archivos procesados.
        
        Returns:
            dict: Resultado del cálculo
        """
        try:
            print("🎮 Calculando sumatoria total...")
            
            if not self.archivos_procesados:
                return {
                    'exito': False,
                    'mensaje': 'No hay archivos procesados para sumar'
                }
            
            # Calcular usando DataManager
            self.sumatoria_total = self.data_manager.calcular_sumatoria()
            
            if self.sumatoria_total is not None:
                print(f"✅ Sumatoria calculada: {self.sumatoria_total.shape}")
                return {
                    'exito': True,
                    'sumatoria': self.sumatoria_total,
                    'archivos_incluidos': len(self.archivos_procesados)
                }
            else:
                return {
                    'exito': False,
                    'mensaje': 'Error calculando sumatoria'
                }
                
        except Exception as e:
            print(f"❌ Error calculando sumatoria: {e}")
            return {
                'exito': False,
                'error': str(e)
            }
    
    def exportar_a_plantilla(self, archivo_destino: str) -> Dict[str, Any]:
        """
        Exportar sumatoria a plantilla Excel.
        
        Args:
            archivo_destino: Ruta donde guardar el resultado
            
        Returns:
            dict: Resultado de la exportación
        """
        try:
            print(f"🎮 Exportando a plantilla: {archivo_destino}")
            
            if self.sumatoria_total is None:
                return {
                    'exito': False,
                    'mensaje': 'No hay sumatoria calculada para exportar'
                }
            
            # Obtener plantilla desde configuración dinámica
            plantilla_path = self.template_injector._obtener_plantilla_dinamica()
            
            # Exportar usando TemplateInjector
            exito = self.template_injector.inyectar_en_plantilla(
                self.sumatoria_total, plantilla_path, archivo_destino
            )
            
            if exito:
                return {
                    'exito': True,
                    'archivo_destino': archivo_destino,
                    'plantilla_usada': plantilla_path
                }
            else:
                return {
                    'exito': False,
                    'mensaje': 'Error durante la exportación'
                }
                
        except Exception as e:
            print(f"❌ Error exportando: {e}")
            return {
                'exito': False,
                'error': str(e)
            }
    
    def obtener_estado_aplicacion(self) -> Dict[str, Any]:
        """
        Obtener estado actual de la aplicación.
        
        Returns:
            dict: Estado completo de la aplicación
        """
        return {
            'modo_actual': self.modo_actual,
            'archivos_procesados': len(self.archivos_procesados),
            'lista_archivos': list(self.archivos_procesados.keys()),
            'sumatoria_calculada': self.sumatoria_total is not None,
            'validaciones_activas': self.validaciones_activas,
            'configuracion': self.config_actual
        }
    
    def limpiar_datos(self):
        """Limpiar todos los datos procesados."""
        self.archivos_procesados.clear()
        self.sumatoria_total = None
        self.data_manager.limpiar_datos()
        print("🧹 Datos de aplicación limpiados")
    
    def habilitar_validaciones(self, habilitar: bool = True):
        """
        Habilitar o deshabilitar validaciones automáticas.
        
        Args:
            habilitar: True para habilitar, False para deshabilitar
        """
        self.validaciones_activas = habilitar
        print(f"🔍 Validaciones {'habilitadas' if habilitar else 'deshabilitadas'}")
    
    def obtener_resumen_validaciones(self) -> Dict[str, Any]:
        """
        Obtener resumen de todas las validaciones realizadas.
        
        Returns:
            dict: Resumen de validaciones
        """
        total_archivos = len(self.archivos_procesados)
        archivos_con_errores = 0
        total_discrepancias = 0
        
        for archivo_info in self.archivos_procesados.values():
            validacion = archivo_info.get('validacion')
            if validacion and validacion.get('discrepancias'):
                archivos_con_errores += 1
                total_discrepancias += len(validacion['discrepancias'])
        
        return {
            'total_archivos': total_archivos,
            'archivos_con_errores': archivos_con_errores,
            'archivos_sin_errores': total_archivos - archivos_con_errores,
            'total_discrepancias': total_discrepancias,
            'porcentaje_exito': ((total_archivos - archivos_con_errores) / total_archivos * 100) if total_archivos > 0 else 0
        }

    def obtener_datos_archivo(self, nombre_archivo: str) -> Dict[str, Any]:
        """
        Obtener datos procesados de un archivo específico.

        Args:
            nombre_archivo: Nombre del archivo

        Returns:
            dict: Datos del archivo o None si no existe
        """
        try:
            if nombre_archivo in self.archivos_procesados:
                return self.archivos_procesados[nombre_archivo]
            else:
                print(f"⚠️ Archivo no encontrado: {nombre_archivo}")
                return None

        except Exception as e:
            print(f"❌ Error obteniendo datos de archivo: {e}")
            return None

    def obtener_estado(self) -> Dict[str, Any]:
        """
        Obtener estado actual del controlador.

        Returns:
            dict: Estado del controlador
        """
        return {
            'modo_actual': self.modo_actual,
            'archivos_procesados': len(self.archivos_procesados),
            'sumatoria_disponible': self.sumatoria_total is not None,
            'data_manager_activo': self.data_manager is not None,
            'template_injector_activo': self.template_injector is not None
        }
