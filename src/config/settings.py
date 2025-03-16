# Configuraciones de rutas y archivos
RUTA_PLANTILLA = "plantilla_base.xlsx"
RUTA_SALIDA_DEFAULT = "archivo_consolidado.xlsx"

# Configuraciones de Excel
RANGOS_EXCEL = {
    'tabla_1': {
        'rango_completo': (3, 1, 14, 26),
        'rango_sumatoria': (3, 8, 11, 26),
        'rango_inyeccion': (6, 8, 14, 26)
    },
    'tabla_2': {
        'rango_completo': (16, 13, 22, 25),
        'rango_sumatoria': (4, 3, 6, 13),
        'rango_inyeccion': (20, 15, 22, 25)
    }
}

NOMBRE_HOJAS = {
    'entrada': 'ZONA3',
    'salida': 'SECTOR3'
}

# Configuración de fórmulas
FORMULAS_CONFIG = {
    'totales': {
        'inicio': 6,
        'fin': 13
    }
}

# Configuración de base de datos
DB_CONFIG = {
    'nombre': 'datos_escolares.db'
}