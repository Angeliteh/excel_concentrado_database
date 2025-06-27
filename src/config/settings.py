import os

# Configuraciones de rutas y archivos (rutas relativas al directorio raíz del proyecto)
def get_project_root():
    """Obtiene la ruta raíz del proyecto de forma segura"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_absolute_path(relative_path):
    """Convierte una ruta relativa a absoluta basada en la raíz del proyecto"""
    return os.path.join(get_project_root(), relative_path)

# ✅ CONFIGURACIÓN LEGACY ELIMINADA - Ahora se usa configuración dinámica por modo

# ✅ CONFIGURACIÓN LEGACY ELIMINADA - Ahora se usa ui_config.py para interfaz

# 🎯 CONFIGURACIÓN POR MODO DE OPERACIÓN
# =====================================

# 🏫 CONFIGURACIÓN MODO ESCUELAS
ESCUELAS_CONFIG = {
    "HOJA_DATOS": "ESC2",
    "RANGO_DATOS": "A5:Z17",
    "RANGO_INYECCION": "H6:Z14",  # ✅ Rango correcto para ZONA
    "HOJA_INYECCION": "ZONA3",  # ✅ Exportar a hoja ZONA 3
    "CONCEPTOS": [
        "INSCRIPCIÓN",
        "BAJAS",
        "EXISTENCIA",
        "ALTAS",
        "APROBADOS",
        "REPROBADOS",
        "BECADOS MUNICIPIO",
        "BECADOS SEED",
        "BIENESTAR",
        "GRUPOS"
    ],
    "PLANTILLA": "FORMATO FIN DE CICLO ZONA.xlsx",  # ✅ Plantilla correcta
    "VALIDACION_COMPLETA": True,
    "CREAR_BACKUP": False  # ✅ No crear backup automático
}

# 🌍 CONFIGURACIÓN MODO ZONAS
ZONAS_CONFIG = {
    "HOJA_DATOS": "ZONA3",
    "RANGO_DATOS": "A3:Z14",
    "RANGO_INYECCION": "H6:Z14",
    "HOJA_INYECCION": "ZONA 3",  # ✅ Hoja específica para inyección
    "CONCEPTOS": [
        "PREINSCRIPCIÓN 1ER. GRADO",
        "INSCRIPCIÓN",
        "BAJAS",
        "EXISTENCIA",
        "ALTAS",
        "BECADOS MUNICIPIO",
        "BECADOS SEED",
        "BIENESTAR",
        "GRUPOS"
    ],
    "PLANTILLA": "FORMATO FIN DE CICLO ZONA.xlsx",  # ✅ Plantilla correcta
    "VALIDACION_COMPLETA": True,
    "CREAR_BACKUP": False  # ✅ No crear backup automático
}

# 🏛️ CONFIGURACIÓN MODO SECTORES
SECTORES_CONFIG = {
    "HOJA_DATOS": "SECTOR3",
    "RANGO_DATOS": "A3:Z14",
    "RANGO_INYECCION": "H6:Z14",
    "CONCEPTOS": [
        "PREINSCRIPCIÓN 1ER. GRADO",
        "INSCRIPCIÓN",
        "BAJAS",
        "EXISTENCIA",
        "ALTAS",
        "BECADOS MUNICIPIO",
        "BECADOS SEED",
        "BIENESTAR",
        "GRUPOS"
    ],
    "PLANTILLA": "FORMATO FIN DE CICLO ZONA.xlsx",
    "VALIDACION_COMPLETA": False  # Solo sumatoria
}

# Variables globales para configuración activa
MODO_ACTUAL = "ZONAS"  # Por defecto
CONFIG_ACTUAL = ZONAS_CONFIG.copy()

def configurar_modo(modo):
    """
    Configurar el sistema para un modo específico.

    Args:
        modo (str): "ESCUELAS", "ZONAS", o "SECTORES"
    """
    global MODO_ACTUAL, CONFIG_ACTUAL

    if modo == "ESCUELAS":
        CONFIG_ACTUAL = ESCUELAS_CONFIG.copy()
    elif modo == "ZONAS":
        CONFIG_ACTUAL = ZONAS_CONFIG.copy()
    elif modo == "SECTORES":
        CONFIG_ACTUAL = SECTORES_CONFIG.copy()
    else:
        raise ValueError(f"Modo no válido: {modo}")

    MODO_ACTUAL = modo
    print(f"🎯 Configuración actualizada para modo: {modo}")
    print(f"   📋 Hoja: {CONFIG_ACTUAL['HOJA_DATOS']}")
    print(f"   📊 Rango: {CONFIG_ACTUAL['RANGO_DATOS']}")
    print(f"   🎯 Conceptos: {len(CONFIG_ACTUAL['CONCEPTOS'])}")

    return CONFIG_ACTUAL

def get_config_actual():
    """Obtener la configuración activa actual."""
    return CONFIG_ACTUAL.copy()