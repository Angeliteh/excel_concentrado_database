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
        Procesa una tabla específica siguiendo exactamente la lógica del script antiguo
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
            
            # Seleccionar rango numérico y mostrar para depuración
            rango_datos = df.iloc[min_row - 2 : max_row - 1, min_col - 1 : max_col].copy()
            
            # Convertir a numérico y manejar NaN
            rango_datos = rango_datos.apply(pd.to_numeric, errors='coerce').fillna(0)
            
            # Depuración al estilo del script antiguo
            print(f"\nRango seleccionado del DataFrame para {nombre_tabla}:")
            print(rango_datos.to_string())
            print("\nDimensiones del DataFrame:", rango_datos.shape)
            
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
