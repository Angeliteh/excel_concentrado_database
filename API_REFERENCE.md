# 📚 REFERENCIA DE APIs

## 📋 Visión General

Esta referencia documenta todas las APIs públicas de los módulos del sistema. Úsala como referencia rápida para desarrollo y extensión.

## 🔧 src.core.excel_processor

### Clase: `ExcelProcessor`

Procesador centralizado para extracción y procesamiento de archivos Excel.

#### Constructor
```python
ExcelProcessor()
```
Inicializa el procesador sin parámetros.

#### Métodos Principales

##### `extraer_datos_completo(archivo_path: str) -> dict`

**Propósito**: Extrae y procesa datos completos de archivo Excel.

**Parámetros**:
- `archivo_path` (str): Ruta del archivo Excel a procesar

**Retorna**:
```python
{
    'datos_crudos': pandas.DataFrame,        # (12, 26) con marcadores [valor]
    'datos_combinados': pandas.DataFrame,    # (12, 26) vista Excel limpia
    'datos_numericos': pandas.DataFrame,     # (9, 19) solo números únicos
    'mapeo_posicional': dict                 # Mapeo de posiciones
}
```

**Ejemplo**:
```python
processor = ExcelProcessor()
resultado = processor.extraer_datos_completo("archivo.xlsx")
datos_numericos = resultado['datos_numericos']
```

**Configuración utilizada**:
- `RANGOS_EXTRACCION['principal']`: Rango completo de extracción
- `RANGOS_EXTRACCION['numerico']`: Rango de datos numéricos
- `NOMBRE_HOJAS['entrada']`: Nombre de la hoja a procesar

#### Métodos Internos (Avanzado)

##### `crear_vista_combinada(datos_crudos: DataFrame) -> DataFrame`
Crea vista Excel limpia revirtiendo marcadores [valor].

##### `extraer_datos_numericos(datos_crudos: DataFrame, config: dict) -> DataFrame`
Extrae solo datos numéricos del rango especificado.

##### `generar_mapeo_posicional(datos_crudos: DataFrame, datos_numericos: DataFrame) -> dict`
Genera mapeo completo de posiciones para inyección.

---

## 📁 src.core.data_manager

### Clase: `DataManager`

Gestor centralizado de datos de múltiples archivos.

#### Constructor
```python
DataManager()
```
Inicializa gestor con colección vacía.

#### Propiedades

##### `archivos_procesados: dict`
Diccionario con todos los archivos procesados:
```python
{
    'archivo.xlsx': {
        'archivo_completo': str,
        'datos_crudos': DataFrame,
        'datos_combinados': DataFrame, 
        'datos_numericos': DataFrame,
        'mapeo_posicional': dict
    }
}
```

#### Métodos Principales

##### `procesar_archivo(archivo_path: str) -> dict`

**Propósito**: Procesa archivo individual y lo agrega a la colección.

**Parámetros**:
- `archivo_path` (str): Ruta del archivo Excel

**Retorna**: Mismo formato que `ExcelProcessor.extraer_datos_completo()`

**Ejemplo**:
```python
data_manager = DataManager()
datos = data_manager.procesar_archivo("archivo.xlsx")
```

##### `calcular_sumatoria() -> pandas.DataFrame`

**Propósito**: Calcula sumatoria de todos los archivos procesados.

**Retorna**: DataFrame (9, 19) con suma consolidada

**Excepciones**:
- `ValueError`: Si hay menos de 2 archivos
- `ValueError`: Si las dimensiones no coinciden

**Ejemplo**:
```python
if len(data_manager.archivos_procesados) >= 2:
    sumatoria = data_manager.calcular_sumatoria()
```

##### `limpiar_datos()`
Limpia toda la colección de archivos procesados.

##### `eliminar_archivo(nombre_archivo: str) -> bool`
Elimina archivo específico de la colección.

#### Métodos Avanzados

##### `procesar_multiples_archivos(archivos_paths: list, callback_progreso=None)`
Procesa múltiples archivos con callback opcional de progreso.

##### `obtener_resumen_archivos() -> dict`
Retorna resumen estadístico de archivos procesados.

---

## 📤 src.core.template_injector

### Clase: `TemplateInjector`

Inyector especializado para exportación a plantillas Excel.

#### Constructor
```python
TemplateInjector()
```

#### Métodos Principales

##### `inyectar_en_plantilla(datos_sumatoria: DataFrame, plantilla_path: str, archivo_destino: str)`

**Propósito**: Inyecta datos en plantilla manteniendo formato.

**Parámetros**:
- `datos_sumatoria` (DataFrame): Datos a inyectar (9, 19)
- `plantilla_path` (str): Ruta de plantilla base
- `archivo_destino` (str): Ruta del archivo final

**Configuración utilizada**:
- `RANGOS_INYECCION['plantilla_base']`: Rango de inyección

**Ejemplo**:
```python
injector = TemplateInjector()
injector.inyectar_en_plantilla(
    sumatoria, 
    "plantilla_base.xlsx", 
    "resultado.xlsx"
)
```

**Excepciones**:
- `FileNotFoundError`: Si plantilla no existe
- `ValueError`: Si dimensiones no coinciden

##### `validar_plantilla(plantilla_path: str) -> dict`

**Propósito**: Valida que plantilla sea compatible.

**Retorna**:
```python
{
    'valida': bool,
    'mensaje': str,
    'rangos_combinados': int,
    'error': str  # Solo si valida=False
}
```

#### Métodos Internos

##### `mapear_datos_a_rango(datos: DataFrame, config_rango: dict) -> dict`
Mapea datos del DataFrame a posiciones específicas del rango.

##### `inyectar_preservando_combinadas(workbook, hoja, mapeo_datos: dict)`
Inyecta datos preservando estructura de celdas combinadas.

---

## ⚙️ src.config.settings

### Configuraciones Principales

#### `NOMBRE_HOJAS: dict`
```python
{
    'entrada': 'ZONA3',      # Hoja de entrada por defecto
    'salida': 'CONCENTRADO'  # Hoja de salida por defecto
}
```

#### `RANGOS_EXTRACCION: dict`
```python
{
    'principal': {
        'fila_inicio': 3, 'fila_fin': 14,
        'columna_inicio': 1, 'columna_fin': 26
    },
    'numerico': {
        'filas_inicio': 3, 'filas_fin': 11,
        'columnas_inicio': 7, 'columnas_fin': 25
    }
}
```

#### `RANGOS_INYECCION: dict`
```python
{
    'plantilla_base': {
        'fila_inicio': 6,
        'columna_inicio': 8,  # Columna H
        'columna_fin': 26     # Columna Z
    }
}
```

#### `INTERFAZ_CONFIG: dict`
Configuraciones de la interfaz PyQt (colores, tamaños, etc.)

### Funciones Utilitarias

##### `get_project_root() -> str`
Retorna ruta raíz del proyecto de forma segura.

##### `get_absolute_path(relative_path: str) -> str`
Convierte ruta relativa a absoluta basada en raíz del proyecto.

---

## 🛠️ src.utils.excel_utils

### Funciones Principales

##### `cargar_excel(archivo_path: str, nombre_hoja: str) -> Worksheet`

**Propósito**: Carga hoja específica de archivo Excel.

**Parámetros**:
- `archivo_path` (str): Ruta del archivo
- `nombre_hoja` (str): Nombre de la hoja

**Retorna**: Objeto Worksheet de openpyxl

**Ejemplo**:
```python
from src.utils.excel_utils import cargar_excel
hoja = cargar_excel("archivo.xlsx", "ZONA3")
```

##### `extraer_tabla_y_limpiar(hoja: Worksheet, rango: tuple) -> list`

**Propósito**: Extrae tabla de rango específico y limpia datos.

**Parámetros**:
- `hoja` (Worksheet): Hoja de Excel
- `rango` (tuple): (min_row, min_col, max_row, max_col)

**Retorna**: Lista de listas con datos limpios

### Funciones Avanzadas

##### `inyectar_datos_en_plantilla(df: DataFrame, hoja: Worksheet, rango_inyeccion: tuple)`
Inyecta DataFrame en hoja respetando celdas combinadas.

##### `inyectar_formulas_totales_y_subtotales(archivo_salida: str, hoja_nombre: str, fila_inicial: int, fila_final: int)`
Inyecta fórmulas de totales y subtotales.

---

## 🎯 Patrones de Uso Comunes

### Procesamiento Completo
```python
# 1. Procesar archivo
from src.core.data_manager import DataManager
data_manager = DataManager()
datos = data_manager.procesar_archivo("archivo.xlsx")

# 2. Calcular sumatoria (si hay múltiples)
if len(data_manager.archivos_procesados) >= 2:
    sumatoria = data_manager.calcular_sumatoria()

# 3. Exportar resultado
from src.core.template_injector import TemplateInjector
injector = TemplateInjector()
injector.inyectar_en_plantilla(sumatoria, "plantilla.xlsx", "resultado.xlsx")
```

### Validación de Datos
```python
# Acceder a datos específicos para validación
datos_numericos = data_manager.archivos_procesados['archivo.xlsx']['datos_numericos']

# Validar subtotales (ejemplo)
for fila in range(len(datos_numericos)):
    subtotal = datos_numericos.iloc[fila, 12]  # Columna T
    componentes = datos_numericos.iloc[fila, [0,2,4,6,8,10]].sum()
    if abs(subtotal - componentes) > 0.01:
        print(f"Error en fila {fila}")
```

### Configuración Personalizada
```python
# Modificar rangos dinámicamente
from src.config.settings import RANGOS_EXTRACCION
RANGOS_EXTRACCION['personalizado'] = {
    'fila_inicio': 5, 'fila_fin': 20,
    'columna_inicio': 3, 'columna_fin': 30
}
```

---

Esta referencia cubre todas las APIs públicas del sistema. Para detalles de implementación, consulta [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md).
