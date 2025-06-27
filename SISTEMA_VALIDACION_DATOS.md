# 🔍 SISTEMA DE VALIDACIÓN DE DATOS INTERNOS

## 📋 RESUMEN EJECUTIVO

El **Sistema de Validación de Datos** es un auditor silencioso que verifica automáticamente la coherencia matemática interna de las tablas de movimiento de alumnos. Detecta errores humanos de cálculo sin ser invasivo, proporcionando reportes completos tanto de validaciones exitosas como de discrepancias encontradas.

## 🎯 OBJETIVOS

- ✅ **Validar subtotales y totales** automáticamente
- ✅ **Verificar coherencia** entre filas relacionadas
- ✅ **Detectar errores humanos** de cálculo
- ✅ **Reportar estado completo** (éxitos y problemas)
- ✅ **No ser invasivo** - solo alertar, nunca modificar

## 🏗️ ARQUITECTURA DEL SISTEMA

### **Componentes Principales:**

```
📦 src/core/data_validator.py
├── 🔍 DataValidator (Clase principal)
├── 🧮 Detección de estructura de tabla
├── ⚖️ Validaciones matemáticas
└── 📋 Generación de reportes

📦 main.py
├── 🔄 Integración en flujo de carga
├── 🎨 Interfaz de resultados
└── 📊 Manejo de reportes
```

## 📊 TIPOS DE VALIDACIONES

### **1. VALIDACIÓN DE SUBTOTALES**
**Objetivo:** Verificar que los subtotales H y M coincidan con la suma de sus columnas respectivas.

**Lógica:**
```
Subtotal H = Suma(H_1o + H_2o + H_3o + H_4o + H_5o + H_6o)
Subtotal M = Suma(M_1o + M_2o + M_3o + M_4o + M_5o + M_6o)
```

**Ejemplo:**
```
✅ Subtotal H en INSCRIPCIÓN: 524.0 (correcto)
   Calculado: 72 + 82 + 100 + 74 + 92 + 104 = 524
   Reportado: 524
```

### **2. VALIDACIÓN DE TOTALES**
**Objetivo:** Verificar que los totales sean la suma correcta de subtotales H + M.

**Lógica:**
```
Total = Subtotal H + Subtotal M
```

**Ejemplo:**
```
✅ Total en INSCRIPCIÓN: 1089.0 = Subtotal H 524.0 + Subtotal M 565.0
```

### **3. VALIDACIÓN ESPECIAL: GRUPOS**
**Objetivo:** Para el concepto GRUPOS, validar suma directa sin subtotales intermedios.

**Lógica Especial:**
```
Total GRUPOS = Suma directa de todas las celdas H + M con valores > 0
```

**Razón:** GRUPOS no tiene subtotales reales, solo cuenta individuos por grado.

**Ejemplo:**
```
✅ Total GRUPOS: 46.0 (suma directa de 6 celdas)
   H-1o: 12 + M-1o: 12 + H-2o: 12 + M-2o: 10 + ...
```

### **4. VALIDACIÓN DE COHERENCIA**
**Objetivo:** Verificar relaciones lógicas entre conceptos.

**Lógica:**
```
Existencia = Inscripción - Bajas
```

**Ejemplo:**
```
✅ Coherencia H-1O.: Existencia 72.0 = Inscripción 72.0 - Bajas 0.0
```

## 🔧 DETECCIÓN INTELIGENTE DE ESTRUCTURA

### **Mapeo Automático de Tabla:**

```python
# Análisis de filas de headers
Fila 1 (GRADOS): [1o., 2o., 3o., 4o., 5o., 6o., SUBTOTAL, TOTAL]
Fila 2 (CONCEPTO): [H, M, H, M, H, M, H, M, H, M, H, M, H, M, [TOTAL]]

# Detección de áreas
- Columnas 7-18: Datos por grado (H, M alternados)
- Columnas 19, 21: Subtotales (H, M)
- Columnas 23-25: Totales
```

### **Conceptos Detectados:**
1. **PREINSCRIPCIÓN 1ER. GRADO**
2. **INSCRIPCIÓN**
3. **BAJAS**
4. **EXISTENCIA**
5. **ALTAS**
6. **BECADOS MUNICIPIO**
7. **BECADOS SEED**
8. **BIENESTAR**
9. **GRUPOS** (validación especial)

## 🎨 INTERFAZ DE USUARIO

### **Panel de Validaciones:**
- 🟢 **Verde:** Todas las validaciones exitosas
- 🔴 **Rojo:** Discrepancias encontradas
- 📋 **Botón "Ver Detalles":** Reporte completo

### **Reporte Completo:**
```
🔍 AUDITORÍA DETALLADA: archivo.xlsx
✅ Validaciones exitosas: 33
⚠️ Discrepancias encontradas: 0

✅ VALIDACIONES CORRECTAS:
1. ✅ Subtotal H en INSCRIPCIÓN: 524.0 (correcto)
2. ✅ Total en INSCRIPCIÓN: 1089.0 = Subtotal H 524.0 + Subtotal M 565.0
...
```

## ⚙️ FLUJO DE EJECUCIÓN

### **1. Carga de Archivo:**
```python
# En main.py - método cargar_archivo()
self._validar_coherencia_archivo(nombre_archivo)
```

### **2. Validación Automática:**
```python
# Usar datos del Paso 2 (con marcadores [valor])
reporte = self.data_validator.validar_tabla_completa(datos_combinados, datos_crudos)
```

### **3. Procesamiento:**
```python
# En DataValidator
1. _detectar_estructura_tabla()    # Mapear filas y columnas
2. _validar_subtotales_totales()   # Validar cálculos
3. _validar_totales()              # Validar sumas
4. _validar_coherencia_filas()     # Validar lógica
5. _generar_reporte()              # Crear reporte final
```

### **4. Presentación:**
```python
# Mostrar resultados en interfaz
self._mostrar_resultados_validacion(reporte, nombre_archivo)
```

## 🔍 VALIDACIÓN POR ARCHIVO

**¿Se valida cada archivo individualmente?**

**✅ SÍ** - Cada archivo se valida independientemente:

1. **Al cargar un archivo nuevo:** Se ejecuta validación automática
2. **Al cambiar de archivo:** Se muestra la validación específica de ese archivo
3. **Cada archivo mantiene:** Su propio reporte de validación
4. **Panel dinámico:** Muestra validación del archivo actualmente seleccionado

**Ventajas:**
- ✅ **Detección inmediata** de problemas por archivo
- ✅ **Trazabilidad específica** por fuente de datos
- ✅ **Validación independiente** sin interferencias
- ✅ **Reportes granulares** para corrección dirigida

## 🚀 BENEFICIOS DEL SISTEMA

### **Para el Usuario:**
- 🎯 **Confianza:** Saber que los datos están matemáticamente correctos
- ⚡ **Rapidez:** Detección automática vs. verificación manual
- 📋 **Trazabilidad:** Reportes detallados de cada validación
- 🔍 **Transparencia:** Ver tanto éxitos como problemas

### **Para el Proceso:**
- 🛡️ **Calidad:** Prevención de errores en sumatorias finales
- 📊 **Auditoría:** Registro completo de validaciones
- 🔄 **Escalabilidad:** Fácil agregar nuevas validaciones
- ⚙️ **Mantenibilidad:** Código modular y bien estructurado

## 🔮 PRÓXIMAS FUNCIONALIDADES

### **5. VALIDACIÓN CRUZADA ESC1 vs ESC2 (PRIORITARIA)**
**Objetivo:** Validar coherencia entre datos de grupos (ESC1) y existencias (ESC2).

**Lógica:**
```
Total Existencias por Grado (ESC2) = Suma de Grupos por Grado (ESC1)
```

**Ejemplo:**
```
ESC1 - Grupos 1er Grado: 1A(25) + 1B(23) + 1C(24) = 72 alumnos
ESC2 - Existencia 1er Grado: H(35) + M(37) = 72 alumnos
✅ Coherencia: 72 = 72 (correcto)
```

**Implementación:**
- 📊 **Extracción dual:** ESC1 (grupos) + ESC2 (movimientos)
- 🔄 **Validación primaria:** Ejecutar antes que validaciones internas
- 🚦 **Sistema de semáforos:** Verde = continuar, Rojo = revisar datos base
- 📋 **Reporte integrado:** Incluir en interfaz de validaciones

### **ARQUITECTURA MEJORADA (EN DESARROLLO)**

#### **Separación de Responsabilidades:**
```
📦 src/core/
├── 📊 excel_extractor.py      # Extracción pura de datos
├── 🔄 data_transformer.py     # Transformación y normalización
├── 🔍 data_validator.py       # Validaciones (actual)
├── 📋 table_analyzer.py       # Análisis inteligente de estructura
└── 🗄️ data_normalizer.py      # Normalización tipo BD (futuro)

📦 src/validation/
├── 🔄 cross_sheet_validator.py # Validaciones entre hojas
├── 📊 internal_validator.py    # Validaciones internas (actual)
└── 🎯 validation_engine.py     # Motor de validaciones

📦 src/data/
├── 📋 table_schema.py          # Esquemas de tablas
├── 🗺️ data_mapper.py           # Mapeo de datos
└── 🔍 query_engine.py          # Motor de consultas (IA futuro)
```

#### **Normalización de Datos (Evaluación):**
**Ventajas:**
- 🔍 **Consultas complejas:** SQL-like sobre datos educativos
- 🤖 **IA Integration:** Fácil acceso para sistemas de IA
- 📊 **Análisis avanzado:** Tendencias, patrones, estadísticas
- 🔄 **Escalabilidad:** Manejo de grandes volúmenes

**Desventajas:**
- ⚡ **Complejidad:** Overhead de transformación
- 🔧 **Mantenimiento:** Esquemas adicionales
- 💾 **Memoria:** Duplicación de datos

**Evaluación:** Costo/Beneficio pendiente según casos de uso futuros.

### **Configurabilidad:**
- ⚙️ Tolerancias de cálculo ajustables
- 🎛️ Activar/desactivar validaciones específicas
- 📋 Exportar reportes de validación

### **Validaciones Adicionales:**
- 📈 Tendencias entre archivos
- 🔍 Patrones de errores comunes
- 📊 Estadísticas de calidad de datos

### **Optimización:**
- 🚀 Detección más inteligente de estructura
- 🧠 Aprendizaje de patrones de tabla
- ⚡ Validación en paralelo para múltiples archivos

---

**El Sistema de Validación de Datos representa un auditor silencioso completo que garantiza la integridad matemática de los datos educativos, proporcionando confianza y transparencia en el proceso de análisis.**
