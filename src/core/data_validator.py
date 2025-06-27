"""
🔍 VALIDADOR DE DATOS INTERNOS
============================

Módulo especializado para validar la coherencia interna de las tablas de datos.
Detecta discrepancias en cálculos manuales sin ser invasivo.

FUNCIONALIDADES:
✅ Validación de subtotales y totales
✅ Verificación de coherencia entre filas (Existencia = Inscripción - Bajas)
✅ Detección automática de estructura de tabla
✅ Reportes de discrepancias no invasivos

FILOSOFÍA:
🎯 Solo alertar, nunca modificar
📊 Validar lógica matemática interna
⚠️ Ayudar a detectar errores humanos
🔄 Integración transparente con el flujo existente
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from ..config.settings import get_config_actual
from ..config.table_schemas import get_table_schema


class DataValidator:
    """
    Validador de coherencia interna de datos de tablas educativas.
    
    Detecta automáticamente la estructura y valida cálculos internos.
    """
    
    def __init__(self):
        """Inicializar validador de datos con configuración modular."""
        self.discrepancias = []
        self.validaciones_exitosas = []
        self.estructura_detectada = {}

        # Configuración dinámica
        self.config_actual = get_config_actual()
        self.modo_actual = self.config_actual.get('MODO', 'ESCUELAS')

        # Cargar esquema de validación según el modo
        self.esquema_validacion = self._cargar_esquema_validacion()

        print(f"🔍 DataValidator inicializado - Modo: {self.modo_actual}")

    def _cargar_esquema_validacion(self):
        """
        Cargar esquema de validación según el modo actual.

        Returns:
            dict: Esquema de validación con reglas específicas
        """
        try:
            if self.modo_actual == 'ESCUELAS':
                esquema = get_table_schema("ESC2_MOVIMIENTOS")
            elif self.modo_actual == 'ZONAS':
                esquema = get_table_schema("ZONA3_MOVIMIENTOS")
            else:
                esquema = get_table_schema("ESC2_MOVIMIENTOS")  # Fallback

            # Extraer reglas de validación del esquema
            validaciones = esquema.get('validaciones', {})

            print(f"✅ Esquema de validación cargado para {self.modo_actual}")
            return validaciones

        except Exception as e:
            print(f"⚠️ Error cargando esquema de validación: {e}")
            # Fallback a validaciones por defecto
            return {
                'subtotales': True,
                'totales': True,
                'coherencia_filas': True,
                'rangos_validos': True
            }

    def validar_multiples_hojas(self, datos_hojas):
        """
        Validar datos de múltiples hojas con validaciones cruzadas.

        Args:
            datos_hojas: Dict con datos de múltiples hojas
                {
                    "ESC1": {datos_numericos, datos_crudos, tipo, config},
                    "ESC2": {datos_numericos, datos_crudos, tipo, config}
                }

        Returns:
            dict: Reporte de validación completo con validaciones cruzadas
        """
        print("🔍 Iniciando validación de múltiples hojas...")

        reporte_completo = {
            'validaciones_por_hoja': {},
            'validaciones_cruzadas': {},
            'resumen': {
                'hojas_validadas': 0,
                'total_discrepancias': 0,
                'validaciones_exitosas': 0
            }
        }

        # Validar cada hoja individualmente
        for nombre_hoja, datos_hoja in datos_hojas.items():
            if 'error' not in datos_hoja:
                print(f"🔍 Validando hoja: {nombre_hoja}")

                reporte_hoja = self.validar_tabla_completa(
                    datos_hoja['datos_numericos'],
                    datos_hoja['datos_crudos']
                )

                reporte_completo['validaciones_por_hoja'][nombre_hoja] = reporte_hoja
                reporte_completo['resumen']['hojas_validadas'] += 1
                reporte_completo['resumen']['total_discrepancias'] += len(reporte_hoja.get('discrepancias', []))
                reporte_completo['resumen']['validaciones_exitosas'] += len(reporte_hoja.get('validaciones_exitosas', []))

        # Validaciones cruzadas (preparado para ESC1 vs ESC2)
        if len(datos_hojas) > 1:
            reporte_completo['validaciones_cruzadas'] = self._validar_coherencia_cruzada(datos_hojas)

        print(f"✅ Validación múltiples hojas completada: {reporte_completo['resumen']}")
        return reporte_completo

    def _validar_coherencia_cruzada(self, datos_hojas):
        """
        Validar coherencia entre múltiples hojas (ESC1 vs ESC2).

        Args:
            datos_hojas: Dict con datos de múltiples hojas

        Returns:
            dict: Resultados de validaciones cruzadas
        """
        validaciones_cruzadas = {
            'coherencia_grupos_movimientos': [],
            'consistencia_totales': [],
            'alertas_cruzadas': []
        }

        # Preparado para validaciones específicas ESC1 vs ESC2
        if 'ESC1' in datos_hojas and 'ESC2' in datos_hojas:
            # Aquí se implementarían validaciones específicas como:
            # - Comparar totales de grupos vs movimientos
            # - Verificar coherencia de datos entre hojas
            # - Detectar inconsistencias cruzadas

            validaciones_cruzadas['alertas_cruzadas'].append({
                'tipo': 'info',
                'mensaje': 'Validaciones cruzadas ESC1 vs ESC2 preparadas para implementación futura'
            })

        return validaciones_cruzadas

    def validar_tabla_completa(self, datos_numericos: pd.DataFrame, datos_crudos: pd.DataFrame) -> Dict:
        """
        Validar toda la tabla y retornar reporte de discrepancias.
        
        Args:
            datos_numericos: DataFrame con solo números extraídos
            datos_crudos: DataFrame original con estructura completa
            
        Returns:
            Dict con reporte de validación
        """
        print("🔍 Iniciando validación completa de tabla...")
        
        # Limpiar resultados anteriores
        self.discrepancias = []
        self.validaciones_exitosas = []
        
        # 1. Detectar estructura de la tabla
        self._detectar_estructura_tabla(datos_crudos)
        
        # 2. Validar subtotales y totales
        self._validar_subtotales_totales(datos_numericos)
        
        # 3. Validar totales (suma de subtotales H + M)
        self._validar_totales(datos_numericos)

        # 4. Validar coherencia entre filas
        self._validar_coherencia_filas(datos_numericos)

        # 5. Generar reporte final
        reporte = self._generar_reporte()
        
        print(f"✅ Validación completada: {len(self.discrepancias)} discrepancias encontradas")
        return reporte
    
    def _detectar_estructura_tabla(self, datos_crudos: pd.DataFrame):
        """
        Detectar automáticamente la estructura de la tabla usando datos del Paso 2.

        Analiza la tabla con marcadores [valor] para identificar estructura.
        """
        print("🔍 Detectando estructura de tabla...")
        print(f"📊 Analizando tabla de {datos_crudos.shape[0]}x{datos_crudos.shape[1]}")

        # Buscar patrones conocidos en los datos
        estructura = {
            'filas_conceptos': [],
            'columnas_datos': [],  # Columnas con datos numéricos (H, M por grado)
            'columnas_subtotales': [],  # Columnas de subtotales H, M
            'columnas_totales': [],  # Columnas de totales
            'fila_inscripcion': None,
            'fila_bajas': None,
            'fila_existencia': None,
            'fila_altas': None
        }

        # 🔍 PASO 1: Detectar filas de conceptos principales
        for i, fila in datos_crudos.iterrows():
            concepto = str(fila.iloc[0]).upper() if pd.notna(fila.iloc[0]) else ""

            # Mostrar todas las filas para debugging
            print(f"🔍 Fila {i}: '{concepto}'")

            if 'INSCRIPCIÓN' in concepto or 'INSCRIPCION' in concepto:
                estructura['fila_inscripcion'] = i
                estructura['filas_conceptos'].append(('INSCRIPCIÓN', i))
                print(f"📍 INSCRIPCIÓN encontrada en fila {i}")

            elif 'BAJAS' in concepto:
                estructura['fila_bajas'] = i
                estructura['filas_conceptos'].append(('BAJAS', i))
                print(f"📍 BAJAS encontrada en fila {i}")

            elif 'EXISTENCIA' in concepto:
                estructura['fila_existencia'] = i
                estructura['filas_conceptos'].append(('EXISTENCIA', i))
                print(f"📍 EXISTENCIA encontrada en fila {i}")

            elif 'ALTAS' in concepto:
                estructura['fila_altas'] = i
                estructura['filas_conceptos'].append(('ALTAS', i))
                print(f"📍 ALTAS encontrada en fila {i}")

            elif 'PREINSCRIPCIÓN' in concepto or 'PREINSCRIPCION' in concepto:
                estructura['filas_conceptos'].append(('PREINSCRIPCIÓN 1ER. GRADO', i))
                print(f"📍 PREINSCRIPCIÓN 1ER. GRADO encontrada en fila {i}")

            elif 'BECADOS MUNICIPIO' in concepto:
                estructura['filas_conceptos'].append(('BECADOS MUNICIPIO', i))
                print(f"📍 BECADOS MUNICIPIO encontrada en fila {i}")

            elif 'BECADOS SEED' in concepto:
                estructura['filas_conceptos'].append(('BECADOS SEED', i))
                print(f"📍 BECADOS SEED encontrada en fila {i}")

            elif 'BIENESTAR' in concepto:
                estructura['filas_conceptos'].append(('BIENESTAR', i))
                print(f"📍 BIENESTAR encontrada en fila {i}")

            elif 'GRUPOS' in concepto:
                estructura['filas_conceptos'].append(('GRUPOS', i))
                print(f"📍 GRUPOS encontrada en fila {i}")

            elif 'APROBADOS' in concepto:
                estructura['filas_conceptos'].append(('APROBADOS', i))
                print(f"📍 APROBADOS encontrada en fila {i}")

            elif 'REPROBADOS' in concepto:
                estructura['filas_conceptos'].append(('REPROBADOS', i))
                print(f"📍 REPROBADOS encontrada en fila {i}")

            # Detectar otras filas que puedan tener datos numéricos
            elif concepto.strip() != '' and not concepto.startswith('[') and i > 2:
                # Verificar si la fila tiene datos numéricos
                tiene_numeros = False
                for j in range(7, min(19, len(fila))):  # Verificar área de datos
                    valor = fila.iloc[j]
                    if pd.notna(valor) and str(valor).strip() != '' and not str(valor).startswith('['):
                        try:
                            float(valor)
                            tiene_numeros = True
                            break
                        except:
                            pass

                if tiene_numeros:
                    estructura['filas_conceptos'].append((concepto, i))
                    print(f"📍 Concepto adicional encontrado en fila {i}: {concepto}")

        # 🔍 PASO 2: Analizar estructura de columnas de forma más inteligente
        if len(datos_crudos) >= 3:  # Fila 2 debería tener H, M, H, M, etc.
            fila_headers = datos_crudos.iloc[2]  # Fila "CONCEPTO" con H, M
            fila_grados = datos_crudos.iloc[1]   # Fila "GRADOS" para contexto

            print(f"🔍 Analizando headers: {fila_headers.values}")
            print(f"🔍 Analizando grados: {fila_grados.values}")

            for j, header in enumerate(fila_headers):
                header_str = str(header).upper().strip()
                grado_str = str(fila_grados.iloc[j]).upper().strip() if j < len(fila_grados) else ""

                # Identificar si estamos en área de datos, subtotales o totales
                if 'SUBTOTAL' in grado_str:
                    # Estamos en área de subtotales
                    if header_str == 'H':
                        estructura['columnas_subtotales'].append(('H', j))
                        print(f"📍 Subtotal H encontrado en posición {j}")
                    elif header_str == 'M':
                        estructura['columnas_subtotales'].append(('M', j))
                        print(f"📍 Subtotal M encontrado en posición {j}")

                elif 'TOTAL' in grado_str and 'SUBTOTAL' not in grado_str:
                    # Estamos en área de totales
                    estructura['columnas_totales'].append(('TOTAL', j))
                    print(f"📍 Total encontrado en posición {j}")

                elif header_str == 'H' and ('1O' in grado_str or '2O' in grado_str or '3O' in grado_str or
                                           '4O' in grado_str or '5O' in grado_str or '6O' in grado_str):
                    # Columna H de datos por grado
                    estructura['columnas_datos'].append(('H', j, grado_str))
                    print(f"📍 Datos H-{grado_str} en posición {j}")

                elif header_str == 'M' and ('1O' in grado_str or '2O' in grado_str or '3O' in grado_str or
                                           '4O' in grado_str or '5O' in grado_str or '6O' in grado_str):
                    # Columna M de datos por grado
                    estructura['columnas_datos'].append(('M', j, grado_str))
                    print(f"📍 Datos M-{grado_str} en posición {j}")

                elif header_str == 'H' and j > 15:  # Área probable de subtotales
                    estructura['columnas_subtotales'].append(('H', j))
                    print(f"📍 Posible Subtotal H en posición {j}")

                elif header_str == 'M' and j > 15:  # Área probable de subtotales
                    estructura['columnas_subtotales'].append(('M', j))
                    print(f"📍 Posible Subtotal M en posición {j}")

        self.estructura_detectada = estructura
        print(f"✅ Estructura detectada:")
        print(f"   📋 Conceptos: {len(estructura['filas_conceptos'])}")
        print(f"   📊 Columnas datos: {len(estructura['columnas_datos'])}")
        print(f"   🧮 Columnas subtotales: {len(estructura['columnas_subtotales'])}")
        print(f"   📈 Columnas totales: {len(estructura['columnas_totales'])}")
    
    def _validar_subtotales_totales(self, datos_numericos: pd.DataFrame):
        """
        Validar que los subtotales y totales coincidan con las sumas reales.
        """
        print("🧮 Validando subtotales y totales...")

        # Verificar si tenemos columnas de subtotales detectadas
        if not self.estructura_detectada.get('columnas_subtotales'):
            print("⚠️ No se detectaron columnas de subtotales")
            return

        print(f"✅ Detectadas {len(self.estructura_detectada['columnas_subtotales'])} columnas de subtotales")

        # Validar cada fila de conceptos
        for concepto, fila_idx in self.estructura_detectada['filas_conceptos']:
            # MAPEAR índice de tabla completa a datos_numericos
            offset_numerico = 3  # Primer fila de datos numéricos
            idx_numerico = fila_idx - offset_numerico

            if 0 <= idx_numerico < len(datos_numericos):
                print(f"🔍 Validando {concepto} en fila {fila_idx}")
                self._validar_fila_subtotales(datos_numericos, concepto, fila_idx)
            else:
                print(f"⚠️ Fila {fila_idx} fuera de rango para {concepto} (mapeado: {idx_numerico})")
    
    def _validar_fila_subtotales(self, datos_numericos: pd.DataFrame, concepto: str, fila_idx: int):
        """
        Validar subtotales de una fila específica usando estructura detectada.
        """
        try:
            # GRUPOS no tiene subtotales H/M, se valida diferente
            if 'GRUPOS' in concepto.upper():
                print(f"🔍 GRUPOS detectado - saltando validación de subtotales H/M")
                print(f"   ℹ️ GRUPOS se valida como suma directa en la validación de totales")
                return

            print(f"🔍 Validando subtotales para {concepto} (fila {fila_idx})")
            print(f"📊 Tamaño datos_numericos: {datos_numericos.shape}")

            # MAPEAR índice de tabla completa a datos_numericos
            offset_numerico = 3  # Primer fila de datos numéricos
            idx_numerico = fila_idx - offset_numerico

            print(f"🔍 Mapeando fila {fila_idx} → {idx_numerico} en datos_numericos")

            if idx_numerico < 0 or idx_numerico >= len(datos_numericos):
                print(f"⚠️ Fila {fila_idx} fuera de rango para datos_numericos (max: {len(datos_numericos)-1})")
                return

            fila_cruda = datos_numericos.iloc[idx_numerico]
            print(f"📊 Datos de fila {fila_idx}: {fila_cruda.values}")
            print(f"📊 Longitud de fila: {len(fila_cruda)}")

            # Mostrar estructura detectada para debugging
            print(f"🔍 Columnas de datos detectadas: {len(self.estructura_detectada['columnas_datos'])}")
            print(f"🔍 Columnas de subtotales detectadas: {len(self.estructura_detectada['columnas_subtotales'])}")
            for i, item in enumerate(self.estructura_detectada['columnas_datos'][:5]):  # Mostrar solo las primeras 5
                print(f"   📊 Dato {i}: {item}")
            for i, item in enumerate(self.estructura_detectada['columnas_subtotales']):
                print(f"   🧮 Subtotal {i}: {item}")

            # Separar columnas de datos H y M usando estructura detectada
            valores_h = []
            valores_m = []

            for item in self.estructura_detectada['columnas_datos']:
                if len(item) >= 2:  # Puede tener 2 o 3 elementos (tipo, col_idx, [grado])
                    tipo, col_idx = item[0], item[1]
                    grado = item[2] if len(item) > 2 else "N/A"

                    # MAPEAR columna de tabla completa a datos_numericos
                    offset_columna = 7  # Primera columna de datos numéricos
                    idx_columna = col_idx - offset_columna

                    if 0 <= idx_columna < len(fila_cruda):
                        valor = fila_cruda.iloc[idx_columna]
                        # Convertir a número si es posible
                        try:
                            valor_num = float(valor) if pd.notna(valor) and str(valor).strip() != '' else 0
                            if tipo == 'H':
                                valores_h.append(valor_num)
                                print(f"   📊 H-{grado} en col {col_idx}: {valor_num}")
                            elif tipo == 'M':
                                valores_m.append(valor_num)
                                print(f"   📊 M-{grado} en col {col_idx}: {valor_num}")
                        except (ValueError, TypeError):
                            print(f"   ⚠️ Valor no numérico en col {col_idx}: {valor}")

            # Calcular sumas y mostrar operación completa
            suma_h_calculada = sum(valores_h) if valores_h else 0
            suma_m_calculada = sum(valores_m) if valores_m else 0

            # Mostrar operación de suma H
            if valores_h:
                operacion_h = " + ".join([str(v) for v in valores_h])
                print(f"🧮 Suma H calculada: {operacion_h} = {suma_h_calculada}")
            else:
                print(f"🧮 Suma H calculada: 0 (sin valores)")

            # Mostrar operación de suma M
            if valores_m:
                operacion_m = " + ".join([str(v) for v in valores_m])
                print(f"🧮 Suma M calculada: {operacion_m} = {suma_m_calculada}")
            else:
                print(f"🧮 Suma M calculada: 0 (sin valores)")

            # Buscar subtotales reportados en las columnas de subtotales
            for item in self.estructura_detectada['columnas_subtotales']:
                if len(item) >= 2:
                    tipo, col_idx = item[0], item[1]

                    # MAPEAR columna de tabla completa a datos_numericos
                    offset_columna = 7  # Primera columna de datos numéricos
                    idx_columna = col_idx - offset_columna

                    if 0 <= idx_columna < len(fila_cruda):
                        valor_celda = fila_cruda.iloc[idx_columna]
                        print(f"🔍 DEBUG - {concepto} {tipo} col {col_idx}→{idx_columna}: valor_celda = {valor_celda}")

                        # Convertir a número, manejando marcadores [valor]
                        try:
                            if isinstance(valor_celda, str) and valor_celda.startswith('[') and valor_celda.endswith(']'):
                                # Es un marcador [valor], extraer el número
                                numero_str = valor_celda.strip('[]')
                                subtotal_reportado = float(numero_str) if numero_str.strip() != '' else 0
                            else:
                                subtotal_reportado = float(valor_celda) if pd.notna(valor_celda) else 0

                            if tipo == 'H':
                                print(f"📋 Subtotal H reportado: {subtotal_reportado}")
                                diferencia = abs(suma_h_calculada - subtotal_reportado)
                                print(f"🔍 Diferencia H en {concepto}: |{suma_h_calculada} - {subtotal_reportado}| = {diferencia}")
                                if diferencia > 0.01:
                                    print(f"❌ Discrepancia en subtotal H de {concepto}: reportado {subtotal_reportado} vs calculado {suma_h_calculada}")
                                    self.discrepancias.append({
                                        'tipo': 'SUBTOTAL_H',
                                        'concepto': concepto,
                                        'valor_reportado': subtotal_reportado,
                                        'valor_calculado': suma_h_calculada,
                                        'diferencia': abs(suma_h_calculada - subtotal_reportado),
                                        'descripcion': f"❌ Subtotal H en {concepto}: reportado {subtotal_reportado}, calculado {' + '.join([str(v) for v in valores_h]) if valores_h else '0'} = {suma_h_calculada}"
                                    })
                                else:
                                    operacion_h = " + ".join([str(v) for v in valores_h]) if valores_h else "0"
                                    self.validaciones_exitosas.append({
                                        'tipo': 'SUBTOTAL_H',
                                        'concepto': concepto,
                                        'valor': subtotal_reportado,
                                        'descripcion': f"✅ Subtotal H en {concepto}: {operacion_h} = {subtotal_reportado} (correcto)"
                                    })
                                    print(f"✅ Subtotal H correcto en {concepto}")

                            elif tipo == 'M':
                                print(f"📋 Subtotal M reportado: {subtotal_reportado}")
                                if abs(suma_m_calculada - subtotal_reportado) > 0.01:
                                    self.discrepancias.append({
                                        'tipo': 'SUBTOTAL_M',
                                        'concepto': concepto,
                                        'valor_reportado': subtotal_reportado,
                                        'valor_calculado': suma_m_calculada,
                                        'diferencia': abs(suma_m_calculada - subtotal_reportado),
                                        'descripcion': f"❌ Subtotal M en {concepto}: reportado {subtotal_reportado}, calculado {' + '.join([str(v) for v in valores_m]) if valores_m else '0'} = {suma_m_calculada}"
                                    })
                                else:
                                    operacion_m = " + ".join([str(v) for v in valores_m]) if valores_m else "0"
                                    self.validaciones_exitosas.append({
                                        'tipo': 'SUBTOTAL_M',
                                        'concepto': concepto,
                                        'valor': subtotal_reportado,
                                        'descripcion': f"✅ Subtotal M en {concepto}: {operacion_m} = {subtotal_reportado} (correcto)"
                                    })
                                    print(f"✅ Subtotal M correcto en {concepto}")

                        except (ValueError, TypeError) as e:
                            print(f"⚠️ Error procesando subtotal {tipo} en col {col_idx}: {valor_celda} - {e}")

        except Exception as e:
            print(f"⚠️ Error validando subtotales en {concepto}: {e}")
    
    def _validar_coherencia_filas(self, datos_numericos: pd.DataFrame):
        """
        Validar coherencia entre filas relacionadas (Existencia = Inscripción - Bajas).
        """
        print("🔄 Validando coherencia entre filas...")
        
        estructura = self.estructura_detectada
        fila_inscripcion = estructura.get('fila_inscripcion')
        fila_bajas = estructura.get('fila_bajas')
        fila_existencia = estructura.get('fila_existencia')
        
        if all(x is not None for x in [fila_inscripcion, fila_bajas, fila_existencia]):
            try:
                # MAPEAR índices de tabla completa a datos_numericos
                # datos_numericos empieza en fila 3 de la tabla completa
                offset_numerico = 3  # Primer fila de datos numéricos

                idx_inscripcion = fila_inscripcion - offset_numerico
                idx_bajas = fila_bajas - offset_numerico
                idx_existencia = fila_existencia - offset_numerico

                print(f"🔍 Mapeando índices: inscripción {fila_inscripcion}→{idx_inscripcion}, bajas {fila_bajas}→{idx_bajas}, existencia {fila_existencia}→{idx_existencia}")

                if all(0 <= idx < len(datos_numericos) for idx in [idx_inscripcion, idx_bajas, idx_existencia]):
                    inscripcion = datos_numericos.iloc[idx_inscripcion]
                    bajas = datos_numericos.iloc[idx_bajas]
                    existencia = datos_numericos.iloc[idx_existencia]
                else:
                    print(f"❌ Índices fuera de rango para datos_numericos ({len(datos_numericos)} filas)")
                    return
                
                # Calcular existencia esperada por columna (solo en columnas de datos)
                for item in self.estructura_detectada['columnas_datos']:
                    if len(item) >= 2:
                        tipo, col_idx = item[0], item[1]
                        grado = item[2] if len(item) > 2 else f"Col{col_idx}"

                        # MAPEAR columna de tabla completa a datos_numericos
                        offset_columna = 7  # Primera columna de datos numéricos
                        idx_columna = col_idx - offset_columna

                        if 0 <= idx_columna < min(len(inscripcion), len(bajas), len(existencia)):
                            try:
                                # Convertir valores a números
                                val_inscripcion = self._convertir_a_numero(inscripcion.iloc[idx_columna])
                                val_bajas = self._convertir_a_numero(bajas.iloc[idx_columna])
                                val_existencia = self._convertir_a_numero(existencia.iloc[idx_columna])

                                if val_inscripcion is not None and val_bajas is not None and val_existencia is not None:
                                    existencia_calculada = val_inscripcion - val_bajas

                                    if abs(existencia_calculada - val_existencia) > 0.01:
                                        self.discrepancias.append({
                                            'tipo': 'COHERENCIA_EXISTENCIA',
                                            'concepto': f'{tipo}-{grado}',
                                            'valor_reportado': val_existencia,
                                            'valor_calculado': existencia_calculada,
                                            'diferencia': abs(existencia_calculada - val_existencia),
                                            'descripcion': f"Existencia {tipo}-{grado}: reportada {val_existencia}, calculada {existencia_calculada} (Inscripción {val_inscripcion} - Bajas {val_bajas})"
                                        })
                                    else:
                                        self.validaciones_exitosas.append({
                                            'tipo': 'COHERENCIA_EXISTENCIA',
                                            'concepto': f'{tipo}-{grado}',
                                            'valor': val_existencia,
                                            'descripcion': f"✅ Coherencia {tipo}-{grado}: Existencia {val_existencia} = Inscripción {val_inscripcion} - Bajas {val_bajas}"
                                        })
                                        print(f"✅ Coherencia correcta en {tipo}-{grado}")

                            except Exception as e:
                                print(f"⚠️ Error validando coherencia en col {col_idx}: {e}")
                            
            except Exception as e:
                print(f"⚠️ Error validando coherencia de filas: {e}")
        else:
            print("⚠️ No se pudieron identificar todas las filas necesarias para validación de coherencia")

    def _validar_totales(self, datos_numericos: pd.DataFrame):
        """
        Validar que los totales coincidan con la suma de subtotales H + M.
        """
        print("🧮 Validando totales (Subtotal H + Subtotal M)...")

        # Verificar si tenemos columnas de totales detectadas
        if not self.estructura_detectada.get('columnas_totales'):
            print("⚠️ No se detectaron columnas de totales")
            return

        print(f"✅ Detectadas {len(self.estructura_detectada['columnas_totales'])} columnas de totales")

        # Validar cada fila de conceptos
        for concepto, fila_idx in self.estructura_detectada['filas_conceptos']:
            # MAPEAR índice de tabla completa a datos_numericos
            offset_numerico = 3  # Primer fila de datos numéricos
            idx_numerico = fila_idx - offset_numerico

            if 0 <= idx_numerico < len(datos_numericos):
                print(f"🔍 Validando total de {concepto} en fila {fila_idx}")
                self._validar_fila_totales(datos_numericos, concepto, fila_idx)
            else:
                print(f"⚠️ Fila {fila_idx} fuera de rango para total de {concepto} (mapeado: {idx_numerico})")

    def _validar_fila_totales(self, datos_numericos: pd.DataFrame, concepto: str, fila_idx: int):
        """
        Validar total de una fila específica.

        - Para conceptos normales: Total = Subtotal H + Subtotal M
        - Para GRUPOS: Total = suma directa de todas las celdas H + M
        """
        try:
            print(f"🔍 Validando total para {concepto} (fila {fila_idx})")

            # MAPEAR índice de tabla completa a datos_numericos
            offset_numerico = 3  # Primer fila de datos numéricos
            idx_numerico = fila_idx - offset_numerico

            if idx_numerico < 0 or idx_numerico >= len(datos_numericos):
                print(f"⚠️ Fila {fila_idx} fuera de rango para datos_numericos")
                return

            fila_cruda = datos_numericos.iloc[idx_numerico]

            # Validación especial para GRUPOS
            if 'GRUPOS' in concepto.upper():
                self._validar_total_grupos(fila_cruda, concepto)
                return

            # Buscar subtotales H y M en esta fila
            subtotal_h = None
            subtotal_m = None

            for item in self.estructura_detectada['columnas_subtotales']:
                if len(item) >= 2:
                    tipo, col_idx = item[0], item[1]

                    # MAPEAR columna de tabla completa a datos_numericos
                    offset_columna = 7  # Primera columna de datos numéricos
                    idx_columna = col_idx - offset_columna

                    if 0 <= idx_columna < len(fila_cruda):
                        valor_celda = fila_cruda.iloc[idx_columna]
                        valor_num = self._convertir_a_numero(valor_celda)

                        if valor_num is not None:
                            if tipo == 'H':
                                subtotal_h = valor_num
                                print(f"   📊 Subtotal H: {subtotal_h}")
                            elif tipo == 'M':
                                subtotal_m = valor_num
                                print(f"   📊 Subtotal M: {subtotal_m}")

            # Calcular total esperado y mostrar operación
            if subtotal_h is not None and subtotal_m is not None:
                total_calculado = subtotal_h + subtotal_m
                print(f"🧮 Total calculado para {concepto}: {subtotal_h} (H) + {subtotal_m} (M) = {total_calculado}")

                # VALIDACIÓN CRUZADA: Calcular también suma directa de celdas
                total_directo = self._calcular_total_directo(fila_cruda, concepto)
                if abs(total_calculado - total_directo) > 0.01:
                    print(f"⚠️ DISCREPANCIA INTERNA en {concepto}:")
                    print(f"   Método subtotales: {total_calculado}")
                    print(f"   Método directo: {total_directo}")
                    print(f"   Diferencia: {abs(total_calculado - total_directo)}")

                    # AGREGAR como discrepancia oficial
                    self.discrepancias.append({
                        'tipo': 'DISCREPANCIA_INTERNA',
                        'concepto': concepto,
                        'valor_reportado': total_calculado,
                        'valor_calculado': total_directo,
                        'diferencia': abs(total_calculado - total_directo),
                        'descripcion': f"❌ {concepto}: Subtotales suman {total_calculado}, pero celdas suman {total_directo}. Problema en subtotales H/M."
                    })
                else:
                    print(f"✅ Validación cruzada OK: {total_calculado} = {total_directo}")

                # Buscar totales reportados
                for item in self.estructura_detectada['columnas_totales']:
                    if len(item) >= 2:
                        tipo, col_idx = item[0], item[1]

                        # MAPEAR columna de tabla completa a datos_numericos
                        offset_columna = 7  # Primera columna de datos numéricos
                        idx_columna = col_idx - offset_columna

                        if 0 <= idx_columna < len(fila_cruda):
                            valor_celda = fila_cruda.iloc[idx_columna]
                            total_reportado = self._convertir_a_numero(valor_celda)

                            if total_reportado is not None:
                                print(f"📋 Total reportado: {total_reportado}")

                                if abs(total_calculado - total_reportado) > 0.01:
                                    self.discrepancias.append({
                                        'tipo': 'TOTAL',
                                        'concepto': concepto,
                                        'valor_reportado': total_reportado,
                                        'valor_calculado': total_calculado,
                                        'diferencia': abs(total_calculado - total_reportado),
                                        'descripcion': f"❌ Total {concepto}: reportado {total_reportado}, calculado {subtotal_h} (H) + {subtotal_m} (M) = {total_calculado}"
                                    })
                                else:
                                    self.validaciones_exitosas.append({
                                        'tipo': 'TOTAL',
                                        'concepto': concepto,
                                        'valor': total_reportado,
                                        'descripcion': f"✅ Total {concepto}: {subtotal_h} (H) + {subtotal_m} (M) = {total_reportado}"
                                    })
                                    print(f"✅ Total correcto en {concepto}")
                                break  # Solo validar el primer total encontrado
            else:
                subtotal_h_str = f"{subtotal_h}" if subtotal_h is not None else "NO ENCONTRADO"
                subtotal_m_str = f"{subtotal_m}" if subtotal_m is not None else "NO ENCONTRADO"
                print(f"⚠️ No se encontraron ambos subtotales para calcular total de {concepto}")
                print(f"   📊 Subtotal H: {subtotal_h_str}")
                print(f"   📊 Subtotal M: {subtotal_m_str}")

                # Agregar como discrepancia si hay datos pero faltan subtotales
                if subtotal_h is None or subtotal_m is None:
                    self.discrepancias.append({
                        'tipo': 'SUBTOTALES_FALTANTES',
                        'concepto': concepto,
                        'valor_reportado': 'N/A',
                        'valor_calculado': 'N/A',
                        'diferencia': 0,
                        'descripcion': f"❌ {concepto}: Subtotal H: {subtotal_h_str}, Subtotal M: {subtotal_m_str}"
                    })

        except Exception as e:
            print(f"⚠️ Error validando total en {concepto}: {e}")

    def _validar_total_grupos(self, fila_cruda, concepto):
        """
        Validar total de GRUPOS sumando directamente todas las celdas H y M.

        Para GRUPOS no hay subtotales reales, el total es la suma directa.
        """
        try:
            print(f"🔍 Validación especial para {concepto} - suma directa de celdas")

            # Sumar todas las celdas de datos H y M directamente
            suma_total_calculada = 0
            celdas_sumadas = []

            for item in self.estructura_detectada['columnas_datos']:
                if len(item) >= 2:
                    tipo, col_idx = item[0], item[1]
                    grado = item[2] if len(item) > 2 else f"Col{col_idx}"

                    # MAPEAR columna de tabla completa a datos_numericos
                    offset_columna = 7  # Primera columna de datos numéricos
                    idx_columna = col_idx - offset_columna

                    if 0 <= idx_columna < len(fila_cruda):
                        valor_num = self._convertir_a_numero(fila_cruda.iloc[idx_columna])
                        if valor_num is not None and valor_num > 0:  # Solo sumar valores positivos
                            suma_total_calculada += valor_num
                            celdas_sumadas.append(f"{tipo}-{grado}: {valor_num}")
                            print(f"   📊 {tipo}-{grado}: {valor_num}")

            # Mostrar operación completa
            if celdas_sumadas:
                operacion_completa = " + ".join([celda.split(": ")[1] for celda in celdas_sumadas])
                print(f"🧮 Total GRUPOS calculado: {operacion_completa} = {suma_total_calculada}")
                print(f"📋 Celdas incluidas: {', '.join([celda.split(': ')[0] for celda in celdas_sumadas])}")
            else:
                print(f"🧮 Total GRUPOS calculado: 0 (sin celdas con valores)")
                print(f"📋 Celdas sumadas: 0")

            # Buscar total reportado
            for item in self.estructura_detectada['columnas_totales']:
                if len(item) >= 2:
                    tipo, col_idx = item[0], item[1]

                    # MAPEAR columna de tabla completa a datos_numericos
                    offset_columna = 7  # Primera columna de datos numéricos
                    idx_columna = col_idx - offset_columna

                    if 0 <= idx_columna < len(fila_cruda):
                        valor_celda = fila_cruda.iloc[idx_columna]
                        total_reportado = self._convertir_a_numero(valor_celda)

                        if total_reportado is not None:
                            print(f"📋 Total GRUPOS reportado: {total_reportado}")

                            if abs(suma_total_calculada - total_reportado) > 0.01:
                                self.discrepancias.append({
                                    'tipo': 'TOTAL_GRUPOS',
                                    'concepto': concepto,
                                    'valor_reportado': total_reportado,
                                    'valor_calculado': suma_total_calculada,
                                    'diferencia': abs(suma_total_calculada - total_reportado),
                                    'descripcion': f"❌ Total GRUPOS: reportado {total_reportado}, calculado {' + '.join([celda.split(': ')[1] for celda in celdas_sumadas]) if celdas_sumadas else '0'} = {suma_total_calculada}"
                                })
                            else:
                                self.validaciones_exitosas.append({
                                    'tipo': 'TOTAL_GRUPOS',
                                    'concepto': concepto,
                                    'valor': total_reportado,
                                    'descripcion': f"✅ Total GRUPOS: {' + '.join([celda.split(': ')[1] for celda in celdas_sumadas]) if celdas_sumadas else '0'} = {total_reportado} (suma directa)"
                                })
                                print(f"✅ Total GRUPOS correcto")
                            break  # Solo validar el primer total encontrado

        except Exception as e:
            print(f"⚠️ Error validando total de GRUPOS: {e}")

    def _calcular_total_directo(self, fila_cruda, concepto):
        """
        Calcular total sumando directamente todas las celdas H y M.

        Esto sirve para validación cruzada contra el método de subtotales.
        """
        try:
            suma_directa = 0
            celdas_sumadas = []

            for item in self.estructura_detectada['columnas_datos']:
                if len(item) >= 2:
                    tipo, col_idx = item[0], item[1]
                    grado = item[2] if len(item) > 2 else f"Col{col_idx}"

                    # MAPEAR columna de tabla completa a datos_numericos
                    offset_columna = 7  # Primera columna de datos numéricos
                    idx_columna = col_idx - offset_columna

                    if 0 <= idx_columna < len(fila_cruda):
                        valor_num = self._convertir_a_numero(fila_cruda.iloc[idx_columna])
                        if valor_num is not None:
                            suma_directa += valor_num
                            if valor_num > 0:  # Solo mostrar valores no-cero
                                celdas_sumadas.append(f"{tipo}-{grado}: {valor_num}")

            return suma_directa

        except Exception as e:
            print(f"⚠️ Error calculando total directo: {e}")
            return 0

    def _generar_reporte(self) -> Dict:
        """
        Generar reporte final de validación.
        """
        reporte = {
            'total_discrepancias': len(self.discrepancias),
            'total_validaciones_exitosas': len(self.validaciones_exitosas),
            'discrepancias': self.discrepancias,
            'validaciones_exitosas': self.validaciones_exitosas,
            'estructura_detectada': self.estructura_detectada,
            'resumen': self._generar_resumen()
        }
        
        return reporte
    
    def _generar_resumen(self) -> str:
        """
        Generar resumen textual completo de validaciones.
        """
        total_validaciones = len(self.validaciones_exitosas) + len(self.discrepancias)

        if total_validaciones == 0:
            return "⚠️ No se pudieron realizar validaciones"

        resumen = f"🔍 AUDITORÍA COMPLETA: {total_validaciones} validaciones realizadas\n"
        resumen += f"✅ Correctas: {len(self.validaciones_exitosas)}\n"
        resumen += f"⚠️ Discrepancias: {len(self.discrepancias)}\n"

        # Mostrar validaciones exitosas (resumen)
        if self.validaciones_exitosas:
            resumen += f"\n✅ VALIDACIONES EXITOSAS:\n"
            tipos_exitosos = {}
            for val in self.validaciones_exitosas:
                tipo = val['tipo']
                if tipo not in tipos_exitosos:
                    tipos_exitosos[tipo] = []
                tipos_exitosos[tipo].append(val)

            for tipo, validaciones in tipos_exitosos.items():
                resumen += f"   📊 {tipo}: {len(validaciones)} correctas\n"

        # Mostrar discrepancias (detallado)
        if self.discrepancias:
            resumen += f"\n⚠️ DISCREPANCIAS ENCONTRADAS:\n"
            tipos_disc = {}
            for disc in self.discrepancias:
                tipo = disc['tipo']
                if tipo not in tipos_disc:
                    tipos_disc[tipo] = []
                tipos_disc[tipo].append(disc)

            for tipo, discrepancias in tipos_disc.items():
                resumen += f"   📊 {tipo}: {len(discrepancias)} casos\n"
                for disc in discrepancias[:2]:  # Mostrar máximo 2 ejemplos
                    resumen += f"      • {disc['descripcion']}\n"
                if len(discrepancias) > 2:
                    resumen += f"      • ... y {len(discrepancias) - 2} más\n"

        return resumen

    def _convertir_a_numero(self, valor):
        """
        Convertir un valor a número, manejando marcadores [valor] y strings.

        Returns:
            float: Número convertido o 0.0 si está vacío/None
        """
        try:
            # Casos de valores vacíos o None
            if pd.isna(valor) or valor is None:
                return 0.0

            # Si ya es número (incluyendo tipos numpy)
            if isinstance(valor, (int, float)) or hasattr(valor, 'dtype'):
                return float(valor)

            # Si es string
            if isinstance(valor, str):
                valor_limpio = valor.strip()

                # String completamente vacío
                if valor_limpio == '':
                    return 0.0

                # Manejar marcadores [valor]
                if valor_limpio.startswith('[') and valor_limpio.endswith(']'):
                    numero_str = valor_limpio.strip('[]').strip()
                    if numero_str == '':
                        return 0.0
                    return float(numero_str)
                else:
                    # String normal con número
                    return float(valor_limpio)

            # Otros tipos no soportados
            print(f"⚠️ Tipo no soportado para conversión: {type(valor)} - {valor}")
            return 0.0

        except (ValueError, TypeError) as e:
            print(f"⚠️ Error convirtiendo '{valor}' a número: {e}")
            return 0.0
