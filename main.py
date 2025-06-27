#!/usr/bin/env python3
"""
🎯 PROCESADOR EXCEL MÚLTIPLE - SISTEMA FINAL MODULAR
====================================================

Sistema modular para procesamiento de múltiples archivos Excel con:
✅ Extracción de datos con marcadores [valor]
✅ Visualización secuencial (3 pasos)
✅ Gestión múltiple de archivos
✅ Sumatoria automática
✅ Exportación a plantilla base

Arquitectura modular refactorizada:
📦 ExcelProcessor: Extracción y procesamiento centralizado
📦 DataManager: Gestión múltiple de archivos
📦 TemplateInjector: Exportación a plantillas
📦 Settings: Configuraciones centralizadas

Uso: python main.py
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from src.controllers.app_controller import AppController
from src.controllers.ui_manager import UIManager
from src.controllers.event_handler import EventHandler
from src.gui.mode_selector import ModeSelector
from src.config.settings import configurar_modo


class ExcelVisualizerApp(QMainWindow):
    """
    Aplicación principal simplificada.

    Coordina controladores especializados sin lógica de negocio.
    """

    def __init__(self):
        super().__init__()

        # Inicializar controladores especializados
        self.app_controller = AppController()
        self.ui_manager = UIManager(self)
        self.event_handler = EventHandler(self.app_controller, self.ui_manager)

        # Variables de compatibilidad (para componentes existentes)
        self.datos_crudos = None
        self.datos_combinados = None
        self.datos_numericos = None
        self.archivo_actual = None
        self.datos_paso1 = None
        self.datos_paso2 = None
        self.datos_paso3 = None
        self.paso_actual = 0
        self.archivo_seleccionado = None
        self.sumatoria_total = None

        # Inicializar interfaz
        self.ui_manager.inicializar_componentes()

        # Configurar conexiones de eventos
        self._configurar_eventos()

        print("🎯 ExcelVisualizerApp inicializada con arquitectura modular")

    def _configurar_eventos(self):
        """Configurar eventos específicos de la aplicación."""
        try:
            # Conectar eventos del event_handler
            self.event_handler.archivo_procesado.connect(self._on_archivo_procesado)
            self.event_handler.sumatoria_calculada.connect(self._on_sumatoria_calculada)
            self.event_handler.exportacion_completada.connect(self._on_exportacion_completada)
            self.event_handler.error_ocurrido.connect(self._on_error_ocurrido)

            print("� Eventos de aplicación configurados")

        except Exception as e:
            print(f"⚠️ Error configurando eventos: {e}")

    def _on_archivo_procesado(self, archivo_path: str, resultado: dict):
        """Callback cuando se procesa un archivo."""
        # Actualizar variables de compatibilidad
        datos = resultado['datos']
        self.datos_crudos = datos['datos_crudos']
        self.datos_combinados = datos['datos_combinados']
        self.datos_numericos = datos['datos_numericos']
        self.archivo_actual = archivo_path

        print(f"📁 Archivo procesado: {resultado['archivo']}")

    def _on_sumatoria_calculada(self, resultado: dict):
        """Callback cuando se calcula la sumatoria."""
        self.sumatoria_total = resultado['sumatoria']
        print(f"🧮 Sumatoria calculada: {resultado['archivos_incluidos']} archivos")

    def _on_exportacion_completada(self, archivo_destino: str, exito: bool):
        """Callback cuando se completa la exportación."""
        if exito:
            print(f"📤 Exportación exitosa: {archivo_destino}")
        else:
            print(f"❌ Error en exportación: {archivo_destino}")

    def _on_error_ocurrido(self, tipo: str, mensaje: str):
        """Callback cuando ocurre un error."""
        print(f"❌ Error en {tipo}: {mensaje}")

    @property
    def archivos_procesados(self):
        """Propiedad para mantener compatibilidad con código existente"""
        return self.app_controller.archivos_procesados

    def procesar_archivo(self, archivo, mostrar_proceso=True):
        """Método de compatibilidad - delegar al event_handler"""
        self.event_handler.procesar_archivo_seleccionado(archivo)

    # Métodos de compatibilidad simplificados
    def extraer_datos(self):
        """Método de compatibilidad - funcionalidad movida a controladores"""
        print("⚠️ extraer_datos() es obsoleto - usar event_handler")
        pass

    def mostrar_datos(self):
        """Método de compatibilidad - funcionalidad movida a ui_manager"""
        print("⚠️ mostrar_datos() es obsoleto - usar ui_manager")
        pass

    def inicializar_proceso_secuencial(self):
        """Método de compatibilidad - funcionalidad movida a ui_manager"""
        print("⚠️ inicializar_proceso_secuencial() es obsoleto - usar ui_manager")
        pass


def main():
    """
    Función principal simplificada.

    Solo maneja inicialización básica y delegación a controladores.
    """
    try:
        # Inicializar aplicación PyQt
        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        # Selector de modo
        modo_seleccionado = ModeSelector.get_selected_mode()
        if modo_seleccionado is None:
            print("❌ No se seleccionó ningún modo. Cerrando aplicación.")
            return

        # Configurar modo seleccionado
        configurar_modo(modo_seleccionado)
        print(f"🎯 Modo configurado: {modo_seleccionado}")

        # Crear y mostrar ventana principal
        window = ExcelVisualizerApp()
        window.show()

        # Ejecutar aplicación
        print("🚀 Aplicación iniciada exitosamente")
        sys.exit(app.exec_())

    except Exception as e:
        print(f"❌ Error crítico en main(): {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
