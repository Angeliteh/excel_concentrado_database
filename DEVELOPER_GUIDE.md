# 👨‍💻 GUÍA PARA DESARROLLADORES

## 🎯 Propósito de esta Guía

Esta guía te ayudará a **entender a profundidad** cómo funciona el sistema y cómo extenderlo de manera efectiva. Está diseñada para desarrolladores que necesiten:

- Entender la lógica interna del sistema
- Agregar nuevas funcionalidades
- Modificar comportamientos existentes
- Implementar validaciones internas
- Debuggear problemas complejos

## 🧠 Conceptos Fundamentales

### 🔄 Proceso Secuencial de 3 Pasos

El corazón del sistema es el **proceso secuencial** que transforma datos Excel en 3 etapas:

#### Paso 1: Vista Excel Original
```python
# En ExcelProcessor.extraer_datos_completo()
datos_combinados = self.crear_vista_combinada(datos_crudos)
# Resultado: DataFrame que replica exactamente cómo se ve en Excel
```

#### Paso 2: Vista con Marcadores
```python
# Datos con marcadores [valor] para celdas combinadas
datos_crudos = self.extraer_con_marcadores(hoja, rango)
# Ejemplo: "Juan" → "Juan", "[Juan]", "[Juan]" para celda combinada de 3 columnas
```

#### Paso 3: Datos Numéricos Puros
```python
# Solo valores numéricos para operaciones matemáticas
datos_numericos = self.extraer_datos_numericos(datos_crudos, config_numerico)
# Resultado: DataFrame (9, 19) con solo números
```

### 🗺️ Mapeo Posicional

**Concepto clave**: El sistema mantiene un mapeo exacto de dónde está cada dato:

```python
mapeo_posicional = {
    (fila, columna): {
        'valor_original': valor,
        'es_combinada': True/False,
        'rango_combinado': (inicio_fila, inicio_col, fin_fila, fin_col),
        'posicion_en_sumatoria': (nueva_fila, nueva_col)
    }
}
```

Este mapeo permite:
- Ubicar cualquier dato específico
- Saber si una celda está combinada
- Revertir marcadores para exportación
- Validar relaciones entre datos

## 🔧 Módulos Core - Análisis Profundo

### 📊 ExcelProcessor - El Cerebro del Sistema

**Ubicación**: `src/core/excel_processor.py`

#### Método Principal: `extraer_datos_completo()`

```python
def extraer_datos_completo(self, archivo_path):
    """
    FLUJO INTERNO:
    1. Carga Excel con openpyxl
    2. Detecta celdas combinadas
    3. Extrae datos con marcadores [valor]
    4. Crea vista combinada (reversión)
    5. Extrae datos numéricos puros
    6. Genera mapeo posicional
    """
```

#### Algoritmo de Marcadores (Crítico para entender):

```python
# Pseudocódigo del algoritmo
for cada_celda_combinada in rangos_combinados:
    valor_original = celda_principal.valor
    for cada_celda_secundaria in rango_combinado:
        marcar_como(f"[{valor_original}]")
    
# Resultado: 
# Celda principal: "Juan"
# Celdas secundarias: "[Juan]", "[Juan]", "[Juan]"
```

#### ¿Por qué este algoritmo?
- **Rastreabilidad**: Sabemos qué celdas estaban combinadas
- **Reversibilidad**: Podemos recrear la estructura original
- **Flexibilidad**: Funciona con cualquier tamaño de combinación

### 📁 DataManager - Gestión Inteligente

**Ubicación**: `src/core/data_manager.py`

#### Estructura de Datos Interna:

```python
self.archivos_procesados = {
    'archivo1.xlsx': {
        'archivo_completo': '/ruta/completa/archivo1.xlsx',
        'datos_crudos': DataFrame(12, 26),      # Con marcadores
        'datos_combinados': DataFrame(12, 26),   # Vista Excel
        'datos_numericos': DataFrame(9, 19),     # Solo números
        'mapeo_posicional': dict                 # Mapeo completo
    },
    'archivo2.xlsx': { ... }
}
```

#### Algoritmo de Sumatoria:

```python
def calcular_sumatoria(self):
    """
    LÓGICA INTERNA:
    1. Extrae datos_numericos de todos los archivos
    2. Verifica que tengan las mismas dimensiones
    3. Suma elemento por elemento (pandas)
    4. Maneja valores NaN y errores
    5. Retorna DataFrame consolidado
    """
    dataframes = [archivo['datos_numericos'] for archivo in self.archivos_procesados.values()]
    return sum(dataframes)  # Simplificado
```

### 📤 TemplateInjector - Inyección Precisa

**Ubicación**: `src/core/template_injector.py`

#### Algoritmo de Inyección (Complejo pero crucial):

```python
def inyectar_en_plantilla(self, datos_sumatoria, plantilla_path, archivo_destino):
    """
    PROCESO INTERNO:
    1. Carga plantilla con celdas combinadas intactas
    2. Mapea datos_sumatoria a rango H6:Z14
    3. Para cada celda de datos:
       - Verifica si está en rango combinado
       - Si SÍ: inyecta solo en celda principal
       - Si NO: inyecta directamente
    4. Preserva formato y estructura
    5. Guarda archivo final
    """
```

#### ¿Por qué es complejo?
- Debe preservar celdas combinadas de la plantilla
- Debe mapear correctamente datos de sumatoria
- Debe manejar diferentes tamaños de rangos combinados

## 🎨 Interfaz PyQt - Coordinación Maestra

### Flujo de Eventos en main.py

```python
# Flujo típico de procesamiento
def procesar_archivo(self, archivo):
    # 1. Delegar a DataManager
    datos_procesados = self.data_manager.procesar_archivo(archivo)
    
    # 2. Cargar datos para visualización
    self.datos_crudos = datos_procesados['datos_crudos']
    self.datos_combinados = datos_procesados['datos_combinados']
    self.datos_numericos = datos_procesados['datos_numericos']
    
    # 3. Inicializar proceso secuencial
    self.inicializar_proceso_secuencial()
```

### Visualización de Celdas Combinadas

```python
def aplicar_combinacion_celdas_proceso(self, dataframe):
    """
    MAGIA DE LA VISUALIZACIÓN:
    1. Analiza datos_crudos para encontrar marcadores [valor]
    2. Calcula spans necesarios para PyQt
    3. Aplica setSpan() en tabla
    4. Colorea según tipo (cyan=texto, amarillo=números)
    """
    for i, j in posiciones:
        if es_inicio_de_combinacion(i, j):
            span_count = calcular_span(i, j)
            self.tabla_proceso.setSpan(i, j, 1, span_count)
```

## 🔍 Debugging y Troubleshooting

### Logs Importantes

El sistema genera logs específicos que te ayudan a debuggear:

```python
# En ExcelProcessor
print(f"📊 Rangos combinados encontrados: {len(rangos_combinados)}")
print(f"✅ Datos extraídos con marcadores: {datos_crudos.shape}")

# En DataManager  
print(f"✅ Archivo procesado y agregado: {nombre_archivo}")

# En TemplateInjector
print(f"📤 Inyectando en rango: H{fila_inicio}:Z{fila_inicio + filas - 1}")
```

### Puntos de Verificación

Para debuggear problemas:

1. **Verificar extracción**: `datos_crudos.head(8).to_string()`
2. **Verificar combinación**: Buscar patrones `[valor]`
3. **Verificar numéricos**: `datos_numericos.shape` debe ser (9, 19)
4. **Verificar mapeo**: `len(mapeo_posicional)` debe ser ~171

### Errores Comunes

```python
# Error: Dimensiones incorrectas
if datos_numericos.shape != (9, 19):
    print("❌ Error: Configurar RANGOS_EXTRACCION['numerico']")

# Error: Celdas combinadas no detectadas
if len(rangos_combinados) == 0:
    print("❌ Error: Archivo sin celdas combinadas o protegido")

# Error: Mapeo incompleto
if len(mapeo_posicional) < 100:
    print("❌ Error: Mapeo posicional incompleto")
```

## 🚀 Extensión del Sistema

### Agregar Validaciones Internas (Tu próximo objetivo)

```python
# En ExcelProcessor, agregar método:
def validar_tabla_interna(self, datos_numericos):
    """
    Ejemplo: Validar que subtotales = suma de componentes
    """
    errores = []
    for fila in range(len(datos_numericos)):
        # Columna T (índice 12) = suma de H,J,L,N,P,R (índices 0,2,4,6,8,10)
        subtotal = datos_numericos.iloc[fila, 12]
        componentes = datos_numericos.iloc[fila, [0,2,4,6,8,10]].sum()
        
        if abs(subtotal - componentes) > 0.01:
            errores.append(f"Fila {fila}: {subtotal} ≠ {componentes}")
    
    return errores
```

### Agregar Nuevo Tipo de Archivo

```python
# 1. Extender configuración
RANGOS_EXTRACCION['nuevo_tipo'] = {
    'fila_inicio': X, 'fila_fin': Y,
    'columna_inicio': A, 'columna_fin': B
}

# 2. Modificar ExcelProcessor para detectar tipo
def detectar_tipo_archivo(self, hoja):
    # Lógica para detectar tipo de archivo
    pass

# 3. Usar configuración apropiada
config_rango = RANGOS_EXTRACCION[tipo_detectado]
```

## 💡 Tips de Desarrollo

### 1. Usar Configuración Centralizada
```python
# ❌ MAL
min_row = 3
max_row = 14

# ✅ BIEN  
from src.config.settings import RANGOS_EXTRACCION
config = RANGOS_EXTRACCION['principal']
min_row = config['fila_inicio']
```

### 2. Mantener Compatibilidad de Interfaces
```python
# Al modificar ExcelProcessor, mantener formato de retorno:
return {
    'datos_crudos': datos_crudos,
    'datos_combinados': datos_combinados,
    'datos_numericos': datos_numericos,
    'mapeo_posicional': mapeo_posicional
}
```

### 3. Logging Consistente
```python
print(f"📋 Procesando: {nombre_archivo}")  # Inicio
print(f"✅ Completado: {resultado}")       # Éxito  
print(f"❌ Error: {error}")               # Error
```

---

Con esta guía tienes todo lo necesario para entender y extender el sistema de manera profesional. ¡El código está listo para tus validaciones internas!
