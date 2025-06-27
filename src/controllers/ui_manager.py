"""
🎨 UI MANAGER - Gestor de Interfaz Gráfica
==========================================

Controlador especializado en gestión de interfaz gráfica.
Separa completamente la lógica de UI de la lógica de negocio.

RESPONSABILIDADES:
✅ Inicialización de componentes UI
✅ Configuración de estilos y temas
✅ Gestión de tabs y tablas
✅ Actualización de elementos visuales
✅ Coordinación entre componentes GUI
✅ Sin lógica de negocio
"""

from typing import Dict, Any, Optional
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal

from ..gui.table_visualizer import TableVisualizer
from ..gui.sequential_process import SequentialProcess
from ..gui.main_window_ui import MainWindowUI
from ..gui.file_manager import FileManager
from ..gui.data_processor import DataProcessor
from ..gui.validation_details_window import ValidationDetailsWindow
from ..config.ui_config import UIConfig


class UIManager(QObject):
    """
    Gestor de interfaz gráfica.

    Coordina todos los componentes de UI sin mezclarse con lógica de negocio.
    """

    # Señales para comunicación con otros controladores
    archivo_seleccionado = pyqtSignal(str)
    sumatoria_solicitada = pyqtSignal()
    exportacion_solicitada = pyqtSignal(str)
    validacion_solicitada = pyqtSignal(str)

    def __init__(self, main_window: QMainWindow):
        """
        Inicializar gestor de UI.

        Args:
            main_window: Ventana principal de la aplicación
        """
        super().__init__()
        self.main_window = main_window
        self.ui_config = UIConfig()
        
        # Componentes de UI
        self.table_visualizer = None
        self.sequential_process = None
        self.main_window_ui = None
        self.file_manager = None
        self.data_processor = None
        
        # Estado de UI
        self.tabs_inicializados = False
        self.validaciones_visibles = False
        
        print("🎨 UIManager inicializado")
    
    def inicializar_componentes(self):
        """Inicializar todos los componentes de UI."""
        try:
            print("🎨 Inicializando componentes de UI...")

            # PRIMERO: Crear componentes especializados
            self.table_visualizer = TableVisualizer(self.main_window)
            self.sequential_process = SequentialProcess(self.main_window)
            self.file_manager = FileManager(self.main_window)
            self.data_processor = DataProcessor(self.main_window)

            # Asignar componentes a la ventana principal ANTES de init_ui
            self.main_window.table_visualizer = self.table_visualizer
            self.main_window.sequential_process = self.sequential_process
            self.main_window.file_manager = self.file_manager
            self.main_window.data_processor = self.data_processor

            # DESPUÉS: Inicializar UI principal (ahora que los componentes existen)
            self.main_window_ui = MainWindowUI(self.main_window)
            self.main_window_ui.init_ui()

            # Configurar conexiones de señales
            self._configurar_conexiones()

            # Configurar conexiones de botones
            self._configurar_botones()

            self.tabs_inicializados = True
            print("✅ Componentes de UI inicializados")

        except Exception as e:
            print(f"❌ Error inicializando UI: {e}")
            QMessageBox.critical(
                self.main_window,
                "Error de Inicialización",
                f"Error inicializando interfaz:\n{str(e)}"
            )
    
    def _configurar_conexiones(self):
        """Configurar conexiones entre componentes de UI."""
        try:
            # Conectar señales del file_manager
            if hasattr(self.file_manager, 'archivo_seleccionado'):
                self.file_manager.archivo_seleccionado.connect(
                    self.archivo_seleccionado.emit
                )
            
            # Conectar señales del data_processor
            if hasattr(self.data_processor, 'sumatoria_solicitada'):
                self.data_processor.sumatoria_solicitada.connect(
                    self.sumatoria_solicitada.emit
                )
            
            print("🔗 Conexiones de UI configuradas")
            
        except Exception as e:
            print(f"⚠️ Error configurando conexiones: {e}")

    def _configurar_botones(self):
        """Configurar conexiones de botones."""
        try:
            # Conectar botón de sumatoria
            if hasattr(self.main_window, 'btn_calcular_suma'):
                self.main_window.btn_calcular_suma.clicked.connect(
                    self.sumatoria_solicitada.emit
                )
                print("🔘 Botón de sumatoria conectado")

            # Conectar otros botones si es necesario
            # TODO: Agregar más botones según se necesiten

        except Exception as e:
            print(f"⚠️ Error configurando botones: {e}")

    def mostrar_datos_en_tablas(self, datos_crudos, datos_combinados, datos_numericos):
        """
        Mostrar datos en las tres tablas principales.

        Args:
            datos_crudos: Datos con marcadores [valor]
            datos_combinados: Datos combinados (vista Excel)
            datos_numericos: Datos numéricos puros
        """
        try:
            print("🎨 Mostrando datos en tablas...")

            if not self.table_visualizer:
                print("❌ TableVisualizer no inicializado")
                return

            # Validar que los datos no sean None
            if datos_crudos is None or datos_combinados is None or datos_numericos is None:
                print("❌ Datos faltantes para mostrar en tablas")
                return

            # Obtener configuración de headers desde UI config
            headers_config = self.ui_config.get_headers_config()
            headers_completos = headers_config.get('excel_columns', [chr(65 + i) for i in range(26)])
            headers_numericos = headers_config.get('numeric_columns', [chr(72 + i) for i in range(19)])
            
            # Mostrar en cada tabla (verificar que existan)
            if hasattr(self.main_window, 'table_marcadores'):
                self.table_visualizer.llenar_tabla(
                    self.main_window.table_marcadores,
                    datos_crudos,
                    headers_completos,
                    "Vista con Marcadores"
                )

            if hasattr(self.main_window, 'table_combinada'):
                self.table_visualizer.llenar_tabla(
                    self.main_window.table_combinada,
                    datos_combinados,
                    headers_completos,
                    "Vista Combinada"
                )

            if hasattr(self.main_window, 'table_numericos'):
                self.table_visualizer.llenar_tabla(
                    self.main_window.table_numericos,
                    datos_numericos,
                    headers_numericos,
                    "Datos Numéricos"
                )
            else:
                print("⚠️ Tablas principales no encontradas, usando tabla de proceso")
            
            print("✅ Datos mostrados en tablas")
            
        except Exception as e:
            print(f"❌ Error mostrando datos: {e}")
    
    def inicializar_proceso_secuencial(self, datos_paso1, datos_paso2, datos_paso3):
        """
        Inicializar el proceso secuencial de 3 pasos.

        Args:
            datos_paso1: Datos para paso 1 (vista Excel)
            datos_paso2: Datos para paso 2 (con marcadores)
            datos_paso3: Datos para paso 3 (numéricos)
        """
        try:
            print("🎨 Inicializando proceso secuencial...")

            if not self.sequential_process:
                print("❌ SequentialProcess no inicializado")
                return

            # Validar que los datos no sean None
            if datos_paso1 is None or datos_paso2 is None or datos_paso3 is None:
                print("❌ Datos faltantes para proceso secuencial")
                return

            # Preparar datos en el componente secuencial Y en la ventana principal
            self.main_window.datos_paso1 = datos_paso1
            self.main_window.datos_paso2 = datos_paso2
            self.main_window.datos_paso3 = datos_paso3

            # TAMBIÉN asegurar que los datos base estén disponibles
            self.main_window.datos_combinados = datos_paso1
            self.main_window.datos_crudos = datos_paso2
            self.main_window.datos_numericos = datos_paso3

            # Habilitar botones si existen
            if hasattr(self.main_window, 'btn_paso1'):
                self.main_window.btn_paso1.setEnabled(True)
            if hasattr(self.main_window, 'btn_paso2'):
                self.main_window.btn_paso2.setEnabled(True)
            if hasattr(self.main_window, 'btn_paso3'):
                self.main_window.btn_paso3.setEnabled(True)

            # Empezar en Paso 1
            self.sequential_process.mostrar_paso(1)

            print("✅ Proceso secuencial inicializado")

        except Exception as e:
            print(f"❌ Error inicializando proceso secuencial: {e}")
    
    def actualizar_lista_archivos(self, nombre_archivo: str, datos_procesados: dict = None):
        """
        Actualizar la lista de archivos en la interfaz.

        Args:
            nombre_archivo: Nombre del archivo a agregar
            datos_procesados: Datos procesados del archivo (opcional)
        """
        try:
            if self.file_manager and hasattr(self.file_manager, 'agregar_archivo_a_lista'):
                # Si tenemos datos procesados, pasarlos al file_manager
                if datos_procesados:
                    self.file_manager.agregar_archivo_a_lista_con_datos(nombre_archivo, datos_procesados)
                else:
                    # Fallback al método original (puede fallar)
                    self.file_manager.agregar_archivo_a_lista(nombre_archivo)
                print(f"📁 Archivo agregado a lista: {nombre_archivo}")
            else:
                print("⚠️ FileManager no disponible para actualizar lista")

        except Exception as e:
            print(f"❌ Error actualizando lista: {e}")
    
    def habilitar_boton_sumatoria(self, habilitar: bool):
        """
        Habilitar o deshabilitar el botón de sumatoria.
        
        Args:
            habilitar: True para habilitar, False para deshabilitar
        """
        try:
            if hasattr(self.main_window, 'btn_calcular_suma'):
                self.main_window.btn_calcular_suma.setEnabled(habilitar)
                print(f"🔘 Botón sumatoria {'habilitado' if habilitar else 'deshabilitado'}")
            
        except Exception as e:
            print(f"❌ Error configurando botón: {e}")

    def mostrar_resultados_validacion(self, reporte: Dict[str, Any], nombre_archivo: str):
        """
        Mostrar resultados de validación en la interfaz.

        Args:
            reporte: Reporte de validación
            nombre_archivo: Nombre del archivo validado
        """
        try:
            total_discrepancias = reporte.get('total_discrepancias', 0)
            total_exitosas = reporte.get('total_validaciones_exitosas', 0)

            # SIEMPRE mostrar panel de validaciones
            if hasattr(self.main_window, 'grupo_validaciones'):
                self.main_window.grupo_validaciones.setVisible(True)
                self.validaciones_visibles = True

                # Configurar estilo según resultado
                if total_discrepancias > 0:
                    self._aplicar_estilo_validacion_error()
                    self.main_window.grupo_validaciones.setTitle("⚠️ VALIDACIONES - DISCREPANCIAS ENCONTRADAS")
                else:
                    self._aplicar_estilo_validacion_exito()
                    self.main_window.grupo_validaciones.setTitle("✅ VALIDACIONES - TODO CORRECTO")

                # Actualizar texto del resumen
                resumen = f"📁 {nombre_archivo}\n{reporte.get('resumen', 'Sin resumen disponible')}"
                if hasattr(self.main_window, 'label_validaciones'):
                    self.main_window.label_validaciones.setText(resumen)

                # Configurar botón de detalles
                self._configurar_boton_detalles(reporte, nombre_archivo)

            print(f"🎨 Resultados de validación mostrados para {nombre_archivo}")

        except Exception as e:
            print(f"❌ Error mostrando validación: {e}")

    def _aplicar_estilo_validacion_error(self):
        """Aplicar estilo de error a panel de validaciones."""
        estilo_error = """
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #d32f2f;
                border: 2px solid #f44336;
                border-radius: 6px;
                margin-top: 5px;
                padding-top: 5px;
                background-color: #ffebee;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px 0 6px;
                background-color: white;
            }
        """
        if hasattr(self.main_window, 'grupo_validaciones'):
            self.main_window.grupo_validaciones.setStyleSheet(estilo_error)

    def _aplicar_estilo_validacion_exito(self):
        """Aplicar estilo de éxito a panel de validaciones."""
        estilo_exito = """
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #2e7d32;
                border: 2px solid #4caf50;
                border-radius: 6px;
                margin-top: 5px;
                padding-top: 5px;
                background-color: #e8f5e9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px 0 6px;
                background-color: white;
            }
        """
        if hasattr(self.main_window, 'grupo_validaciones'):
            self.main_window.grupo_validaciones.setStyleSheet(estilo_exito)

    def _configurar_boton_detalles(self, reporte: Dict[str, Any], nombre_archivo: str):
        """
        Configurar botón de detalles de validación.

        Args:
            reporte: Reporte de validación
            nombre_archivo: Nombre del archivo
        """
        try:
            if hasattr(self.main_window, 'btn_ver_validaciones'):
                # Desconectar conexiones previas
                try:
                    self.main_window.btn_ver_validaciones.clicked.disconnect()
                except:
                    pass

                # Conectar nueva función
                self.main_window.btn_ver_validaciones.clicked.connect(
                    lambda checked, r=reporte, n=nombre_archivo: self._mostrar_detalles_validacion(r, n)
                )

        except Exception as e:
            print(f"⚠️ Error configurando botón detalles: {e}")

    def _mostrar_detalles_validacion(self, reporte: Dict[str, Any], nombre_archivo: str):
        """
        Mostrar detalles completos de validación en ventana dedicada.

        Args:
            reporte: Reporte de validación
            nombre_archivo: Nombre del archivo
        """
        try:
            ventana_detalles = ValidationDetailsWindow(reporte, nombre_archivo, self.main_window)
            ventana_detalles.exec_()

        except Exception as e:
            print(f"❌ Error mostrando detalles: {e}")

    def obtener_estado_ui(self) -> Dict[str, Any]:
        """
        Obtener estado actual de la interfaz.

        Returns:
            dict: Estado de la UI
        """
        return {
            'tabs_inicializados': self.tabs_inicializados,
            'validaciones_visibles': self.validaciones_visibles,
            'componentes_activos': {
                'table_visualizer': self.table_visualizer is not None,
                'sequential_process': self.sequential_process is not None,
                'main_window_ui': self.main_window_ui is not None,
                'file_manager': self.file_manager is not None,
                'data_processor': self.data_processor is not None
            }
        }

    def seleccionar_archivo_desde_lista(self, nombre_archivo: str, app_controller):
        """
        Manejar selección de archivo desde la lista.

        Args:
            nombre_archivo: Nombre del archivo seleccionado
            app_controller: Controlador de aplicación para obtener datos
        """
        try:
            print(f"🎨 Seleccionando archivo: {nombre_archivo}")

            # Obtener datos del AppController
            datos_archivo = app_controller.obtener_datos_archivo(nombre_archivo)

            if not datos_archivo:
                print(f"❌ No se encontraron datos para: {nombre_archivo}")
                return

            # Extraer datos de la estructura correcta
            datos = datos_archivo.get('datos', {})

            if not datos:
                print(f"❌ No se encontraron datos procesados para: {nombre_archivo}")
                return

            # Verificar que todos los datos necesarios estén presentes
            required_keys = ['datos_crudos', 'datos_combinados', 'datos_numericos']
            missing_keys = [key for key in required_keys if key not in datos]

            if missing_keys:
                print(f"❌ Faltan datos requeridos: {missing_keys}")
                return

            # Actualizar datos en la ventana principal
            self.main_window.datos_crudos = datos['datos_crudos']
            self.main_window.datos_combinados = datos['datos_combinados']
            self.main_window.datos_numericos = datos['datos_numericos']
            self.main_window.archivo_seleccionado = nombre_archivo

            if 'mapeo_posicional' in datos:
                self.main_window.mapeo_posicional = datos['mapeo_posicional']

            # Mostrar datos en tablas
            self.mostrar_datos_en_tablas(
                datos['datos_crudos'],
                datos['datos_combinados'],
                datos['datos_numericos']
            )

            # Inicializar proceso secuencial
            self.inicializar_proceso_secuencial(
                datos['datos_combinados'],  # Paso 1
                datos['datos_crudos'],      # Paso 2
                datos['datos_numericos']    # Paso 3
            )

            # ACTUALIZAR VALIDACIONES del archivo seleccionado
            validacion = datos_archivo.get('validacion')
            if validacion:
                self.mostrar_resultados_validacion(validacion, nombre_archivo)
                print(f"🔍 Validaciones actualizadas para: {nombre_archivo}")
            else:
                # Si no hay validaciones, ocultar panel
                if hasattr(self.main_window, 'grupo_validaciones'):
                    self.main_window.grupo_validaciones.setVisible(False)
                    self.validaciones_visibles = False
                print(f"⚠️ No hay validaciones para: {nombre_archivo}")

            # Actualizar título
            if hasattr(self.main_window, 'label_paso'):
                self.main_window.label_paso.setText(f"📁 {nombre_archivo} - Selecciona un paso para visualizar")

            print(f"✅ Archivo seleccionado: {nombre_archivo}")

        except Exception as e:
            print(f"❌ Error seleccionando archivo: {e}")

    def mostrar_sumatoria_en_tabla(self, sumatoria_data):
        """
        Mostrar sumatoria en la tabla correspondiente.

        Args:
            sumatoria_data: Datos de la sumatoria calculada
        """
        try:
            print("🎨 Mostrando sumatoria en tabla...")

            if not hasattr(self.main_window, 'tabla_sumatoria'):
                print("⚠️ Tabla de sumatoria no encontrada")
                return

            # Usar DataProcessor para mostrar la sumatoria
            if self.data_processor and hasattr(self.data_processor, 'mostrar_sumatoria_total'):
                # Actualizar datos en la ventana principal
                self.main_window.sumatoria_total = sumatoria_data

                # Mostrar usando el método existente
                self.data_processor.mostrar_sumatoria_total()

                # Mostrar grupo de sumatoria
                if hasattr(self.main_window, 'grupo_sumatoria'):
                    self.main_window.grupo_sumatoria.setVisible(True)

                # Habilitar botón de exportar
                if hasattr(self.main_window, 'btn_exportar'):
                    self.main_window.btn_exportar.setEnabled(True)

                print("✅ Sumatoria mostrada en tabla")
            else:
                print("⚠️ DataProcessor no disponible para mostrar sumatoria")

        except Exception as e:
            print(f"❌ Error mostrando sumatoria: {e}")

    def limpiar_interfaz(self):
        """Limpiar elementos de la interfaz."""
        try:
            # Ocultar validaciones
            if hasattr(self.main_window, 'grupo_validaciones'):
                self.main_window.grupo_validaciones.setVisible(False)
                self.validaciones_visibles = False

            # Limpiar listas
            if self.file_manager:
                self.file_manager.limpiar_lista()

            # Deshabilitar botones
            if hasattr(self.main_window, 'btn_calcular_suma'):
                self.main_window.btn_calcular_suma.setEnabled(False)

            print("🧹 Interfaz limpiada")

        except Exception as e:
            print(f"❌ Error limpiando interfaz: {e}")
