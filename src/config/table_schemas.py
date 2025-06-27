"""
📋 TABLE SCHEMAS - Esquemas de Tablas Dinámicos
===============================================

Configuración centralizada y completamente dinámica de todas las estructuras de tablas.
Elimina TODO hardcodeo del sistema.

PRINCIPIOS:
✅ Configuración única: un solo lugar para todos los esquemas
✅ Completamente dinámico: sin valores hardcodeados
✅ Extensible: fácil agregar nuevos tipos de tabla
✅ Validable: esquemas auto-documentados
✅ Reutilizable: funciona con cualquier estructura similar
"""

from typing import Dict, List, Any


# 📊 ESQUEMAS DE TABLAS PRINCIPALES
TABLE_SCHEMAS = {
    
    # 🏫 TABLA DE MOVIMIENTO DE ALUMNOS (ESC2)
    "ESC2_MOVIMIENTOS": {
        "descripcion": "Tabla de movimiento de alumnos por grados y géneros",
        "hoja_default": "ESC2",
        "rango_datos": "A5:Z17",
        "rango_numerico": "H6:Z16",
        
        "estructura": {
            # Filas de headers
            "fila_titulo": 0,           # "MOVIMIENTO DE ALUMNOS"
            "fila_grados": 1,           # "1O.", "2O.", "3O.", etc.
            "fila_generos": 2,          # "H", "M", "H", "M", etc.
            
            # Filas de datos (conceptos)
            "filas_conceptos": {
                "inicio": 3,
                "fin": 12,
                "mapeo": {
                    3: "INSCRIPCIÓN",
                    4: "BAJAS", 
                    5: "EXISTENCIA",
                    6: "ALTAS",
                    7: "APROBADOS",
                    8: "REPROBADOS", 
                    9: "BECADOS MUNICIPIO",
                    10: "BECADOS SEED",
                    11: "BIENESTAR",
                    12: "GRUPOS"
                }
            },
            
            # Columnas de datos
            "columnas_grados": {
                "inicio": 7,            # Columna H (índice 7)
                "fin": 18,              # Hasta columna S
                "patron": "H_M",        # Alternado H, M, H, M...
                "grados": ["1O", "2O", "3O", "4O", "5O", "6O"]
            },
            
            # Columnas de subtotales
            "columnas_subtotales": {
                "H": 19,                # Columna T (subtotal hombres)
                "M": 21                 # Columna V (subtotal mujeres)
            },
            
            # Columnas de totales
            "columnas_totales": {
                "inicio": 23,           # Columna X
                "fin": 25               # Columna Z
            }
        },
        
        "validaciones": {
            "subtotales_H": {
                "formula": "suma(H_1O + H_2O + H_3O + H_4O + H_5O + H_6O)",
                "columna_resultado": 19
            },
            "subtotales_M": {
                "formula": "suma(M_1O + M_2O + M_3O + M_4O + M_5O + M_6O)", 
                "columna_resultado": 21
            },
            "totales": {
                "formula": "subtotal_H + subtotal_M",
                "columna_resultado": 23
            },
            "coherencia": {
                "EXISTENCIA": "INSCRIPCIÓN - BAJAS"
            }
        },
        
        "conceptos_especiales": {
            "GRUPOS": {
                "tipo": "suma_directa",
                "descripcion": "No tiene subtotales H/M, suma directa de celdas"
            }
        }
    },
    
    # 📚 TABLA DE GRUPOS POR GRADO (ESC1)
    "ESC1_GRUPOS": {
        "descripcion": "Tabla de grupos por grado (1A, 1B, 1C, etc.)",
        "hoja_default": "ESC1",
        "rango_datos": "A3:Z15",
        "rango_numerico": "H4:Z14",
        
        "estructura": {
            # Filas de headers
            "fila_titulo": 0,           # "GRUPOS POR GRADO"
            "fila_grados": 1,           # "1ER GRADO", "2DO GRADO", etc.
            "fila_grupos": 2,           # "A", "B", "C", "A", "B", "C", etc.
            
            # Filas de datos
            "filas_datos": {
                "inicio": 3,
                "fin": 14,
                "mapeo": {
                    3: "HOMBRES",
                    4: "MUJERES",
                    5: "TOTAL_GRUPO"
                }
            },
            
            # Columnas por grado y grupo
            "columnas_grupos": {
                "inicio": 7,            # Columna H
                "fin": 25,              # Columna Z
                "estructura": {
                    "1ER_GRADO": {
                        "grupos": ["A", "B", "C"],
                        "columnas": [7, 8, 9]       # H, I, J
                    },
                    "2DO_GRADO": {
                        "grupos": ["A", "B", "C"],
                        "columnas": [10, 11, 12]    # K, L, M
                    },
                    "3ER_GRADO": {
                        "grupos": ["A", "B", "C"],
                        "columnas": [13, 14, 15]    # N, O, P
                    },
                    "4TO_GRADO": {
                        "grupos": ["A", "B", "C"],
                        "columnas": [16, 17, 18]    # Q, R, S
                    },
                    "5TO_GRADO": {
                        "grupos": ["A", "B", "C"],
                        "columnas": [19, 20, 21]    # T, U, V
                    },
                    "6TO_GRADO": {
                        "grupos": ["A", "B", "C"],
                        "columnas": [22, 23, 24]    # W, X, Y
                    }
                }
            },

            # ✅ Configuración de inyección para ESC2 → ZONA 3
            "rango_inyeccion": {
                "fila_inicio": 6,      # H6
                "columna_inicio": 8,   # Columna H (índice 8)
                "columna_fin": 26,     # Columna Z (índice 26)
                "hoja_destino": "ZONA 3",  # ✅ Exportar a hoja ZONA 3
                "celdas_combinadas": {
                    "X_Z_combinadas": True,  # X y Z están combinadas
                    "rango_combinado": "X6:Z14"  # Rango de celdas combinadas
                }
            }
        },

        "validaciones": {
            "total_por_grupo": {
                "formula": "HOMBRES + MUJERES",
                "fila_resultado": 5
            },
            "coherencia_con_esc2": {
                "descripcion": "Total por grado debe coincidir con EXISTENCIA en ESC2"
            }
        }
    },
    
    # 🌍 TABLA ZONA (ZONA3)
    "ZONA3_CONCENTRADO": {
        "descripcion": "Tabla concentrada de zona (suma de escuelas)",
        "hoja_default": "ZONA3", 
        "rango_datos": "A3:Z14",
        "rango_numerico": "H4:Z13",
        
        "estructura": {
            # Hereda estructura de ESC2 pero con diferentes rangos
            "base": "ESC2_MOVIMIENTOS",
            "diferencias": {
                "rango_datos": "A3:Z14",
                "filas_conceptos": {
                    "inicio": 2,
                    "fin": 11,
                    "mapeo": {
                        2: "PREINSCRIPCIÓN 1ER. GRADO",
                        3: "INSCRIPCIÓN",
                        4: "BAJAS",
                        5: "EXISTENCIA", 
                        6: "ALTAS",
                        7: "BECADOS MUNICIPIO",
                        8: "BECADOS SEED",
                        9: "BIENESTAR",
                        10: "GRUPOS"
                    }
                }
            },

            # ✅ Configuración de inyección específica para ZONA3
            "rango_inyeccion": {
                "fila_inicio": 6,      # H6
                "columna_inicio": 8,   # Columna H (índice 8)
                "columna_fin": 26,     # Columna Z (índice 26)
                "hoja_destino": "ZONA 3",  # ✅ Hoja específica con espacio
                "celdas_combinadas": {
                    "X_Z_combinadas": True,  # X y Z están combinadas
                    "rango_combinado": "X6:Z14"  # Rango de celdas combinadas
                }
            }
        }
    },
    
    # 🏛️ TABLA SECTOR (SECTOR3)
    "SECTOR3_CONCENTRADO": {
        "descripcion": "Tabla concentrada de sector (suma de zonas)",
        "hoja_default": "SECTOR3",
        "rango_datos": "A3:Z14", 
        "rango_numerico": "H4:Z13",
        
        "estructura": {
            # Hereda estructura de ZONA3
            "base": "ZONA3_CONCENTRADO",
            "diferencias": {
                "hoja_default": "SECTOR3"
            }
        }
    }
}


# 🎯 CONFIGURACIONES POR MODO
MODE_CONFIGS = {
    "ESCUELAS": {
        "tabla_principal": "ESC2_MOVIMIENTOS",
        "tabla_secundaria": "ESC1_GRUPOS",
        "validacion_cruzada": True,
        "validacion_completa": True,
        "plantilla": "FORMATO FIN DE CICLO ESCUELA.xlsx",  # ✅ Plantilla correcta
        "hoja_inyeccion": "ESC2",  # ✅ Hoja específica
        "rango_inyeccion": "H6:Z15"
    },
    
    "ZONAS": {
        "tabla_principal": "ZONA3_CONCENTRADO",
        "validacion_cruzada": False,
        "validacion_completa": True,
        "plantilla": "FORMATO FIN DE CICLO ZONA.xlsx",  # ✅ Plantilla correcta
        "hoja_inyeccion": "ZONA 3",  # ✅ Hoja específica
        "rango_inyeccion": "H6:Z14"  # ✅ Rango correcto (X-Z combinadas)
    },
    
    "SECTORES": {
        "tabla_principal": "SECTOR3_CONCENTRADO",
        "validacion_cruzada": False,
        "validacion_completa": False,  # Solo sumatoria
        "plantilla": "FORMATO FIN DE CICLO ZONA.xlsx",
        "rango_inyeccion": "H6:Z14"
    }
}


# 🔍 ESQUEMAS DE VALIDACIÓN
VALIDATION_SCHEMAS = {
    "SUBTOTALES": {
        "descripcion": "Validación de subtotales H y M",
        "aplicable_a": ["ESC2_MOVIMIENTOS", "ZONA3_CONCENTRADO", "SECTOR3_CONCENTRADO"],
        "conceptos_excluidos": ["GRUPOS"]  # GRUPOS no tiene subtotales
    },
    
    "TOTALES": {
        "descripcion": "Validación de totales (H + M)",
        "aplicable_a": ["ESC2_MOVIMIENTOS", "ZONA3_CONCENTRADO", "SECTOR3_CONCENTRADO"],
        "formula_normal": "subtotal_H + subtotal_M",
        "formula_grupos": "suma_directa_celdas"
    },
    
    "COHERENCIA_INTERNA": {
        "descripcion": "Validación de coherencia entre filas",
        "aplicable_a": ["ESC2_MOVIMIENTOS", "ZONA3_CONCENTRADO", "SECTOR3_CONCENTRADO"],
        "reglas": {
            "EXISTENCIA": "INSCRIPCIÓN - BAJAS"
        }
    },
    
    "COHERENCIA_CRUZADA": {
        "descripcion": "Validación entre hojas ESC1 y ESC2",
        "aplicable_a": ["ESCUELAS"],
        "reglas": {
            "EXISTENCIA_VS_GRUPOS": "suma_grupos_por_grado == existencia_por_grado"
        }
    }
}


# 🛠️ FUNCIONES DE UTILIDAD
def get_table_schema(schema_name: str) -> Dict[str, Any]:
    """
    Obtener esquema de tabla por nombre.
    
    Args:
        schema_name: Nombre del esquema
        
    Returns:
        Diccionario con esquema completo
    """
    if schema_name not in TABLE_SCHEMAS:
        raise ValueError(f"Esquema '{schema_name}' no encontrado")
    
    schema = TABLE_SCHEMAS[schema_name].copy()
    
    # Resolver herencia si existe
    if "estructura" in schema and "base" in schema["estructura"]:
        base_schema = TABLE_SCHEMAS[schema["estructura"]["base"]]
        
        # Combinar esquema base con diferencias
        schema_final = base_schema.copy()
        if "diferencias" in schema["estructura"]:
            schema_final.update(schema["estructura"]["diferencias"])
        
        schema["estructura"] = schema_final["estructura"]
    
    return schema


def get_mode_config(mode: str) -> Dict[str, Any]:
    """
    Obtener configuración por modo.
    
    Args:
        mode: Modo ("ESCUELAS", "ZONAS", "SECTORES")
        
    Returns:
        Diccionario con configuración del modo
    """
    if mode not in MODE_CONFIGS:
        raise ValueError(f"Modo '{mode}' no encontrado")
    
    config = MODE_CONFIGS[mode].copy()
    
    # Agregar esquema de tabla principal
    tabla_principal = config["tabla_principal"]
    config["esquema_tabla"] = get_table_schema(tabla_principal)
    
    # Agregar esquema de tabla secundaria si existe
    if "tabla_secundaria" in config:
        tabla_secundaria = config["tabla_secundaria"]
        config["esquema_tabla_secundaria"] = get_table_schema(tabla_secundaria)
    
    return config


def get_validation_schema(validation_type: str) -> Dict[str, Any]:
    """
    Obtener esquema de validación por tipo.
    
    Args:
        validation_type: Tipo de validación
        
    Returns:
        Diccionario con esquema de validación
    """
    if validation_type not in VALIDATION_SCHEMAS:
        raise ValueError(f"Esquema de validación '{validation_type}' no encontrado")
    
    return VALIDATION_SCHEMAS[validation_type].copy()


def list_available_schemas() -> Dict[str, List[str]]:
    """
    Listar todos los esquemas disponibles.
    
    Returns:
        Diccionario con listas de esquemas por categoría
    """
    return {
        "table_schemas": list(TABLE_SCHEMAS.keys()),
        "mode_configs": list(MODE_CONFIGS.keys()),
        "validation_schemas": list(VALIDATION_SCHEMAS.keys())
    }


def validate_schema_compatibility(schema1: str, schema2: str) -> bool:
    """
    Validar si dos esquemas son compatibles para validación cruzada.
    
    Args:
        schema1: Nombre del primer esquema
        schema2: Nombre del segundo esquema
        
    Returns:
        True si son compatibles
    """
    # Implementación básica - se puede extender
    compatible_pairs = [
        ("ESC1_GRUPOS", "ESC2_MOVIMIENTOS"),
        ("ESC2_MOVIMIENTOS", "ESC1_GRUPOS")
    ]
    
    return (schema1, schema2) in compatible_pairs
