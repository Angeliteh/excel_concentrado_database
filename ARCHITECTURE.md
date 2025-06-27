# 🏗️ ARQUITECTURA DEL SISTEMA

## 📋 Visión General

El sistema utiliza una **arquitectura modular ultra-limpia** resultado de una refactorización completa que redujo main.py de 858 a 216 líneas (75% reducción), separando responsabilidades en módulos especializados.

## 🎯 Principios de Diseño

### ✅ Separación Ultra-Modular
- **main.py** (216 líneas): Solo coordinación entre módulos
- **src/core/**: Lógica de negocio pura y reutilizable
- **src/gui/**: Módulos especializados de interfaz
- **src/config/**: Configuración centralizada

### ✅ Arquitectura por Capas
```
📦 CAPA DE COORDINACIÓN
└── main.py (216 líneas) - Solo coordinación

📦 CAPA DE INTERFAZ ESPECIALIZADA
├── TableVisualizer (250 líneas) - Visualización de datos
├── SequentialProcess (165 líneas) - Navegación de pasos
├── MainWindowUI (325 líneas) - Construcción de interfaz
├── FileManager (160 líneas) - Gestión de archivos
└── DataProcessor (160 líneas) - Procesamiento UI

📦 CAPA DE LÓGICA DE NEGOCIO
├── ExcelProcessor - Extracción de datos
├── DataManager - Gestión de datos
└── TemplateInjector - Exportación

📦 CAPA DE CONFIGURACIÓN
└── settings.py - Parámetros centralizados
```

### ✅ Beneficios Logrados
- Todos los parámetros en `settings.py`
- Sin valores hardcodeados en el código
- Fácil adaptación a diferentes estructuras

## 🔧 Componentes Principales

### 1. 🖥️ main.py - Coordinador Principal

**Responsabilidad**: Interfaz PyQt + coordinación de módulos

```python
class ExcelVisualizerApp(QMainWindow):
    def __init__(self):
        # Inicializar gestión modular
        from src.core.data_manager import DataManager
        self.data_manager = DataManager()
```

**Funciones clave**:
- `procesar_archivo()`: Coordina procesamiento individual
- `calcular_sumatoria_total()`: Coordina consolidación
- `exportar_a_plantilla()`: Coordina exportación
- `mostrar_paso()`: Maneja visualización secuencial

**Patrón**: Coordinador que delega a módulos especializados

### 2. 📊 ExcelProcessor - Extracción Especializada

**Ubicación**: `src/core/excel_processor.py`
**Responsabilidad**: Extracción y procesamiento de archivos Excel

```python
class ExcelProcessor:
    def extraer_datos_completo(self, archivo_path):
        # Retorna formato exacto esperado por interfaz
        return {
            'datos_crudos': datos_crudos,        # (12, 26) con [valor]
            'datos_combinados': datos_combinados, # (12, 26) vista Excel
            'datos_numericos': datos_numericos,   # (9, 19) solo números
            'mapeo_posicional': mapeo_posicional  # Dict posiciones
        }
```

**Algoritmo de marcadores `[valor]`**:
1. Detecta celdas combinadas en Excel
2. Marca celdas secundarias con `[valor_original]`
3. Mantiene valor original en celda principal
4. Genera mapeo posicional para reversión

**Características**:
- Manejo inteligente de celdas combinadas
- Generación de 3 vistas de datos
- Mapeo posicional preciso
- Configuración flexible de rangos

### 3. 📁 DataManager - Gestión Múltiple

**Ubicación**: `src/core/data_manager.py`
**Responsabilidad**: Manejo de múltiples archivos y operaciones

```python
class DataManager:
    def __init__(self):
        self.archivos_procesados = {}
        self.sumatoria_total = None
        self.processor = ExcelProcessor()
```

**Funciones principales**:
- `procesar_archivo()`: Procesa y almacena archivo individual
- `calcular_sumatoria()`: Suma DataFrames de múltiples archivos
- `limpiar_datos()`: Limpia toda la colección
- `eliminar_archivo()`: Elimina archivo específico

**Patrón**: Repository + Aggregate para gestión de colecciones

### 4. 📤 TemplateInjector - Exportación Inteligente

**Ubicación**: `src/core/template_injector.py`
**Responsabilidad**: Inyección en plantillas manteniendo formato

```python
class TemplateInjector:
    def inyectar_en_plantilla(self, datos_sumatoria, plantilla_path, archivo_destino):
        # Inyecta datos manteniendo celdas combinadas
```

**Algoritmo de inyección**:
1. Carga plantilla base con celdas combinadas
2. Mapea datos a posiciones específicas
3. Inyecta solo en celdas principales de rangos combinados
4. Preserva formato y estructura original

**Características**:
- Preservación de celdas combinadas
- Mapeo posicional inteligente
- Validación de plantilla
- Manejo de errores robusto

### 5. ⚙️ Settings - Configuración Centralizada

**Ubicación**: `src/config/settings.py`
**Responsabilidad**: Todas las configuraciones del sistema

```python
# Rangos de extracción
RANGOS_EXTRACCION = {
    'principal': {
        'fila_inicio': 3, 'fila_fin': 14,
        'columna_inicio': 1, 'columna_fin': 26
    },
    'numerico': {
        'filas_inicio': 3, 'filas_fin': 11,
        'columnas_inicio': 7, 'columnas_fin': 25
    }
}

# Rangos de inyección
RANGOS_INYECCION = {
    'plantilla_base': {
        'fila_inicio': 6,
        'columna_inicio': 8,  # Columna H
        'columna_fin': 26     # Columna Z
    }
}
```

**Ventajas**:
- Sin valores hardcodeados
- Fácil adaptación a nuevas estructuras
- Configuración por ambiente
- Rutas relativas para portabilidad

## 🔄 Flujo de Datos

### Procesamiento Individual
```
Excel File → ExcelProcessor → 3 DataFrames → DataManager → Storage
```

### Procesamiento Múltiple
```
Multiple Files → DataManager → ExcelProcessor (cada uno) → Collection → Sumatoria
```

### Exportación
```
Sumatoria → TemplateInjector → Plantilla Base → Archivo Final
```

## 🎨 Patrones de Diseño Utilizados

### 1. **Facade Pattern**
- `main.py` actúa como facade para módulos core
- Simplifica interfaz compleja para el usuario

### 2. **Strategy Pattern**
- Diferentes estrategias de procesamiento según tipo de archivo
- Configuración flexible de rangos

### 3. **Repository Pattern**
- `DataManager` como repository de archivos procesados
- Abstrae almacenamiento y operaciones de colección

### 4. **Template Method Pattern**
- Proceso secuencial con pasos bien definidos
- Cada paso puede ser customizado independientemente

## 🔧 Extensibilidad

### Agregar Nuevo Tipo de Procesamiento
1. Crear nueva clase en `src/core/`
2. Implementar interfaz compatible con `DataManager`
3. Configurar en `settings.py`
4. Integrar en `main.py`

### Agregar Validaciones Internas
1. Extender `ExcelProcessor` con métodos de validación
2. Usar mapeo posicional para ubicar datos específicos
3. Integrar en proceso secuencial
4. Mostrar resultados en interfaz

### Modificar Rangos de Datos
1. Actualizar `RANGOS_EXTRACCION` en `settings.py`
2. No requiere cambios en código
3. Sistema se adapta automáticamente

## 🛡️ Robustez y Manejo de Errores

### Validaciones
- Verificación de archivos antes de procesamiento
- Validación de plantillas antes de inyección
- Verificación de integridad de datos

### Recuperación de Errores
- Logs detallados para debugging
- Manejo graceful de archivos corruptos
- Rollback automático en operaciones críticas

## 📊 Performance

### Optimizaciones
- Carga lazy de módulos pesados
- Procesamiento en memoria para archivos múltiples
- Cache de configuraciones

### Escalabilidad
- Arquitectura preparada para procesamiento asíncrono
- Modularidad permite optimización independiente
- Configuración flexible para diferentes tamaños

---

Esta arquitectura garantiza **mantenibilidad**, **extensibilidad** y **robustez** para el crecimiento futuro del sistema.
