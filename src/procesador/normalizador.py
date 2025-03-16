import pandas as pd
from ..config.settings import DB_CONFIG

class NormalizadorDatosEscolares:
    def __init__(self):
        self.reglas_normalizacion = {
            'tabla_1': self._normalizar_movimiento_alumnos,
            'tabla_2': self._normalizar_periodos_proceso
        }
        
        # Diccionario de mapeo para estandarizar grados
        self.mapeo_grados = {
            '1o': '1RO',
            '2o': '2DO',
            '3o': '3RO',
            '4o': '4TO',
            '5o': '5TO',
            '6o': '6TO'
        }

        # Mapeo de conceptos según aparecen en Excel
        self.conceptos_excel = {
            0: 'PREINSCRIPCIÓN 1ER. GRADO',
            1: 'INSCRIPCIÓN',
            2: 'BAJAS',
            3: 'EXISTENCIA',
            4: 'ALTAS',
            5: 'BECADOS MUNICIPIO',
            6: 'BECADOS SEED',
            7: 'BIENESTAR',
            8: 'GRUPOS'
        }

    def normalizar(self, tablas):
        """
        Normaliza las tablas manteniendo consistencia entre conceptos compartidos
        """
        datos_normalizados = {}
        
        # Primero normalizamos la tabla de movimiento_alumnos para establecer los grados base
        if 'tabla_1' in tablas:
            datos_normalizados['tabla_1'] = self._normalizar_movimiento_alumnos(tablas['tabla_1'])
            grados_base = datos_normalizados['tabla_1']['grado'].unique()
        
        # Normalizamos la tabla de periodos usando los mismos grados como referencia
        if 'tabla_2' in tablas:
            datos_normalizados['tabla_2'] = self._normalizar_periodos_proceso(
                tablas['tabla_2'], 
                grados_base
            )
        
        return datos_normalizados

    def _estandarizar_grado(self, grado):
        """
        Estandariza el formato de los grados entre tablas
        """
        grado_limpio = grado.split('.')[0].strip()
        return self.mapeo_grados.get(grado_limpio, grado_limpio)

    def _normalizar_movimiento_alumnos(self, df):
        datos_normalizados = []
        
        # Convertir el índice de columnas a lista para poder usar posiciones numéricas
        columnas = df.columns.tolist()
        
        for col in columnas:
            # Obtener la posición numérica de la columna
            col_index = columnas.index(col)
            
            # Determinar género basado en la posición (par/impar)
            genero = 'H' if col_index % 2 == 0 else 'M'
            
            # Obtener el grado del nombre de la columna
            grado = None
            for grado_original, grado_normalizado in self.mapeo_grados.items():
                if grado_original in str(col).upper():
                    grado = grado_normalizado
                    break
            
            if grado:
                # Procesar los datos para esta columna
                for concepto_id, concepto_nombre in self.conceptos_excel.items():
                    valor = df[col].iloc[concepto_id]
                    
                    datos_normalizados.append({
                        'grado': grado,
                        'genero': genero,
                        'concepto': concepto_nombre,
                        'valor': valor
                    })
        
        return pd.DataFrame(datos_normalizados)

    def _normalizar_periodos_proceso(self, df, grados_base=None):
        """
        Normaliza la tabla de periodos manteniendo consistencia con los grados de movimiento_alumnos
        """
        datos_normalizados = []
        
        for idx, row in df.iterrows():
            grado_actual = self._estandarizar_grado(str(idx))
            
            for col in df.columns:
                if col not in ['id', 'grado']:
                    periodo = col.split('_')[0]
                    genero = 'H' if col.endswith('H') else 'M' if col.endswith('M') else ''
                    
                    datos_normalizados.append({
                        'grado': grado_actual,
                        'periodo': periodo,
                        'genero': genero,
                        'valor': row[col],
                        'tipo_registro': 'PERIODO'
                    })
        
        return pd.DataFrame(datos_normalizados)
    
