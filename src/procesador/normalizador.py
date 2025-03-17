import pandas as pd
from ..config.settings import DB_CONFIG

class NormalizadorDatosEscolares:
    def __init__(self):
        # Mapeos exactos como aparecen en el Excel
        self.mapeo_grados = {
            '1o.': '1RO',
            '2o.': '2DO',
            '3o.': '3RO',
            '4o.': '4TO',
            '5o.': '5TO',
            '6o.': '6TO'
        }

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
        Normaliza las tablas manteniendo consistencia con el formato original
        """
        print("\n=== Iniciando proceso de normalización ===")
        datos_normalizados = {}
        
        if 'tabla_1' in tablas:
            print("\nProcesando tabla de movimiento_alumnos:")
            datos_normalizados['tabla_1'] = self._normalizar_movimiento_alumnos(tablas['tabla_1'])
            print(f"Registros normalizados: {len(datos_normalizados['tabla_1'])}")
        
        if 'tabla_2' in tablas:
            print("\nProcesando tabla de periodos:")
            datos_normalizados['tabla_2'] = self._normalizar_periodos_proceso(tablas['tabla_2'])
            print(f"Registros normalizados: {len(datos_normalizados['tabla_2'])}")
        
        return datos_normalizados

    def _normalizar_movimiento_alumnos(self, df):
        """
        Normaliza la tabla de movimiento_alumnos siguiendo el formato original
        """
        datos_normalizados = []
        print("\nNormalizando datos por concepto y grado:")
        
        # Procesar cada concepto
        for concepto_id, concepto_nombre in self.conceptos_excel.items():
            for grado in self.mapeo_grados.keys():
                # Obtener índices de columnas H/M según el formato original
                idx_base = list(self.mapeo_grados.keys()).index(grado) * 2
                col_h = idx_base + 1  # Columna Hombres
                col_m = idx_base + 2  # Columna Mujeres
                
                # Extraer valores asegurando que sean numéricos
                valor_h = float(df.iloc[concepto_id, col_h]) if concepto_id < len(df) else 0
                valor_m = float(df.iloc[concepto_id, col_m]) if concepto_id < len(df) else 0
                
                grado_norm = self.mapeo_grados[grado]
                
                # Registrar datos normalizados
                datos_normalizados.extend([
                    {
                        'grado': grado_norm,
                        'genero': 'H',
                        'concepto': concepto_nombre,
                        'valor': valor_h,
                        'tipo': 'MOVIMIENTO'
                    },
                    {
                        'grado': grado_norm,
                        'genero': 'M',
                        'concepto': concepto_nombre,
                        'valor': valor_m,
                        'tipo': 'MOVIMIENTO'
                    }
                ])
                
                print(f"  {grado_norm} - {concepto_nombre}: H={valor_h}, M={valor_m}")
        
        return pd.DataFrame(datos_normalizados)

    def _normalizar_periodos_proceso(self, df):
        """
        Normaliza la tabla de periodos manteniendo el formato original
        """
        datos_normalizados = []
        periodos = ['PRIM MOM', 'SEGUNDO MOMENTO']
        tipos_escritura = ['Presilábico', 'Silábico', 'Silábico/Alfabético', 'Alfabético']
        
        print("\nNormalizando datos de periodos:")
        for grado in ['1RO', '2DO']:  # Solo primero y segundo grado
            for periodo in periodos:
                for tipo in tipos_escritura:
                    # Calcular índices según el formato original
                    idx_grado = ['1RO', '2DO'].index(grado)
                    idx_periodo = periodos.index(periodo)
                    idx_tipo = tipos_escritura.index(tipo)
                    
                    # Calcular posición en el DataFrame original
                    fila_base = idx_grado * 4 + idx_tipo
                    col_base = idx_periodo * 2
                    
                    # Extraer valores
                    valor_h = float(df.iloc[fila_base, col_base])
                    valor_m = float(df.iloc[fila_base, col_base + 1])
                    
                    datos_normalizados.extend([
                        {
                            'grado': grado,
                            'periodo': periodo,
                            'tipo_escritura': tipo,
                            'genero': 'H',
                            'valor': valor_h,
                            'tipo_registro': 'PERIODO'
                        },
                        {
                            'grado': grado,
                            'periodo': periodo,
                            'tipo_escritura': tipo,
                            'genero': 'M',
                            'valor': valor_m,
                            'tipo_registro': 'PERIODO'
                        }
                    ])
                    
                    print(f"  {grado} - {periodo} - {tipo}: H={valor_h}, M={valor_m}")
        
        return pd.DataFrame(datos_normalizados)