import sys
import os
import pandas as pd
import numpy as np

# Agregar el directorio raíz al path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from src.utils.excel_utils import extraer_tabla_y_limpiar, cargar_excel

def limpiar_y_estructurar_datos(df):
    """Limpia y estructura los datos para que se parezcan al Excel original"""
    # Obtener el título
    titulo = df.iloc[0, 0]
    
    # Crear estructura de columnas correcta
    columnas = []
    for grado in ['1o.', '2o.', '3o.', '4o.', '5o.', '6o.']:
        columnas.extend([f'{grado}_H', f'{grado}_M'])
    columnas.extend(['SUBTOTAL_H', 'SUBTOTAL_M', 'TOTAL'])
    
    # Extraer conceptos y datos
    conceptos = [
        'PREINSCRIPCIÓN 1ER. GRADO', 'INSCRIPCIÓN', 'BAJAS', 'EXISTENCIA',
        'ALTAS', 'BECADOS MUNICIPIO', 'BECADOS SEED', 'BIENESTAR', 'GRUPOS'
    ]
    
    # Mapeo de columnas del DataFrame original a las columnas deseadas
    mapeo_columnas = {
        '1o._H': 7,    '1o._M': 8,
        '2o._H': 9,    '2o._M': 10,
        '3o._H': 11,   '3o._M': 12,
        '4o._H': 13,   '4o._M': 14,
        '5o._H': 15,   '5o._M': 16,
        '6o._H': 17,   '6o._M': 18,
        'SUBTOTAL_H': 19, 'SUBTOTAL_M': 20,
        'TOTAL': 21
    }
    
    # Llenar datos
    datos_finales = []
    for concepto in conceptos:
        fila = df[df.iloc[:, 0] == concepto]
        if len(fila) > 0:
            fila = fila.iloc[0]
            valores = []
            
            # Extraer valores usando el mapeo
            for columna in columnas:
                idx = mapeo_columnas.get(columna)
                if idx is not None and idx < len(fila):
                    valor = fila[idx]
                    valores.append(valor if pd.notna(valor) else 0)
                else:
                    valores.append(0)
            
            datos_finales.append([concepto] + valores)
    
    # Crear DataFrame con las columnas correctas
    datos_limpios = pd.DataFrame(datos_finales, columns=['CONCEPTO'] + columnas)
    
    # Debug info
    print(f"Número de columnas en datos_finales: {len(datos_finales[0]) if datos_finales else 0}")
    print(f"Número de columnas definidas: {len(['CONCEPTO'] + columnas)}")
    print(f"Columnas en datos_limpios: {datos_limpios.columns.tolist()}")
    
    return titulo, datos_limpios

def normalizar_datos_movimiento(df):
    """
    Normaliza los datos de movimiento de alumnos para formato de base de datos
    """
    datos_normalizados = []
    
    for _, row in df.iterrows():
        concepto = row['CONCEPTO']
        
        # Iterar sobre cada grado y género
        for grado in ['1o.', '2o.', '3o.', '4o.', '5o.', '6o.']:
            # Procesar datos para hombres
            valor_h = row[f'{grado}_H']
            datos_normalizados.append({
                'grado': grado,
                'genero': 'H',
                'concepto': concepto,
                'valor': valor_h,
                'tipo': 'MOVIMIENTO'
            })
            
            # Procesar datos para mujeres
            valor_m = row[f'{grado}_M']
            datos_normalizados.append({
                'grado': grado,
                'genero': 'M',
                'concepto': concepto,
                'valor': valor_m,
                'tipo': 'MOVIMIENTO'
            })
    
    return pd.DataFrame(datos_normalizados)

def probar_extraccion(archivo_excel):
    try:
        # Cargar y extraer datos
        hoja = cargar_excel(archivo_excel, 'ZONA3')
        rango_tabla = (3, 1, 15, 26)
        tabla_cruda = extraer_tabla_y_limpiar(hoja, rango_tabla)
        df = pd.DataFrame(tabla_cruda)

        print("Forma del DataFrame original:", df.shape)
        print("Primeras columnas del DataFrame original:", df.columns.tolist()[:5])
        
        # Limpiar y estructurar datos
        titulo, datos_limpios = limpiar_y_estructurar_datos(df)
        
        # Mostrar resultados de forma legible
        print("\n" + "="*80)
        print(f"TÍTULO: {titulo}")
        print("="*80)
        
        # Configurar opciones de visualización
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_rows', None)
        
        print("\nDATOS ESTRUCTURADOS:")
        print(datos_limpios.to_string(index=False))
        
        # Normalizar datos
        print("\nDATOS NORMALIZADOS:")
        datos_normalizados = normalizar_datos_movimiento(datos_limpios)
        print(datos_normalizados.to_string(index=False))
        
        # Guardar ambos formatos
        datos_limpios.to_excel("datos_extraidos_original.xlsx", index=False)
        datos_normalizados.to_excel("datos_normalizados.xlsx", index=False)
        
        return datos_limpios, datos_normalizados
        
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        raise

# Ejecutar la prueba
archivo_prueba = "C:\\Users\\Angel\\Desktop\\esucela_prueba -2.xlsx"
df_original, df_normalizado = probar_extraccion(archivo_prueba)
