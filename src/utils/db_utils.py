import pandas as pd
import sqlite3
import os
from ..config.settings import DB_CONFIG

def get_db_connection():
    """Establece una conexión con la base de datos"""
    # Asegurarse de que la base de datos existe
    if not os.path.exists(DB_CONFIG['database']):
        crear_tabla_inicial()
    return sqlite3.connect(DB_CONFIG['database'])

def crear_tabla_inicial():
    """Crea las tablas necesarias si no existen"""
    conn = sqlite3.connect(DB_CONFIG['database'])
    cursor = conn.cursor()
    
    # Tabla principal para datos de movimiento de alumnos (tabla 1)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datos_alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        archivo TEXT,
        grado TEXT,
        genero TEXT,
        concepto TEXT,
        valor REAL,
        tipo_registro TEXT DEFAULT 'MOVIMIENTO',
        fecha_proceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Tabla para datos de periodos (tabla 2)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datos_periodos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        archivo TEXT,
        grado TEXT,
        periodo TEXT,
        genero TEXT,
        valor REAL,
        tipo_registro TEXT DEFAULT 'PERIODO',
        fecha_proceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    print("Base de datos y tablas creadas correctamente")

def ejecutar_consulta(query):
    """
    Ejecuta una consulta SQL y devuelve los resultados como DataFrame
    """
    try:
        # Verificar si las tablas existen antes de ejecutar la consulta
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('datos_alumnos', 'datos_periodos')
            """)
            if not cursor.fetchall():
                raise Exception("Las tablas de datos no existen")
            
            return pd.read_sql_query(query, conn)
    except Exception as e:
        raise Exception(f"Error al ejecutar consulta: {str(e)}")

def obtener_tablas():
    """
    Obtiene la lista de tablas en la base de datos
    """
    query = """
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        raise Exception(f"Error al obtener tablas: {str(e)}")

def obtener_columnas(tabla):
    """
    Obtiene la lista de columnas de una tabla específica
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({tabla})")
            return [row[1] for row in cursor.fetchall()]
    except Exception as e:
        raise Exception(f"Error al obtener columnas: {str(e)}")

def procesar_archivos_db(archivos, config):
    """
    Procesa los archivos Excel y los guarda en la base de datos
    """
    try:
        from ..utils.excel_utils import extraer_tabla_y_limpiar, cargar_excel
        
        for archivo in archivos:
            print(f"\n{'='*50}")
            print(f"Extrayendo tablas de: {archivo}")
            print(f"{'='*50}")
            
            hoja = cargar_excel(archivo, 'ZONA3')
            
            # Extraer tabla 1
            rango_tabla1 = (3, 1, 14, 26)
            tabla1_cruda = extraer_tabla_y_limpiar(hoja, rango_tabla1)
            df_tabla1 = pd.DataFrame(tabla1_cruda)
            
            # Limpiar columnas repetidas
            # Nos quedamos solo con la primera fila para los encabezados
            encabezados = df_tabla1.iloc[0]
            # Eliminamos columnas duplicadas manteniendo la primera ocurrencia
            columnas_unicas = ~encabezados.duplicated()
            df_tabla1_limpia = df_tabla1.loc[:, columnas_unicas]
            
            print("\nTabla 1 después de eliminar duplicados:")
            print(df_tabla1_limpia.to_string())
            
            # Verificar estructura
            print("\nEncabezados únicos:")
            print(df_tabla1_limpia.columns.tolist())
            print("\nPrimeras filas de datos:")
            print(df_tabla1_limpia.iloc[1:5])  # Mostrar algunas filas de ejemplo

    except Exception as e:
        raise Exception(f"Error procesando tablas: {str(e)}")

def verificar_tabla():
    """
    Verifica si las tablas existen y muestra su estructura
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        tablas = ['datos_alumnos', 'datos_periodos']
        for tabla in tablas:
            # Verificar si la tabla existe
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """, (tabla,))
            
            if cursor.fetchone():
                print(f"\nLa tabla {tabla} existe")
                
                # Mostrar estructura de la tabla
                cursor.execute(f"PRAGMA table_info({tabla})")
                columnas = cursor.fetchall()
                print("\nEstructura de la tabla:")
                for col in columnas:
                    print(f"- {col[1]} ({col[2]})")
                
                # Mostrar cantidad de registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                total = cursor.fetchone()[0]
                print(f"\nTotal de registros: {total}")
            else:
                print(f"\nLa tabla {tabla} NO existe")
        
        conn.close()
    except Exception as e:
        print(f"Error al verificar las tablas: {str(e)}")
