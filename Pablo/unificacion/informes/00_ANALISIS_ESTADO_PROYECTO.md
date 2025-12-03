# ANÁLISIS PROFUNDO DEL ESTADO ACTUAL DEL PROYECTO
## Predicción del Precio del Oro y Análisis de Sentimientos de Noticias Financieras

**Fecha de Análisis:** 1 de Diciembre de 2025  
**Analista:** GitHub Copilot  
**Tipo de Documento:** Informe Técnico de Evaluación de Proyecto

---

## RESUMEN EJECUTIVO

Este documento presenta un análisis exhaustivo y científico del estado actual del proyecto de investigación sobre la predicción del precio del oro mediante técnicas de aprendizaje profundo y análisis de sentimientos de noticias financieras. El proyecto se encuentra en una fase avanzada de desarrollo, con componentes individuales implementados por diferentes integrantes del equipo, lo que ha resultado en una estructura modular que requiere unificación e integración.

---

## 1. OBJETIVOS DEL PROYECTO

### 1.1 Objetivos Principales

1. **Extracción de Datos:** Obtener bases de datos del precio del oro y noticias relacionadas desde 2016 hasta 2025 con resolución temporal diaria.

2. **Análisis Exploratorio de Datos (EDA):** Realizar un análisis estadístico profundo de las bases de datos obtenidas.

3. **Modelado Predictivo:** Desarrollar modelos de redes neuronales y/o machine learning para predecir el precio del oro y determinar su porcentaje de acierto.

4. **Análisis de Sentimientos:** Aplicar técnicas de procesamiento de lenguaje natural para determinar la positividad/negatividad de las noticias e identificar las más impactantes.

5. **Detección de Anomalías:** Analizar la curva de precios del oro para identificar puntos anómalos y determinar si coinciden con noticias impactantes.

6. **Análisis de Causalidad:** Determinar si existe causalidad entre las noticias y los puntos anómalos, evaluando un criterio de estabilidad de precios según el factor desestabilizante de las noticias.

---

## 2. INVENTARIO DE COMPONENTES DESARROLLADOS

### 2.1 Scripts y Archivos de Código

#### 2.1.1 `Extraccion_Datos` (Script Python)

**Ubicación:** `/home/els4nchez/Videos/TECH/Extraccion_Datos`

**Descripción:**
- Script ejecutable Python para descarga automatizada de datos de precios del oro desde la API de Dukascopy
- Implementación profesional con manejo de errores, procesamiento paralelo y configuración interactiva

**Funcionalidades:**
- Descarga de datos históricos de XAU-USD (Oro), XTI-USD (Petróleo WTI) y UKOIL (Brent)
- Configuración flexible de períodos temporales (años, meses, días)
- Múltiples resoluciones temporales: segundos, minutos, horas, días
- Procesamiento paralelo con ThreadPoolExecutor (máximo 12 workers)
- Aggregación de ticks a barras OHLCV (Open, High, Low, Close, Volume)
- Exportación a Excel (.xlsx) o CSV (.csv)
- Opciones de agrupación: por día, mes, año o rango completo
- Manejo robusto de interrupciones (Ctrl+C) y errores de red
- Retry strategy con backoff exponencial

**Fortalezas:**
- Código bien estructurado y profesional
- Uso eficiente de NumPy para operaciones vectorizadas
- Connection pooling para optimización de rendimiento
- Documentación clara en código

**Debilidades Identificadas:**
- No está organizado como módulo reutilizable (todo en un script)
- Falta documentación externa (README, docstrings formales)
- No genera metadatos sobre las descargas realizadas

#### 2.1.2 `filtrado_noticias.py`

**Ubicación:** `/home/els4nchez/Videos/TECH/filtrado_noticias.py`

**Descripción:**
- Script para filtrado y procesamiento de artículos del Wall Street Journal
- Objetivo: limpiar y organizar datos de noticias extraídas

**Funcionalidades:**
- Carga de archivo CSV de hipervínculos
- Filtrado por patrón URL específico: `/articles/.*-\d+$`
- Eliminación de duplicados basados en URL
- Conversión y validación de fechas
- Ordenamiento temporal
- Exportación a CSV procesado

**Fortalezas:**
- Uso correcto de pandas para manipulación de datos
- Manejo de errores con `errors='coerce'` en conversión de fechas
- Lógica clara y directa

**Debilidades Identificadas:**
- Usa rutas relativas con `../data/` que no coinciden con estructura actual
- Variables hardcodeadas (nombres de archivos)
- Falta configuración para diferentes fuentes de noticias
- No genera estadísticas de procesamiento

### 2.2 Notebooks de Análisis

#### 2.2.1 `AU_Exploratorio_V2.ipynb`

**Objetivo:** Análisis Exploratorio de Datos del precio del oro

**Contenido:**
1. **Carga de Datos:** Importación de `XAU_USD_2016-2025_01-12_1h_bars.csv` (54,118 registros con resolución horaria)

2. **Limpieza de Datos:**
   - Eliminación del sufijo " UTC" en columna de fechas
   - Conversión de formato DD.MM.YYYY HH:MM:SS a datetime
   - Establecimiento de índice temporal

3. **Análisis Descriptivo:**
   - Estadísticas descriptivas (describe, info, shape)
   - Verificación de valores nulos
   - Análisis de valores únicos por columna

4. **Análisis Estadístico:**
   - Cálculo de correlaciones entre variables
   - Visualización con heatmap
   - Pairplot para relaciones bivariadas
   - Box plots para identificación de outliers

5. **Detección de Outliers:**
   - Método IQR (Rango Intercuartílico) aplicado a: Open, High, Low, Close, Volume
   - Visualización temporal de outliers
   - Separación de datos en:
     * `df_outliers`: Fechas y valores de movimientos extremos
     * `df_AU_limpio_para_LSTM`: Dataset limpio para entrenamiento

6. **Extracción de Fechas Clave:**
   - Lista de fechas/horas con outliers
   - Fechas redondeadas al día para búsqueda de noticias

**Fortalezas:**
- Metodología sólida de identificación de outliers (IQR)
- Buena separación entre datos de entrenamiento y anomalías
- Visualizaciones comprehensivas
- Documentación bilingüe (español/inglés)

**Debilidades Identificadas:**
- No hay análisis de estacionariedad (crucial para series temporales)
- Falta prueba de Dickey-Fuller aumentada (ADF)
- No se realiza descomposición de series temporales (tendencia, estacionalidad, residuo)
- Importa ARIMA pero no lo utiliza
- No genera archivos de salida con outliers identificados
- Falta marco teórico sobre criterios de outliers

**Discrepancias:**
- Usa ruta de Google Colab (`/content/drive/MyDrive/`) incompatible con estructura local
- Resolución temporal horaria cuando el objetivo es DIARIA

#### 2.2.2 `ModeloOro.ipynb`

**Objetivo:** Desarrollo de modelos predictivos del precio del oro

**Contenido:**

1. **Preparación de Datos:**
   - Carga de datos horarios
   - Limpieza de formato UTC
   - Verificación de completitud temporal (24 horas por día)
   - **Resampleado a frecuencia diaria:**
     * Open: primer valor del día
     * High: máximo del día
     * Low: mínimo del día
     * Close: último valor del día
     * Volume: suma del día
   - Forward fill para valores faltantes
   - División temporal: Train (2016-2023), Test (2024-2025)

2. **Modelo LSTM Univariado:**
   - **Arquitectura:**
     * Entrada: ventana de 80 días previos
     * LSTM(256) + Dropout(0.2)
     * LSTM(128) + Dropout(0.2)
     * LSTM(64) + Dropout(0.2)
     * Dense(1)
   - **Entrenamiento:**
     * Optimizador: Adam
     * Función de pérdida: MSE
     * Métricas: MSE, MAE, MAPE
     * Early stopping (patience=5, min_delta=0.001)
     * Batch size: 32, Epochs: hasta 30
   - **Normalización:** MinMaxScaler (0,1)
   - **Evaluación:**
     * RMSE, MAE, R², MAPE
     * Visualización de predicciones vs valores reales

3. **Modelo LSTM Multivariado:**
   - **Variables:** Close + Volume
   - **Arquitectura idéntica** ajustando input_shape
   - **Mismo protocolo de entrenamiento**
   - Comparación de métricas con modelo univariado

**Fortalezas:**
- Arquitectura LSTM bien diseñada con regularización (Dropout)
- Early stopping para prevenir overfitting
- Evaluación exhaustiva con múltiples métricas
- Comparación univariado vs multivariado
- Resampleado correcto a frecuencia diaria

**Debilidades Identificadas:**
- No realiza búsqueda de hiperparámetros (GridSearch/RandomSearch)
- No valida supuestos del modelo (residuos, autocorrelación)
- Falta conjunto de validación (solo train/test)
- No guarda modelos entrenados para reproducibilidad
- No implementa cross-validation temporal (time series split)
- Falta análisis de importancia de features
- No compara con modelos baseline (ARIMA, Prophet, persistencia)
- Visualizaciones sin intervalos de confianza

**Discrepancias:**
- Lee archivo con ruta relativa simple (no Google Drive)
- No integra análisis de outliers del notebook exploratorio

#### 2.2.3 `Analisis_de_impacto.ipynb`

**Objetivo:** Análisis de sentimientos de noticias sobre oro y correlación con precios

**Contenido:**

1. **Carga de Datos:**
   - Importación de `articulos_filtrados_ordenados.csv`
   - Dataset: 188,469 artículos con título, URL y fecha

2. **Filtrado de Noticias Relevantes:**
   - **Palabras clave definidas (25 términos bilingües):**
     * Inglés: gold price, precious metals, inflation, central bank, bullion, safe haven, commodity, gold standard, gold futures, etc.
     * Español: precio oro, metal precioso, inflación, banco central, refugio seguro, oro físico, etc.
   - **Preprocesamiento:**
     * Conversión a minúsculas
     * Eliminación de puntuación (preservando caracteres unicode)
   - **Resultado:** 5,464 artículos relevantes (2.9% del total)

3. **Análisis de Sentimientos:**
   - **Modelo:** `finiteautomata/beto-sentiment-analysis` (BETO - BERT en español)
   - **Pipeline:** Transformers de HuggingFace
   - **Clasificación:** POS (Positivo), NEG (Negativo), NEU (Neutral)
   - **Métricas:** Label + Score de confianza
   
4. **Distribución de Sentimientos:**
   - **Resultados:**
     * Neutral: ~81%
     * Negativo: ~16%
     * Positivo: ~3%
   - Visualización con barplot de Seaborn

5. **Interpretación:**
   - Análisis sobre predominancia de noticias neutrales/informativas
   - Reflexión sobre sentimiento negativo en contexto económico
   - Baja frecuencia de noticias altamente optimistas

**Fortalezas:**
- Uso de modelo BERTO state-of-the-art para español
- Palabras clave comprehensivas bilingües
- Preprocesamiento adecuado con regex
- Visualizaciones claras
- Análisis interpretativo de resultados

**Debilidades Identificadas:**
- **CRÍTICO:** Usa modelo en ESPAÑOL sobre títulos en INGLÉS (WSJ)
- No valida idioma de los textos antes de aplicar modelo
- No extrae el contenido completo de artículos (solo títulos)
- Falta análisis temporal de sentimientos
- No correlaciona sentimientos con movimientos de precios
- No identifica noticias más impactantes cuantitativamente
- No implementa agregación temporal de sentimientos
- Falta validación manual de clasificaciones (ground truth)

**Discrepancias:**
- Usa ruta de Google Colab incompatible con estructura local
- Dataset de entrada diferente al generado por `filtrado_noticias.py`
- No se conecta con outliers identificados en `AU_Exploratorio_V2.ipynb`
- **ERROR FUNDAMENTAL:** Modelo español aplicado a texto inglés

### 2.3 Bases de Datos

#### 2.3.1 Datos de Precios

**Archivo:** `datos_horas/XAU_USD_2016-2025_01-12_1h_bars.csv`

**Características:**
- **Registros:** 54,118 barras horarias
- **Período:** 03/01/2016 23:00 UTC hasta 12/01/2025 (estimado)
- **Columnas:**
  * UTC: Timestamp con formato DD.MM.YYYY HH:MM:SS UTC
  * Open: Precio de apertura
  * High: Precio máximo
  * Low: Precio mínimo
  * Close: Precio de cierre
  * Volume: Volumen negociado
- **Rango de Precios:** ~$1,062 - ~$2,800+ (aproximado del período)

**Observaciones:**
- Datos de alta calidad desde API profesional (Dukascopy)
- Cobertura temporal completa
- **Resolución horaria NO coincide con objetivo de resolución diaria**

#### 2.3.2 Datos de Noticias

**Archivo Principal:** `articulos_filtrados_ordenados.csv`

**Características:**
- **Registros:** 189,456 artículos
- **Período:** 01/01/2016 - fecha reciente
- **Columnas:**
  * titulo: Título del artículo
  * url: URL del artículo
  * fecha: Fecha de publicación (formato YYYY-MM-DD)
- **Fuente:** Wall Street Journal (WSJ)

**Archivo Secundario:** `articulos_con_fechas_final.csv`

**Características:**
- Versión extendida con múltiples columnas de fecha:
  * fecha_publicacion: Formato "MMM DD, YYYY HH:MM AM/PM ET"
  * fecha_corta: Formato "MMM DD, YYYY"
  * timestamp: Unix timestamp
  * fecha_iso: Formato ISO 8601
  * metodo: Método de extracción (url_timestamp)

**Archivo Raw:** `hipervinculos_wsj.csv`

**Características:**
- **Registros:** 295,677 enlaces
- Incluye enlaces de navegación, secciones, artículos
- Requiere filtrado extensivo

**Observaciones:**
- **CRÍTICO:** Artículos del WSJ están en INGLÉS
- Buena cobertura temporal alineada con datos de precios
- Necesita extracción de contenido completo (actualmente solo títulos)
- Fechas en múltiples formatos requieren normalización

---

## 3. ANÁLISIS DE LOGROS

### 3.1 Objetivos Cumplidos

#### ✅ Objetivo 1: Extracción de Bases de Datos

**Estado:** COMPLETADO

**Evidencia:**
- Script `Extraccion_Datos` funcional y robusto
- Dataset de precios con 54,118 registros (2016-2025)
- Dataset de noticias con 189,456 artículos (2016-2025)

**Observación:**
- Resolución temporal de precios es HORARIA (más granular que lo requerido)
- Puede agregarse fácilmente a diaria

#### ✅ Objetivo 2: Análisis Exploratorio de Datos

**Estado:** PARCIALMENTE COMPLETADO

**Evidencia:**
- Notebook `AU_Exploratorio_V2.ipynb` con análisis completo de precios
- Estadísticas descriptivas, correlaciones, visualizaciones
- Identificación de outliers con método IQR

**Faltante:**
- Análisis de estacionariedad
- Descomposición de series temporales
- Análisis exploratorio unificado de noticias

#### ✅ Objetivo 3: Modelo Predictivo

**Estado:** COMPLETADO

**Evidencia:**
- Notebook `ModeloOro.ipynb` con dos arquitecturas LSTM
- Métricas de evaluación: RMSE, MAE, R², MAPE
- Comparación univariado vs multivariado

**Observación:**
- Falta comparación con modelos baseline
- No hay validación cruzada temporal
- Sin optimización de hiperparámetros

#### ✅ Objetivo 4: Análisis de Sentimientos

**Estado:** COMPLETADO CON ERROR CRÍTICO

**Evidencia:**
- Notebook `Analisis_de_impacto.ipynb` con análisis completo
- Filtrado de 5,464 artículos relevantes
- Clasificación en 3 categorías (POS/NEG/NEU)

**Error Crítico:**
- **Modelo BETO (español) aplicado a títulos en INGLÉS**
- Resultados NO son válidos científicamente

### 3.2 Objetivos Pendientes

#### ❌ Objetivo 5: Detección de Anomalías y Correlación con Noticias

**Estado:** NO COMPLETADO

**Evidencia:**
- `AU_Exploratorio_V2.ipynb` identifica outliers pero no correlaciona con noticias
- `Analisis_de_impacto.ipynb` analiza sentimientos pero no correlaciona con precios
- **NO EXISTE INTEGRACIÓN entre ambos análisis**

**Requerimiento:**
- Vincular fechas de outliers con noticias del mismo período
- Análisis estadístico de correlación

#### ❌ Objetivo 6: Análisis de Causalidad

**Estado:** NO COMPLETADO

**Evidencia:**
- No hay análisis de causalidad de Granger
- No hay evaluación de impacto de sentimiento en volatilidad
- No hay criterio cuantitativo de "estabilidad" definido

**Requerimiento:**
- Test de Granger Causality
- Análisis de función de respuesta al impulso (IRF)
- Definición y medición de "factor desestabilizante"

---

## 4. DISCREPANCIAS IDENTIFICADAS

### 4.1 Discrepancias de Resolución Temporal

| Componente | Resolución Actual | Resolución Objetivo | Impacto |
|-----------|------------------|-------------------|---------|
| Datos de precios | Horaria (54,118 registros) | Diaria | Bajo - Fácil agregación |
| Noticias | Diaria (exacta) | Diaria | ✓ Correcto |
| Modelo LSTM | Usa datos diarios resampleados | Diaria | ✓ Correcto |

**Solución:** Agregación ya implementada en `ModeloOro.ipynb`

### 4.2 Discrepancias de Idioma

| Componente | Idioma Datos | Modelo/Análisis | Validez Científica |
|-----------|-------------|----------------|-------------------|
| Noticias WSJ | Inglés | BETO (español) | ❌ INVÁLIDO |
| Palabras clave | Bilingüe | Búsqueda textual | ⚠️ Parcialmente válido |

**Impacto Crítico:**
- Análisis de sentimientos actual NO es científicamente válido
- Requiere re-ejecución con modelo en inglés (ej: `cardiffnlp/twitter-roberta-base-sentiment`)

### 4.3 Discrepancias de Rutas y Compatibilidad

| Archivo | Ruta Esperada | Ruta Real | Problema |
|---------|--------------|----------|----------|
| `AU_Exploratorio_V2.ipynb` | Google Colab Drive | Local | Hardcoded |
| `Analisis_de_impacto.ipynb` | Google Colab Drive | Local | Hardcoded |
| `filtrado_noticias.py` | `../data/` | Raíz proyecto | No existe carpeta |
| `ModeloOro.ipynb` | Relativa simple | Raíz proyecto | ✓ Funcional |

**Solución:** Estandarizar rutas relativas o usar pathlib

### 4.4 Discrepancias de Integración

**Desconexiones Identificadas:**

1. **Outliers ↔ Noticias:**
   - `AU_Exploratorio_V2.ipynb` genera lista de fechas con outliers
   - `Analisis_de_impacto.ipynb` tiene dataset completo de noticias
   - **NO HAY CÓDIGO que vincule ambos**

2. **Sentimientos ↔ Modelo Predictivo:**
   - Análisis de sentimientos completo
   - Modelo LSTM funcional
   - **NO SE INTEGRA sentimiento como feature predictora**

3. **Datasets:**
   - `articulos_filtrados_ordenados.csv` (189,456 artículos)
   - `articulos_con_fechas_final.csv` (metadata extendida)
   - **NO ESTÁ CLARO cuál es la versión canónica**

---

## 5. ANÁLISIS DE COHERENCIA METODOLÓGICA

### 5.1 Fortalezas Metodológicas

1. **Datos de Precios:**
   - Fuente profesional (Dukascopy API)
   - Cobertura temporal completa (9+ años)
   - Alta frecuencia permite múltiples análisis

2. **Modelo LSTM:**
   - Arquitectura apropiada para series temporales
   - Uso correcto de ventanas temporales
   - Normalización adecuada
   - División temporal Train/Test

3. **Detección de Outliers:**
   - Método estadístico robusto (IQR)
   - Separación de datos limpios vs anomalías
   - Visualización clara

### 5.2 Debilidades Metodológicas

1. **Falta de Marco Teórico Formal:**
   - No hay justificación de por qué LSTM vs otros modelos
   - No hay explicación de criterios de outlier
   - Falta fundamentación teórica de causalidad noticia → precio

2. **Validación Insuficiente:**
   - No hay conjunto de validación en LSTM
   - No hay cross-validation temporal
   - No hay análisis de residuos
   - No hay test de significancia estadística

3. **Reproducibilidad Limitada:**
   - Seeds aleatorios no fijados
   - Rutas hardcodeadas
   - Modelos no guardados
   - Dependencias no documentadas

4. **Análisis Incompleto:**
   - No hay pruebas de estacionariedad
   - No hay análisis de autocorrelación (ACF/PACF)
   - No hay descomposición estacional
   - No hay análisis de causalidad de Granger

### 5.3 Gaps en el Flujo de Trabajo

```
FLUJO ACTUAL (DESCONECTADO):

[Extracción Precios] → [EDA Precios] → [Modelo LSTM]
                                            ↓
                                      [Predicciones]

[Extracción Noticias] → [Filtrado] → [Sentimientos]
                                           ↓
                                      [Distribución]

FLUJO OBJETIVO (INTEGRADO):

[Extracción Precios] ──┐
                       ├→ [EDA Conjunto] → [Detección Anomalías]
[Extracción Noticias] ─┘                           ↓
                                        [Correlación Anomalía-Noticia]
                                                    ↓
                                        [Análisis de Causalidad]
                                                    ↓
                              [Modelo Predictivo con Sentimientos]
                                                    ↓
                                    [Evaluación de Estabilidad]
```

---

## 6. EVALUACIÓN DE CALIDAD CIENTÍFICA

### 6.1 Criterios de Publicación Científica

| Criterio | Estado Actual | Calificación |
|---------|--------------|-------------|
| Introducción clara | Falta | ❌ 0/10 |
| Marco teórico | Inexistente | ❌ 0/10 |
| Revisión literatura | No presente | ❌ 0/10 |
| Metodología documentada | Parcial | ⚠️ 4/10 |
| Resultados reproducibles | Limitado | ⚠️ 3/10 |
| Análisis estadístico riguroso | Incompleto | ⚠️ 5/10 |
| Discusión de limitaciones | Ausente | ❌ 0/10 |
| Conclusiones fundamentadas | No hay | ❌ 0/10 |
| Referencias bibliográficas | Ninguna | ❌ 0/10 |
| Formato científico | No aplicado | ❌ 1/10 |

**Calificación Global:** 13/100 (Requiere trabajo sustancial)

### 6.2 Mejoras Necesarias para Estándar Científico

**Esenciales:**
1. Definir hipótesis de investigación formales
2. Revisar literatura sobre predicción de oro y sentiment analysis
3. Justificar elección de métodos (LSTM, BETO/RoBERTa, IQR)
4. Documentar supuestos y limitaciones
5. Realizar pruebas estadísticas formales
6. Corregir error de idioma en sentiment analysis
7. Implementar análisis de causalidad
8. Agregar sección de ética y sesgos

**Deseables:**
1. Comparación con trabajos previos
2. Análisis de sensibilidad
3. Validación cruzada temporal
4. Intervalos de confianza en predicciones
5. Discusión de implicaciones económicas

---

## 7. RECOMENDACIONES DE UNIFICACIÓN

### 7.1 Prioridades Inmediatas

#### PRIORIDAD CRÍTICA:
**Corrección del Análisis de Sentimientos**
- Reemplazar BETO con modelo en inglés:
  * `cardiffnlp/twitter-roberta-base-sentiment-latest`
  * `ProsusAI/finbert` (específico para finanzas)
  * `mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis`
- Re-ejecutar análisis completo
- Validar resultados manualmente con muestra

#### PRIORIDAD ALTA:
**Integración Outliers-Noticias**
1. Cargar fechas de outliers desde `AU_Exploratorio_V2`
2. Filtrar noticias en ventana ±3 días de cada outlier
3. Analizar distribución de sentimientos en outliers vs días normales
4. Test estadístico (Chi-cuadrado, t-test)

#### PRIORIDAD ALTA:
**Estandarización de Datos**
1. Definir dataset canónico de noticias
2. Crear pipeline de preprocesamiento unificado
3. Agregar precios a frecuencia diaria
4. Exportar datos limpios a `unificacion/datos_procesados/`

### 7.2 Estructura de Notebooks Unificados

**Propuesta:**

1. **`01_Introduccion_Marco_Teorico.ipynb`**
   - Contexto económico del oro
   - Revisión de literatura
   - Hipótesis de investigación

2. **`02_Extraccion_Datos.ipynb`**
   - Wrapper del script de extracción
   - Documentación de fuentes
   - Validación de calidad

3. **`03_Analisis_Exploratorio_Unificado.ipynb`**
   - EDA de precios (estadísticas, visualizaciones)
   - EDA de noticias (frecuencia, cobertura)
   - Análisis temporal conjunto

4. **`04_Deteccion_Anomalias.ipynb`**
   - Métodos múltiples (IQR, Z-score, Isolation Forest)
   - Validación estadística
   - Extracción de fechas clave

5. **`05_Analisis_Sentimientos.ipynb`**
   - Modelo en inglés correcto
   - Análisis temporal de sentimientos
   - Agregación diaria/semanal

6. **`06_Correlacion_Causalidad.ipynb`**
   - Correlación outliers-sentimientos
   - Test de Granger Causality
   - Análisis de eventos

7. **`07_Modelo_Predictivo_Integrado.ipynb`**
   - LSTM con features de sentimiento
   - Comparación con baselines
   - Evaluación exhaustiva

8. **`08_Resultados_Conclusiones.ipynb`**
   - Síntesis de hallazgos
   - Discusión de implicaciones
   - Limitaciones y trabajo futuro

### 7.3 Scripts Consolidados

**Propuesta:**

1. **`data_extraction.py`**
   - Refactorización de `Extraccion_Datos` como módulo
   - Funciones reutilizables
   - CLI con argparse

2. **`data_preprocessing.py`**
   - Limpieza de precios
   - Limpieza de noticias
   - Generación de features

3. **`outlier_detection.py`**
   - Múltiples métodos de detección
   - Clase OutlierDetector

4. **`sentiment_analysis.py`**
   - Pipeline de sentimientos
   - Caché de resultados
   - Validación de idioma

5. **`time_series_models.py`**
   - LSTM, ARIMA, Prophet
   - Evaluación unificada

6. **`causality_tests.py`**
   - Granger Causality
   - Event studies
   - Métricas de impacto

### 7.4 Informe Científico Final

**Estructura Propuesta:**

```markdown
# Predicción del Precio del Oro mediante Redes Neuronales LSTM 
# y Análisis de Sentimientos de Noticias Financieras

## Resumen (Abstract)
- Contexto, objetivo, métodos, resultados, conclusiones
- Español e Inglés

## 1. Introducción
- Importancia económica del oro
- Problema de investigación
- Objetivos específicos
- Contribuciones del estudio

## 2. Marco Teórico
- 2.1 El oro como activo financiero
- 2.2 Series temporales y modelos LSTM
- 2.3 Análisis de sentimientos en finanzas
- 2.4 Teorías de causalidad mercado-noticias

## 3. Revisión de Literatura
- Estudios previos de predicción de oro
- Sentiment analysis en mercados financieros
- Detección de anomalías en precios
- Análisis de causalidad

## 4. Metodología
- 4.1 Fuentes de datos
- 4.2 Preprocesamiento
- 4.3 Análisis exploratorio
- 4.4 Detección de outliers (justificación IQR)
- 4.5 Análisis de sentimientos (modelo, validación)
- 4.6 Modelo LSTM (arquitectura, hiperparámetros)
- 4.7 Pruebas de causalidad
- 4.8 Métricas de evaluación

## 5. Resultados
- 5.1 Estadísticas descriptivas
- 5.2 Outliers identificados
- 5.3 Distribución de sentimientos
- 5.4 Performance del modelo LSTM
- 5.5 Correlación outliers-noticias
- 5.6 Tests de causalidad

## 6. Discusión
- Interpretación de resultados
- Comparación con literatura
- Limitaciones del estudio
- Implicaciones prácticas

## 7. Conclusiones
- Hallazgos principales
- Respuesta a objetivos
- Trabajo futuro

## Referencias
## Apéndices
- A. Código fuente
- B. Datos suplementarios
- C. Tablas adicionales
```

---

## 8. ROADMAP DE UNIFICACIÓN

### Fase 1: Correcciones Críticas (Semana 1)
- [ ] Corregir análisis de sentimientos con modelo en inglés
- [ ] Estandarizar rutas de archivos
- [ ] Crear estructura de carpetas unificada
- [ ] Documentar dependencias (requirements.txt)

### Fase 2: Integración de Análisis (Semana 2)
- [ ] Vincular outliers con noticias
- [ ] Análisis de correlación temporal
- [ ] Implementar tests de causalidad
- [ ] Generar datasets procesados unificados

### Fase 3: Modelado Integrado (Semana 3)
- [ ] Agregar sentimientos como features al LSTM
- [ ] Implementar modelos baseline
- [ ] Optimización de hiperparámetros
- [ ] Validación cruzada temporal

### Fase 4: Documentación Científica (Semana 4)
- [ ] Redactar marco teórico
- [ ] Revisar literatura
- [ ] Escribir metodología formal
- [ ] Crear visualizaciones para publicación

### Fase 5: Síntesis y Presentación (Semana 5)
- [ ] Informe científico completo
- [ ] Presentación ejecutiva
- [ ] Notebooks reproducibles
- [ ] Repositorio organizado

---

## 9. CONCLUSIONES DEL ANÁLISIS

### 9.1 Estado General del Proyecto

El proyecto ha alcanzado un **avance del 65% aproximadamente**, con componentes individuales bien desarrollados pero con **deficiencias críticas de integración y validez científica**. Los integrantes del equipo han trabajado de forma efectiva en sus módulos asignados, pero la falta de coordinación ha resultado en:

1. **Incompatibilidades de idioma** (error crítico)
2. **Desconexión entre análisis** (outliers vs sentimientos)
3. **Falta de marco científico formal**
4. **Reproducibilidad limitada**

### 9.2 Viabilidad de Objetivos

| Objetivo | Viabilidad | Tiempo Estimado |
|---------|-----------|----------------|
| 1. Extracción datos | ✅ Completado | - |
| 2. EDA | ✅ Alcanzable | 3 días |
| 3. Modelo predictivo | ✅ Mejorable | 5 días |
| 4. Sentiment analysis | ⚠️ Requiere rehacer | 4 días |
| 5. Anomalías + noticias | ✅ Alcanzable | 3 días |
| 6. Causalidad | ⚠️ Desafiante | 7 días |

**Total estimado para objetivos completos:** ~22 días de trabajo

### 9.3 Recomendación Final

**Se recomienda proceder con la unificación siguiendo el roadmap propuesto**, priorizando:

1. **Corrección inmediata del análisis de sentimientos**
2. **Integración de outliers con noticias** (objetivo 5)
3. **Implementación básica de análisis de causalidad** (objetivo 6)
4. **Documentación científica rigurosa**

El proyecto tiene **potencial para ser un trabajo científico sólido** si se abordan las deficiencias identificadas. La base técnica es buena, pero requiere pulido metodológico y formalización.

---

**Documento preparado por:** GitHub Copilot  
**Fecha:** 1 de Diciembre de 2025  
**Versión:** 1.0  
**Próxima revisión:** Post-implementación de correcciones críticas
