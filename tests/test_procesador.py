import unittest
from src.procesador.procesador import ProcesadorDatosEscolares
import pandas as pd
import os

class TestProcesador(unittest.TestCase):
    def setUp(self):
        self.procesador = ProcesadorDatosEscolares()
        self.datos_prueba = {
            'movimiento_alumnos': pd.DataFrame({
                'col1': [1, 2],
                'col2': [3, 4]
            }),
            'aprovechamiento': pd.DataFrame({
                'col1': [5, 6],
                'col2': [7, 8]
            })
        }

    def test_normalizar_datos(self):
        resultado = self.procesador.normalizar_datos(self.datos_prueba)
        self.assertIsInstance(resultado, dict)
        self.assertEqual(len(resultado), len(self.datos_prueba))

    def test_consolidar_datos(self):
        datos_nuevos = {
            'movimiento_alumnos': pd.DataFrame({
                'col1': [2, 3],
                'col2': [4, 5]
            })
        }
        datos_base = self.datos_prueba.copy()
        self.procesador._consolidar_datos(datos_base, datos_nuevos)
        self.assertEqual(
            datos_base['movimiento_alumnos'].iloc[0]['col1'],
            self.datos_prueba['movimiento_alumnos'].iloc[0]['col1'] + 
            datos_nuevos['movimiento_alumnos'].iloc[0]['col1']
        )

    def test_procesar_archivo_individual(self):
        archivo_test = os.path.join("tests", "data", "test_input.xlsx")
        if not os.path.exists(archivo_test):
            self.skipTest(f"Archivo de prueba {archivo_test} no encontrado")
        
        resultado = self.procesador.procesar_archivo_individual(archivo_test)
        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)

if __name__ == '__main__':
    unittest.main()