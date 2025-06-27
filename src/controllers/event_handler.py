"""
🎮 EVENT HANDLER - Manejador de Eventos
=======================================

Controlador especializado en manejo de eventos de la interfaz.
Coordina la comunicación entre UI y lógica de negocio.

RESPONSABILIDADES:
✅ Manejo de clicks de botones
✅ Eventos de selección de archivos
✅ Cambios de tabs y navegación
✅ Eventos de validación
✅ Coordinación entre componentes
✅ Sin lógica de negocio directa
"""

from typing import Dict, Any, Optional, Callable
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from .app_controller import AppController
from .ui_manager import UIManager


class EventHandler(QObject):
    """
    Manejador de eventos de la interfaz.
    
    Coordina eventos entre UI y controladores de negocio.
    """
    
    # Señales para comunicación
    archivo_procesado = pyqtSignal(str, dict)
    sumatoria_calculada = pyqtSignal(dict)
    exportacion_completada = pyqtSignal(str, bool)
    error_ocurrido = pyqtSignal(str, str)
    
    def __init__(self, app_controller: AppController, ui_manager: UIManager):
        """
        Inicializar manejador de eventos.
        
        Args:
            app_controller: Controlador de aplicación
            ui_manager: Gestor de interfaz
        """
        super().__init__()
        self.app_controller = app_controller
        self.ui_manager = ui_manager
        
        # Configurar conexiones
        self._configurar_conexiones()
        
        print("🎮 EventHandler inicializado")
    
    def _configurar_conexiones(self):
        """Configurar conexiones entre controladores."""
        try:
            # Conectar señales del UI Manager
            self.ui_manager.archivo_seleccionado.connect(self.manejar_seleccion_archivo)
            self.ui_manager.sumatoria_solicitada.connect(self.manejar_solicitud_sumatoria)
            self.ui_manager.exportacion_solicitada.connect(self.manejar_solicitud_exportacion)
            
            print("🔗 Conexiones de eventos configuradas")
            
        except Exception as e:
            print(f"⚠️ Error configurando conexiones de eventos: {e}")
    
    def manejar_seleccion_archivo(self):
        """Manejar evento de selección de archivo."""
        try:
            # Abrir diálogo de selección
            archivo, _ = QFileDialog.getOpenFileName(
                self.ui_manager.main_window,
                "Seleccionar archivo Excel",
                "",
                "Archivos Excel (*.xlsx *.xls)"
            )
            
            if archivo:
                self.procesar_archivo_seleccionado(archivo)
            
        except Exception as e:
            print(f"❌ Error en selección de archivo: {e}")
            self.error_ocurrido.emit("Selección de Archivo", str(e))
    
    def procesar_archivo_seleccionado(self, archivo_path: str):
        """
        Procesar archivo seleccionado.
        
        Args:
            archivo_path: Ruta del archivo seleccionado
        """
        try:
            print(f"🎮 Procesando archivo seleccionado: {archivo_path}")
            
            # Procesar usando AppController
            resultado = self.app_controller.procesar_archivo(archivo_path)
            
            if resultado['exito']:
                # Actualizar UI
                nombre_archivo = resultado['archivo']
                datos = resultado['datos']
                
                # Mostrar datos en tablas
                self.ui_manager.mostrar_datos_en_tablas(
                    datos['datos_crudos'],
                    datos['datos_combinados'],
                    datos['datos_numericos']
                )
                
                # Inicializar proceso secuencial
                self.ui_manager.inicializar_proceso_secuencial(
                    datos['datos_combinados'],  # Paso 1: Vista Excel
                    datos['datos_crudos'],      # Paso 2: Con marcadores
                    datos['datos_numericos']    # Paso 3: Numéricos
                )
                
                # Actualizar lista de archivos con datos procesados
                self.ui_manager.actualizar_lista_archivos(nombre_archivo, datos)
                
                # Mostrar validaciones si están disponibles
                if resultado.get('validacion'):
                    self.ui_manager.mostrar_resultados_validacion(
                        resultado['validacion'], 
                        nombre_archivo
                    )
                
                # Habilitar botón sumatoria si hay múltiples archivos
                total_archivos = len(self.app_controller.archivos_procesados)
                self.ui_manager.habilitar_boton_sumatoria(total_archivos > 1)
                
                # Emitir señal de éxito
                self.archivo_procesado.emit(archivo_path, resultado)
                
                print(f"✅ Archivo procesado exitosamente: {nombre_archivo}")
                
            else:
                # Mostrar error
                error_msg = resultado.get('error', 'Error desconocido')
                QMessageBox.critical(
                    self.ui_manager.main_window,
                    "Error de Procesamiento",
                    f"Error procesando archivo:\n{error_msg}"
                )
                self.error_ocurrido.emit("Procesamiento", error_msg)
            
        except Exception as e:
            print(f"❌ Error procesando archivo: {e}")
            QMessageBox.critical(
                self.ui_manager.main_window,
                "Error",
                f"Error inesperado:\n{str(e)}"
            )
            self.error_ocurrido.emit("Procesamiento", str(e))
    
    def manejar_solicitud_sumatoria(self):
        """Manejar solicitud de cálculo de sumatoria."""
        try:
            print("🎮 Calculando sumatoria...")
            
            # Calcular usando AppController
            resultado = self.app_controller.calcular_sumatoria()
            
            if resultado['exito']:
                # Mostrar sumatoria en UI
                sumatoria = resultado['sumatoria']

                # Mostrar en tabla de sumatoria específica
                self.ui_manager.mostrar_sumatoria_en_tabla(sumatoria)

                # Emitir señal de éxito
                self.sumatoria_calculada.emit(resultado)

                print(f"✅ Sumatoria calculada: {resultado['archivos_incluidos']} archivos")
                
            else:
                # Mostrar error
                error_msg = resultado.get('mensaje', 'Error calculando sumatoria')
                QMessageBox.warning(
                    self.ui_manager.main_window,
                    "Error de Sumatoria",
                    error_msg
                )
                self.error_ocurrido.emit("Sumatoria", error_msg)
            
        except Exception as e:
            print(f"❌ Error en sumatoria: {e}")
            self.error_ocurrido.emit("Sumatoria", str(e))
    
    def manejar_solicitud_exportacion(self, archivo_destino: str = None):
        """
        Manejar solicitud de exportación.
        
        Args:
            archivo_destino: Archivo destino (opcional, se pregunta si no se proporciona)
        """
        try:
            # Si no se proporciona destino, preguntar
            if not archivo_destino:
                archivo_destino, _ = QFileDialog.getSaveFileName(
                    self.ui_manager.main_window,
                    "Guardar resultado",
                    "resultado_sumatoria.xlsx",
                    "Archivos Excel (*.xlsx)"
                )
            
            if archivo_destino:
                print(f"🎮 Exportando a: {archivo_destino}")
                
                # Exportar usando AppController
                resultado = self.app_controller.exportar_a_plantilla(archivo_destino)
                
                if resultado['exito']:
                    QMessageBox.information(
                        self.ui_manager.main_window,
                        "Exportación Exitosa",
                        f"Datos exportados exitosamente a:\n{archivo_destino}"
                    )
                    self.exportacion_completada.emit(archivo_destino, True)
                    
                else:
                    error_msg = resultado.get('mensaje', 'Error en exportación')
                    QMessageBox.critical(
                        self.ui_manager.main_window,
                        "Error de Exportación",
                        error_msg
                    )
                    self.exportacion_completada.emit(archivo_destino, False)
                    self.error_ocurrido.emit("Exportación", error_msg)
            
        except Exception as e:
            print(f"❌ Error en exportación: {e}")
            self.error_ocurrido.emit("Exportación", str(e))
    
    def manejar_cambio_modo(self, nuevo_modo: str):
        """
        Manejar cambio de modo de operación.
        
        Args:
            nuevo_modo: Nuevo modo ('ESCUELAS' o 'ZONAS')
        """
        try:
            print(f"🎮 Cambiando modo a: {nuevo_modo}")
            
            # Cambiar modo en AppController
            exito = self.app_controller.cambiar_modo(nuevo_modo)
            
            if exito:
                # Limpiar interfaz
                self.ui_manager.limpiar_interfaz()
                
                # Reinicializar componentes si es necesario
                self.ui_manager.inicializar_componentes()
                
                print(f"✅ Modo cambiado exitosamente a: {nuevo_modo}")
                
            else:
                QMessageBox.warning(
                    self.ui_manager.main_window,
                    "Error de Configuración",
                    f"No se pudo cambiar al modo: {nuevo_modo}"
                )
            
        except Exception as e:
            print(f"❌ Error cambiando modo: {e}")
            self.error_ocurrido.emit("Cambio de Modo", str(e))
    
    def obtener_estado_eventos(self) -> Dict[str, Any]:
        """
        Obtener estado del manejador de eventos.
        
        Returns:
            dict: Estado de eventos
        """
        return {
            'app_controller_activo': self.app_controller is not None,
            'ui_manager_activo': self.ui_manager is not None,
            'conexiones_configuradas': True
        }
