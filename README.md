# 📊 Sistema de Automatización Excel para Secretaría Escolar

## 🎯 Descripción

Sistema modular avanzado para automatizar el procesamiento de datos escolares desde archivos Excel. Diseñado específicamente para secretarías escolares que manejan múltiples archivos con estructuras complejas de celdas combinadas.

### ✨ Características Principales

- **🔄 Procesamiento Secuencial Visual**: 3 pasos con visualización en tiempo real
- **📁 Gestión Múltiple**: Procesa múltiples archivos simultáneamente
- **🧮 Sumatoria Automática**: Consolida datos de múltiples fuentes
- **📤 Exportación Inteligente**: Inyecta resultados en plantillas manteniendo formato
- **🎨 Manejo de Celdas Combinadas**: Preserva y manipula celdas combinadas de Excel
- **⚙️ Configuración Centralizada**: Fácil adaptación a diferentes rangos y estructuras

## 🏗️ Arquitectura Modular

```
📦 Sistema Principal
├── 🖥️ main.py                    # Interfaz PyQt + Coordinación
├── ⚙️ src/config/settings.py      # Configuraciones centralizadas
├── 🔧 src/core/                   # Módulos principales
│   ├── 📊 excel_processor.py     # Extracción y procesamiento
│   ├── 📁 data_manager.py        # Gestión múltiple de archivos
│   └── 📤 template_injector.py   # Exportación a plantillas
└── 🛠️ src/utils/excel_utils.py   # Utilidades Excel especializadas
```

## 🚀 Instalación y Configuración

### Requisitos del Sistema
- Python 3.8+
- PyQt5
- pandas
- openpyxl
- win32com.client (para funciones avanzadas de Excel)

### Instalación
```bash
# 1. Clonar el repositorio
git clone [tu-repositorio]
cd excel_concentrado_database

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el sistema
python main.py
```

## 📖 Uso del Sistema

### 🔄 Proceso Básico
1. **Cargar Archivos**: Individual o múltiple
2. **Visualizar Proceso**: 3 pasos secuenciales
3. **Calcular Sumatoria**: Consolidación automática
4. **Exportar Resultados**: A plantilla base

### 📋 Proceso Secuencial Detallado

#### Paso 1: Vista Excel Original
- Muestra datos tal como aparecen en Excel
- Celdas combinadas visualmente preservadas
- Colores diferenciados (cyan=texto, amarillo=números)

#### Paso 2: Vista Reorganizada
- Datos con marcadores `[valor]` para celdas combinadas
- Preparación para manipulación de datos
- Sombreado gris para identificar marcadores

#### Paso 3: Datos Numéricos
- Solo valores numéricos relevantes
- Listos para operaciones matemáticas
- Rango configurable (H3:Z11 por defecto)

## ⚙️ Configuración

Todas las configuraciones están centralizadas en `src/config/settings.py`:

```python
# Rangos de extracción
RANGOS_EXTRACCION = {
    'principal': {
        'fila_inicio': 3,
        'fila_fin': 14,
        'columna_inicio': 1,
        'columna_fin': 26
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

## 🔧 Funcionalidades Avanzadas

### 📊 Gestión de Celdas Combinadas
- **Detección automática** de rangos combinados
- **Marcadores `[valor]`** para rastreo de combinaciones
- **Reversión inteligente** para exportación
- **Mapeo posicional** preciso para inyección

### 🧮 Operaciones Matemáticas
- **Sumatoria automática** de múltiples archivos
- **Validación de integridad** de datos
- **Recálculo incremental** al agregar archivos
- **Manejo de valores nulos** y errores

### 📁 Gestión de Archivos
- **Carga individual** con vista previa
- **Carga múltiple** con barra de progreso
- **Selección de archivos** para visualización
- **Limpieza de datos** con un clic

## 🎨 Interfaz de Usuario

### Panel Izquierdo: Gestión de Archivos
- Botones de carga (individual/múltiple)
- Lista de archivos procesados
- Botón prominente de sumatoria
- Barra de progreso para múltiples archivos

### Panel Derecho: Proceso Secuencial
- Controles de navegación entre pasos
- Tabla principal con datos del paso actual
- Descripción detallada del paso
- Sección de sumatoria (cuando aplica)

## 📚 Documentación Técnica

Para desarrolladores que necesiten entender o extender el sistema:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura detallada del sistema
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Guía completa para desarrolladores
- **[API_REFERENCE.md](API_REFERENCE.md)** - Referencia de APIs de todos los módulos
- **[VALIDATION_GUIDE.md](VALIDATION_GUIDE.md)** - Cómo agregar validaciones internas

## 🔍 Casos de Uso

### Secretaría Escolar Típica
1. **Múltiples archivos** de diferentes zonas/períodos
2. **Estructuras complejas** con celdas combinadas
3. **Consolidación** en reportes únicos
4. **Validación** de consistencia de datos

### Flujo de Trabajo Recomendado
```
📁 Cargar archivos → 👁️ Revisar proceso → 🧮 Calcular → 📤 Exportar
```

## 🛠️ Mantenimiento y Extensión

### Agregar Nuevos Rangos
Modificar `src/config/settings.py`:
```python
RANGOS_EXTRACCION['nuevo_rango'] = {
    'fila_inicio': X,
    'fila_fin': Y,
    'columna_inicio': A,
    'columna_fin': B
}
```

### Agregar Validaciones
El sistema está preparado para validaciones internas:
- Ubicación precisa de cualquier dato
- Mapeo posicional completo
- Proceso secuencial para verificación

## 🐛 Solución de Problemas

### Problemas Comunes
- **Error de celdas combinadas**: Verificar que el archivo no esté protegido
- **Datos incorrectos**: Revisar configuración de rangos en settings.py
- **Exportación fallida**: Verificar que plantilla_base.xlsx existe

### Logs del Sistema
El sistema genera logs detallados en consola para debugging.

## 🤝 Contribución

Para contribuir al proyecto:
1. Revisar documentación técnica
2. Seguir arquitectura modular existente
3. Mantener configuraciones centralizadas
4. Documentar cambios apropiadamente

## 📄 Licencia

[Especificar licencia según necesidades]

---

**Desarrollado para automatizar procesos de secretaría escolar con máxima eficiencia y confiabilidad.**