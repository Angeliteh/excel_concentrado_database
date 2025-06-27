# 📋 PLAN ESTRATÉGICO DE REFACTORIZACIÓN

## 🔍 ANÁLISIS DEL SISTEMA ACTUAL (FUNCIONA PERFECTAMENTE)

### 📊 FLUJO DE PROCESAMIENTO EXITOSO:

```
📋 Procesando: archivo.xlsx
├── 📋 Extrayendo datos con marcadores [valor]...
│   ├── ✅ Hoja cargada: ZONA3
│   ├── 🔍 Extrayendo rango A3:Z14 con marcadores [valor]...
│   ├── 📊 Rangos combinados encontrados: 110
│   └── ✅ Datos extraídos con marcadores: (12, 26)
├── 🎨 Creando vista combinada (reversión)...
│   └── ✅ Vista combinada creada: (12, 26)
├── 🔢 Extrayendo datos numéricos con mapeo posicional...
│   ├── 📊 Configuración: Filas 3-11, Columnas 7-25
│   ├── ✅ Datos numéricos extraídos: (9, 19)
│   └── 📍 Mapeo posicional creado: 171 posiciones
└── 🔄 Inicializando proceso secuencial...
    ├── ✅ Datos preparados: Paso 1: (12, 26), Paso 2: (12, 26), Paso 3: (9, 19)
    └── 📋 Mostrando Vista Excel Original...
```

### 🎯 COMPONENTES CRÍTICOS QUE NO PODEMOS ROMPER:

#### 1. **EXTRACCIÓN DE DATOS (main_pyqt.py líneas ~350-620)**
```python
def extraer_datos(self):
    # CRÍTICO: Esta función produce 3 DataFrames exactos
    self.datos_crudos      # (12, 26) - Con [valor] marcadores
    self.datos_combinados  # (12, 26) - Vista Excel limpia  
    self.datos_numericos   # (9, 19)  - Solo números únicos
    self.mapeo_posicional  # Dict con 171 posiciones
```

#### 2. **VISUALIZACIÓN SECUENCIAL (líneas ~650-850)**
```python
def mostrar_paso1():  # Vista Excel + combinación + colores cyan/amarillo
def mostrar_paso2():  # Vista [valor] + sombreado gris
def mostrar_paso3():  # Datos numéricos únicos
def aplicar_combinacion_celdas_proceso():  # CRÍTICO: setSpan() + colores
```

#### 3. **GESTIÓN MÚLTIPLE (líneas ~200-350)**
```python
self.archivos_procesados = {}  # Almacena todos los datos
def calcular_sumatoria_total():  # Suma DataFrames
def exportar_a_plantilla():     # Inyección con mapeo
```

## 🚨 ERRORES COMUNES EN REFACTORIZACIONES ANTERIORES:

### ❌ **Error 1: Cambiar Estructura de Datos**
- **Problema**: Los módulos devuelven datos en formato diferente
- **Resultado**: Visualización se rompe porque espera formato específico

### ❌ **Error 2: Modificar Lógica de Extracción**
- **Problema**: Cambiar algoritmo de marcadores [valor]
- **Resultado**: Datos incorrectos → visualización incorrecta

### ❌ **Error 3: Alterar Flujo Secuencial**
- **Problema**: Cambiar orden o estructura de pasos
- **Resultado**: Navegación se rompe

## ✅ ESTRATEGIA SEGURA DE REFACTORIZACIÓN

### 🎯 **FASE 1: EXTRACCIÓN SIN CAMBIOS (SEMANA 1)**

#### Objetivo: Mover lógica de extracción manteniendo interfaz exacta

```python
# ANTES (main_pyqt.py):
def extraer_datos(self):
    # 200 líneas de lógica compleja aquí
    
# DESPUÉS (main_pyqt.py):
def extraer_datos(self):
    # Usar módulo pero mantener interfaz exacta
    processor = ExcelProcessor()
    resultado = processor.extraer_datos_completo(self.archivo_actual)
    
    # MANTENER VARIABLES EXACTAS
    self.datos_crudos = resultado['datos_crudos']
    self.datos_combinados = resultado['datos_combinados'] 
    self.datos_numericos = resultado['datos_numericos']
    self.mapeo_posicional = resultado['mapeo_posicional']
```

#### Pasos Seguros:
1. ✅ Crear `ExcelProcessor.extraer_datos_completo()` que devuelva formato exacto
2. ✅ Reemplazar contenido de `extraer_datos()` pero mantener interfaz
3. ✅ Probar que logs sean idénticos
4. ✅ Probar que visualización funcione igual

### 🎯 **FASE 2: GESTIÓN DE ARCHIVOS (SEMANA 2)**

#### Objetivo: Mover gestión múltiple manteniendo comportamiento

```python
# ANTES:
self.archivos_procesados = {}
def calcular_sumatoria_total():
    # lógica aquí

# DESPUÉS:
self.data_manager = DataManager()
def calcular_sumatoria_total():
    self.sumatoria_total = self.data_manager.calcular_sumatoria()
    # resto igual
```

### 🎯 **FASE 3: EXPORTACIÓN (SEMANA 3)**

#### Objetivo: Mover inyección manteniendo funcionalidad

```python
# ANTES:
def exportar_a_plantilla():
    # lógica compleja de inyección

# DESPUÉS:  
def exportar_a_plantilla():
    self.template_injector.inyectar_en_plantilla(...)
    # resto de interfaz igual
```

### 🎯 **FASE 4: LIMPIEZA FINAL (SEMANA 4)**

#### Objetivo: Eliminar código duplicado y optimizar

## 🛡️ VALIDACIONES EN CADA FASE:

### ✅ **Tests de Regresión Obligatorios:**

1. **Test de Logs**: Los logs deben ser 100% idénticos
2. **Test de Datos**: DataFrames deben tener forma y contenido exacto
3. **Test de Visualización**: Colores, combinación, navegación igual
4. **Test de Funcionalidad**: Carga, sumatoria, exportación igual

### 📊 **Métricas de Éxito:**
- ✅ Logs idénticos línea por línea
- ✅ Visualización pixel-perfect
- ✅ Funcionalidad 100% preservada
- ✅ Performance igual o mejor

## 🚀 IMPLEMENTACIÓN FASE 1

### **Paso 1.1: Crear ExcelProcessor Compatible**

```python
class ExcelProcessor:
    def extraer_datos_completo(self, archivo_path):
        """
        DEBE devolver formato EXACTO que espera main_pyqt.py
        """
        # Copiar lógica exacta de main_pyqt.py líneas 350-620
        # NO cambiar algoritmos
        # NO cambiar estructura de datos
        # SOLO mover código
        
        return {
            'datos_crudos': datos_crudos,        # (12, 26)
            'datos_combinados': datos_combinados, # (12, 26)  
            'datos_numericos': datos_numericos,   # (9, 19)
            'mapeo_posicional': mapeo_posicional  # Dict 171 items
        }
```

### **Paso 1.2: Reemplazar en main_pyqt.py**

```python
def extraer_datos(self):
    """Mantener interfaz exacta, usar módulo internamente"""
    from src.core.excel_processor import ExcelProcessor
    
    processor = ExcelProcessor()
    resultado = processor.extraer_datos_completo(self.archivo_actual)
    
    # MANTENER VARIABLES EXACTAS (no cambiar nombres)
    self.datos_crudos = resultado['datos_crudos']
    self.datos_combinados = resultado['datos_combinados']
    self.datos_numericos = resultado['datos_numericos'] 
    self.mapeo_posicional = resultado['mapeo_posicional']
    
    # MANTENER PRINTS EXACTOS para validar
    print("📋 DATOS CRUDOS (con celdas combinadas marcadas con []):")
    print(self.datos_crudos.head(8).to_string())
    # ... resto de prints iguales
```

### **Paso 1.3: Validación Estricta**

```bash
# Ejecutar ambas versiones y comparar logs
python main_pyqt.py > logs_original.txt 2>&1
python main_pyqt_fase1.py > logs_fase1.txt 2>&1
diff logs_original.txt logs_fase1.txt

# DEBE ser idéntico o ROLLBACK inmediato
```

## 📋 CRONOGRAMA DETALLADO

### **Semana 1: Extracción**
- Día 1-2: Crear ExcelProcessor compatible
- Día 3-4: Reemplazar en main_pyqt.py
- Día 5-7: Testing exhaustivo y ajustes

### **Semana 2: Gestión Múltiple**  
- Día 1-2: Crear DataManager compatible
- Día 3-4: Reemplazar gestión de archivos
- Día 5-7: Testing y validación

### **Semana 3: Exportación**
- Día 1-2: Crear TemplateInjector compatible  
- Día 3-4: Reemplazar exportación
- Día 5-7: Testing completo

### **Semana 4: Limpieza**
- Día 1-3: Eliminar código duplicado
- Día 4-5: Optimizaciones
- Día 6-7: Testing final y documentación

## 🎯 CRITERIOS DE ÉXITO FINAL

✅ **Funcionalidad**: 100% idéntica
✅ **Performance**: Igual o mejor  
✅ **Mantenibilidad**: Código modular
✅ **Escalabilidad**: Fácil agregar features
✅ **Estabilidad**: Sin regresiones

## ⚠️ CRITERIOS DE ROLLBACK

❌ **Cualquier diferencia en logs**
❌ **Cualquier cambio en visualización**  
❌ **Cualquier pérdida de funcionalidad**
❌ **Performance significativamente peor**

---

**REGLA DE ORO**: Si algo se rompe, ROLLBACK inmediato y reanalizar.
