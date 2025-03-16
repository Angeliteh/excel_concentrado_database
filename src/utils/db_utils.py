from openpyxl import load_workbook
import pandas as pd
from ..config.settings import RANGOS_EXCEL, NOMBRE_HOJAS, FORMULAS_CONFIG, RUTA_PLANTILLA
from ..utils.excel_utils import (
    extraer_tabla_y_limpiar,
    cargar_excel,
    inyectar_datos_en_plantilla,
    inyectar_formulas_totales_y_subtotales,
    convertir_formulas_a_valores
)

class ProcesadorDatosEscolares:
    def __init__(self):
        self.rangos = {
            'tabla_1': {
                'rango_completo': (3, 1, 14, 26),        # rango tabla 1 (A3:Z14)
                'rango_sumatoria': (3, 8, 11, 26),       # rango de sumatorias tabla 1 (H3:Z11)
                'rango_inyeccion': (6, 8, 14, 26)        # rango de reinyección (H6:Z14)
            },
            'tabla_2': {
                'rango_completo': (16, 13, 22, 25),      # rango tabla 2 (M16:Y22)
                'rango_sumatoria': (4, 3, 6, 13),        # rango de sumatorias tabla 2
                'rango_inyeccion': (20, 15, 22, 25)      # rango de reinyección (O20:Y22)
            }
        }
        self.hojas = {
            'entrada': 'ZONA3',
            'salida': 'SECTOR3'
        }

    def procesar_archivos(self, archivos):
        """
        Procesa múltiples archivos Excel y consolida sus datos
        """
        datos_consolidados = {
            'tabla_1': None,
            'tabla_2': None
        }

        for archivo in archivos:
            datos = self.procesar_archivo_individual(archivo)
            
            # Consolidar datos
            for tabla in ['tabla_1', 'tabla_2']:
                if datos_consolidados[tabla] is None:
                    datos_consolidados[tabla] = datos[tabla]
                else:
                    datos_consolidados[tabla] += datos[tabla]

        return datos_consolidados

    def procesar_archivo_individual(self, archivo_excel):
        """
        Procesa un archivo Excel individual
        """
        try:
            hoja = cargar_excel(archivo_excel, self.hojas['entrada'])
            
            datos = {
                'tabla_1': self._procesar_tabla(hoja, 'tabla_1'),
                'tabla_2': self._procesar_tabla(hoja, 'tabla_2')
            }
            
            return datos
        except Exception as e:
            raise Exception(f"Error procesando archivo {archivo_excel}: {str(e)}")

    def _procesar_tabla(self, hoja, nombre_tabla):
        """
        Procesa una tabla específica manteniendo el formato original de celdas combinadas
        """
        try:
            # Extraer tabla completa
            rango_tabla = self.rangos[nombre_tabla]['rango_completo']
            tabla = extraer_tabla_y_limpiar(hoja, rango_tabla)
            df = pd.DataFrame(tabla)
            
            # Obtener encabezados y renombrar columnas
            encabezados = df.iloc[1]
            df.columns = encabezados
            df = df.iloc[2:].reset_index(drop=True)
            
            # Obtener rango de sumatoria
            rango_suma = self.rangos[nombre_tabla]['rango_sumatoria']
            min_row, min_col, max_row, max_col = rango_suma
            
            # Seleccionar rango numérico
            rango_datos = df.iloc[min_row - 2 : max_row - 1, min_col - 1 : max_col].copy()
            
            # Convertir a numérico y manejar NaN
            rango_datos = rango_datos.apply(pd.to_numeric, errors='coerce')
            rango_datos = rango_datos.fillna(0)
            
            # Manejar columnas especiales (SUBTOTAL y TOTAL)
            for col in rango_datos.columns:
                if 'SUBTOTAL' in str(col) or 'TOTAL' in str(col):
                    # Asegurarse de que solo haya un valor por fila
                    rango_datos[col] = rango_datos[col].apply(lambda x: x if x != 0 else None)
                    rango_datos[col] = rango_datos[col].fillna(method='ffill')
            
            return rango_datos

        except Exception as e:
            raise Exception(f"Error procesando tabla {nombre_tabla}: {str(e)}")

    def guardar_resultados(self, datos, archivo_salida):
        """
        Guarda los resultados siguiendo el proceso del script antiguo
        """
        try:
            wb = load_workbook(RUTA_PLANTILLA)
            hoja = wb[self.hojas['salida']]

            # Inyectar datos siguiendo el proceso antiguo
            for nombre_tabla in ['tabla_1', 'tabla_2']:
                rango_inyeccion = self.rangos[nombre_tabla]['rango_inyeccion']
                df = datos[nombre_tabla]
                inyectar_datos_en_plantilla(df, hoja, rango_inyeccion)

            wb.save(archivo_salida)

            # Aplicar fórmulas como en el script antiguo
            inyectar_formulas_totales_y_subtotales(
                archivo_salida,
                self.hojas['salida'],
                fila_inicial=6,
                fila_final=13
            )
            convertir_formulas_a_valores(archivo_salida)

        except Exception as e:
            raise Exception(f"Error al guardar resultados: {str(e)}")

def obtener_suma_movimientos(conexion):
    """
    Obtiene sumas consolidadas manteniendo la estructura de las tablas originales
    """
    queries = {
        'movimiento_alumnos': """
            SELECT 
                grado,
                genero,
                SUM(valor) as total,
                tipo_registro
            FROM datos_escolares
            WHERE tipo_registro = 'MOVIMIENTO'
            GROUP BY grado, genero
            ORDER BY 
                grado,
                genero
        """,
        
        'periodos_proceso': """
            SELECT 
                grado,
                periodo,
                genero,
                SUM(valor) as total
            FROM datos_escolares
            WHERE tipo_registro = 'PERIODO'
            GROUP BY grado, periodo, genero
            ORDER BY 
                grado,
                periodo,
                genero
        """
    }
    
    resultados = {}
    for nombre, query in queries.items():
        resultados[nombre] = pd.read_sql_query(query, conexion)
    
    return resultados

def reconstruir_formato_original(datos_normalizados, tipo_tabla):
    """
    Reconstruye el formato de tabla original desde los datos normalizados
    """
    if tipo_tabla == 'tabla_1':
        # Pivotear para obtener formato original de movimiento_alumnos
        return datos_normalizados.pivot_table(
            index='concepto',
            columns=['grado', 'genero'],
            values='valor',
            aggfunc='sum'
        )
    elif tipo_tabla == 'tabla_2':
        # Pivotear para obtener formato original de periodos_proceso
        return datos_normalizados.pivot_table(
            index='grado',
            columns=['periodo', 'genero'],
            values='valor',
            aggfunc='sum'
        )

def crear_tablas(conexion):
    """
    Crea la estructura de tablas necesaria para el sistema
    """
    queries = [
        """
        CREATE TABLE IF NOT EXISTS conceptos (
            id_concepto INTEGER PRIMARY KEY,
            nombre_concepto TEXT NOT NULL,
            descripcion TEXT,
            tipo_concepto TEXT CHECK(tipo_concepto IN ('INSCRIPCION', 'BECA', 'OPERATIVO'))
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS grados (
            id_grado INTEGER PRIMARY KEY,
            nombre_grado TEXT NOT NULL,
            nivel TEXT DEFAULT 'PRIMARIA'
        )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS movimiento_alumnos (
            id_movimiento INTEGER PRIMARY KEY,
            id_concepto INTEGER,
            id_grado INTEGER,
            genero TEXT CHECK(genero IN ('H', 'M')),
            cantidad INTEGER DEFAULT 0,
            periodo_escolar TEXT,
            fecha_registro DATE,
            FOREIGN KEY (id_concepto) REFERENCES conceptos(id_concepto),
            FOREIGN KEY (id_grado) REFERENCES grados(id_grado)
        )
        """
    ]
    
    for query in queries:
        conexion.execute(query)
    
    # Insertar conceptos base
    conceptos_base = [
        (1, 'PREINSCRIPCIÓN 1ER. GRADO', 'Alumnos preinscritos para primer grado', 'INSCRIPCION'),
        (2, 'INSCRIPCIÓN', 'Alumnos inscritos', 'INSCRIPCION'),
        (3, 'BAJAS', 'Alumnos dados de baja', 'OPERATIVO'),
        (4, 'EXISTENCIA', 'Total de alumnos existentes', 'OPERATIVO'),
        (5, 'ALTAS', 'Alumnos dados de alta', 'OPERATIVO'),
        (6, 'BECADOS MUNICIPIO', 'Alumnos con beca municipal', 'BECA'),
        (7, 'BECADOS SEED', 'Alumnos con beca SEED', 'BECA'),
        (8, 'BIENESTAR', 'Alumnos en programa bienestar', 'BECA'),
        (9, 'GRUPOS', 'Cantidad de grupos', 'OPERATIVO')
    ]
    
    conexion.executemany(
        "INSERT OR IGNORE INTO conceptos (id_concepto, nombre_concepto, descripcion, tipo_concepto) VALUES (?, ?, ?, ?)",
        conceptos_base
    )

def obtener_resumen_movimientos(conexion, periodo=None):
    """
    Obtiene el resumen de movimientos por concepto y grado
    """
    query = """
    SELECT 
        c.nombre_concepto,
        g.nombre_grado,
        SUM(CASE WHEN m.genero = 'H' THEN m.cantidad ELSE 0 END) as total_hombres,
        SUM(CASE WHEN m.genero = 'M' THEN m.cantidad ELSE 0 END) as total_mujeres,
        SUM(m.cantidad) as total
    FROM movimiento_alumnos m
    JOIN conceptos c ON m.id_concepto = c.id_concepto
    JOIN grados g ON m.id_grado = g.id_grado
    WHERE (:periodo IS NULL OR m.periodo_escolar = :periodo)
    GROUP BY c.nombre_concepto, g.nombre_grado
    ORDER BY c.id_concepto, g.id_grado
    """
    
    return pd.read_sql_query(
        query, 
        conexion, 
        params={'periodo': periodo}
    )

def insertar_movimiento(conexion, concepto, grado, genero, cantidad, periodo):
    """
    Inserta un nuevo registro de movimiento
    """
    query = """
    INSERT INTO movimiento_alumnos 
    (id_concepto, id_grado, genero, cantidad, periodo_escolar, fecha_registro)
    VALUES (
        (SELECT id_concepto FROM conceptos WHERE nombre_concepto = ?),
        (SELECT id_grado FROM grados WHERE nombre_grado = ?),
        ?, ?, ?, DATE('now')
    )
    """
    
    conexion.execute(query, (concepto, grado, genero, cantidad, periodo))
    conexion.commit()

def imprimir_tabla_formato_original(conexion, periodo=None):
    """
    Imprime las tablas en el formato original para verificación
    """
    # Obtener datos de movimiento_alumnos
    query_movimientos = """
    SELECT 
        c.nombre_concepto,
        g.nombre_grado,
        SUM(CASE WHEN m.genero = 'H' THEN m.cantidad ELSE 0 END) as H,
        SUM(CASE WHEN m.genero = 'M' THEN m.cantidad ELSE 0 END) as M
    FROM movimiento_alumnos m
    JOIN conceptos c ON m.id_concepto = c.id_concepto
    JOIN grados g ON m.id_grado = g.id_grado
    WHERE (:periodo IS NULL OR m.periodo_escolar = :periodo)
    GROUP BY c.nombre_concepto, g.nombre_grado
    ORDER BY c.id_concepto, g.id_grado
    """
    
    df_movimientos = pd.read_sql_query(
        query_movimientos, 
        conexion, 
        params={'periodo': periodo}
    )

    # Pivotear para obtener el formato original
    df_pivot = df_movimientos.pivot(
        index='nombre_concepto',
        columns='nombre_grado'
    )

    # Imprimir encabezado
    print("\nGRADOS")
    print("CONCEPTO")
    
    # Imprimir cada concepto con sus valores
    for concepto in df_pivot.index:
        print(f"\n{concepto}")
        row = df_pivot.loc[concepto]
        for grado in df_pivot.columns.levels[1]:
            h_value = row[('H', grado)]
            m_value = row[('M', grado)]
            print(f"{grado}: H={h_value}, M={m_value}", end=' | ')
        print()  # Nueva línea después de cada concepto

def verificar_datos(archivos, periodo):
    """
    Procesa archivos Excel, guarda en BD y verifica mostrando el formato original
    """
    from ..procesador.procesador import ProcesadorDatosEscolares
    from ..procesador.normalizador import NormalizadorDatosEscolares
    import sqlite3
    
    # Inicializar procesadores
    procesador = ProcesadorDatosEscolares()
    normalizador = NormalizadorDatosEscolares()
    
    # Procesar archivos
    datos_consolidados = procesador.procesar_archivos(archivos)
    
    # Normalizar datos
    datos_normalizados = normalizador.normalizar(datos_consolidados)
    
    # Conectar a la BD y guardar datos
    with sqlite3.connect('datos_escolares.db') as conexion:
        # Asegurarse que las tablas existen
        crear_tablas(conexion)
        
        # Guardar datos normalizados
        for concepto, datos in datos_normalizados['tabla_1'].iterrows():
            insertar_movimiento(
                conexion,
                concepto,
                datos['grado'],
                datos['genero'],
                datos['cantidad'],
                periodo
            )
        
        # Imprimir para verificación
        print("\n=== Datos guardados en la BD ===")
        imprimir_tabla_formato_original(conexion, periodo)

# Eliminar la ejecución directa al final del archivo
if __name__ == "__main__":
    # Solo mantener como ejemplo de uso, no ejecutar directamente
    pass
