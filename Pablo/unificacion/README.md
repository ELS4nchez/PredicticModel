# Predicción del Precio del Oro mediante LSTM y Análisis de Sentimientos

## 📋 Descripción del Proyecto

Este proyecto de investigación científica analiza la predicción del precio del oro (XAU/USD) mediante redes neuronales LSTM, integrando análisis de sentimientos de noticias financieras del Wall Street Journal para evaluar la causalidad entre eventos noticiosos y movimientos anómalos de precios.

**Período de análisis:** 2016-2025 (9+ años)  
**Observaciones:** ~54,000 barras horarias de precios, ~5,400 artículos relevantes  
**Métodos:** Deep Learning (LSTM), NLP (Transformers), Análisis de Series Temporales, Causalidad de Granger

---

## 🎯 Objetivos

### Objetivo General
Desarrollar y evaluar un sistema integrado de predicción del precio del oro que combine modelos de aprendizaje profundo (LSTM) con análisis de sentimientos de noticias financieras, cuantificando la relación entre información noticiosa y movimientos anómalos de precios.

### Objetivos Específicos
1. ✅ Extracción de bases de datos del precio del oro y noticias (2016-2025) con resolución diaria
2. ✅ Análisis exploratorio exhaustivo de ambas fuentes de datos
3. 🔄 Desarrollo de modelos LSTM univariados y multivariados para predicción de precios
4. 🔄 Análisis de sentimientos de noticias usando modelos transformer en inglés
5. 🔄 Detección de anomalías en precios y correlación temporal con noticias
6. ⏳ Análisis de causalidad de Granger entre sentimientos y precios
7. ⏳ Evaluación del "factor desestabilizante" de noticias sobre precios del oro

**Leyenda:** ✅ Completado | 🔄 En progreso | ⏳ Pendiente

---

## 📊 Datasets

### Datos de Precios del Oro
- **Fuente:** Dukascopy Bank SA - Historical Data API
- **Activo:** XAU/USD (Oro vs Dólar Estadounidense)
- **Período:** 03 enero 2016 - 12 enero 2025
- **Frecuencia:** Horaria (agregada a diaria)
- **Registros:** 54,118 barras horarias → 3,298 días
- **Variables:** Open, High, Low, Close, Volume, UTC

### Datos de Noticias
- **Fuente:** Wall Street Journal (WSJ)
- **Método:** Web scraping
- **Período:** 01 enero 2016 - diciembre 2025
- **Artículos totales:** 189,456
- **Artículos relevantes al oro:** 5,464 (2.9%)
- **Variables:** título, URL, fecha
- **Idioma:** Inglés

---

## 🏗️ Estructura del Proyecto

```
unificacion/
│
├── notebooks/                          # Jupyter Notebooks del análisis
│   ├── 01_Introduccion_y_Carga_de_Datos.ipynb
│   ├── 02_Analisis_Exploratorio_Precios.ipynb
│   ├── 03_Analisis_Exploratorio_Noticias.ipynb
│   ├── 04_Deteccion_Anomalias.ipynb
│   ├── 05_Analisis_Sentimientos.ipynb
│   ├── 06_Correlacion_y_Causalidad.ipynb
│   ├── 07_Modelo_LSTM_Unificado.ipynb
│   └── 08_Resultados_y_Conclusiones.ipynb
│
├── scripts/                            # Scripts Python reutilizables
│   ├── data_extraction.py              # Extracción de datos de Dukascopy
│   ├── data_preprocessing.py           # Limpieza y preprocesamiento
│   ├── outlier_detection.py            # Detección de anomalías
│   ├── sentiment_analysis.py           # Pipeline de sentimientos
│   ├── time_series_models.py           # Modelos LSTM, ARIMA, Prophet
│   └── causality_tests.py              # Tests de Granger Causality
│
├── datos_procesados/                   # Datos limpios y procesados
│   ├── precios_oro_diario_limpio.csv
│   ├── noticias_oro_limpias.csv
│   ├── sentimientos_diarios.csv
│   ├── outliers_identificados.csv
│   └── metadata_procesamiento.json
│
├── figuras/                            # Gráficos y visualizaciones
│   ├── 01_serie_temporal_oro.png
│   ├── 02_volumen_noticias_diario.png
│   ├── 03_correlacion_features.png
│   └── ...
│
└── informes/                           # Documentación científica
    ├── 00_ANALISIS_ESTADO_PROYECTO.md
    ├── INFORME_CIENTIFICO_PRINCIPAL.md
    └── README.md                       # Este archivo
```

---

## 🔬 Metodología

### 1. Extracción y Preprocesamiento de Datos

**Precios del oro:**
- Descarga automatizada desde API de Dukascopy
- Limpieza de formato temporal
- Agregación horaria → diaria (OHLCV)
- Forward fill para valores faltantes (<1%)

**Noticias:**
- Web scraping del Wall Street Journal
- Filtrado por palabras clave relacionadas con oro (25 términos)
- Eliminación de duplicados y validación de fechas
- Alineación temporal con precios

### 2. Análisis Exploratorio de Datos (EDA)

**Precios:**
- Estadísticas descriptivas (media, volatilidad, rango)
- Pruebas de estacionariedad (ADF, KPSS)
- Análisis de autocorrelación (ACF, PACF)
- Descomposición de series temporales (STL)

**Noticias:**
- Distribución temporal de publicaciones
- Análisis de frecuencia de términos
- Identificación de períodos de alta cobertura

### 3. Detección de Anomalías

**Métodos implementados:**
- **IQR (Interquartile Range):** Método de Tukey con factor 1.5
- **Z-score modificado:** Basado en MAD (Median Absolute Deviation)
- **Isolation Forest:** Algoritmo de machine learning

**Variables analizadas:**
- Precios de cierre (nivel)
- Retornos diarios (cambios)
- Volatilidad (High - Low)

### 4. Análisis de Sentimientos

**Modelo seleccionado:**
- **Opción 1:** `ProsusAI/finbert` - FinBERT (específico para finanzas)
- **Opción 2:** `cardiffnlp/twitter-roberta-base-sentiment-latest` - RoBERTa

**Pipeline:**
1. Tokenización de títulos de noticias
2. Clasificación: Positivo / Negativo / Neutral
3. Agregación diaria: sentimiento promedio, desviación, sentimiento neto
4. Features derivados: volumen de noticias, dispersión de opiniones

### 5. Modelos LSTM

**Arquitecturas implementadas:**

**Modelo 1: LSTM Univariado**
- Input: Precio de cierre (ventana de 80 días)
- Capas: LSTM(256) + Dropout(0.2) → LSTM(128) + Dropout(0.2) → LSTM(64) + Dropout(0.2) → Dense(1)

**Modelo 2: LSTM Multivariado**
- Input: Close + Volume (ventana de 80 días)
- Arquitectura idéntica con input_shape ajustado

**Modelo 3: LSTM con Sentimiento**
- Input: Precios + Volumen + Features de sentimiento
- Arquitectura similar con más features

**Entrenamiento:**
- División: Train (2016-2023, 88%) / Test (2024-2025, 12%)
- Normalización: MinMaxScaler [0,1]
- Optimizer: Adam, Loss: MSE
- Early stopping: patience=5, min_delta=0.001
- Batch size: 32, Epochs: hasta 30

**Métricas de evaluación:**
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- MAPE (Mean Absolute Percentage Error)
- R² (Coefficient of Determination)
- Directional Accuracy

### 6. Análisis de Correlación y Causalidad

**Correlación Temporal:**
- Ventanas de ±1, ±3, ±7 días alrededor de outliers
- Test Chi-cuadrado de independencia
- Efecto de tamaño (Cramér's V)

**Causalidad de Granger:**
- Test en modelos VAR (Vector Autoregression)
- Hipótesis: Sentimiento → Retornos/Volatilidad
- Selección de lags: AIC, BIC
- Nivel de significancia: α = 0.05

**Modelo de Estabilidad:**
Factor Desestabilizante = α·|Sentimiento| + β·Volumen_Noticias + γ·Dispersión

---

## 🛠️ Tecnologías Utilizadas

### Lenguajes y Frameworks
- **Python 3.8+:** Lenguaje principal
- **Jupyter Notebook:** Análisis interactivo

### Bibliotecas de Datos y Análisis
- **pandas 2.0+:** Manipulación de datos
- **numpy 1.24+:** Operaciones numéricas
- **scipy:** Tests estadísticos

### Visualización
- **matplotlib 3.7+:** Gráficos base
- **seaborn 0.12+:** Visualizaciones estadísticas
- **plotly:** Gráficos interactivos (opcional)

### Machine Learning y Deep Learning
- **scikit-learn 1.3+:** Preprocesamiento, métricas, Isolation Forest
- **tensorflow 2.13+:** Backend de Keras
- **keras:** Modelos LSTM
- **xgboost:** Modelos baseline (opcional)

### Procesamiento de Lenguaje Natural
- **transformers 4.30+:** HuggingFace para modelos BERT/RoBERTa
- **torch 2.0+:** Backend de transformers
- **nltk / spacy:** Preprocesamiento de texto (opcional)

### Series Temporales
- **statsmodels 0.14+:** ARIMA, VAR, tests de estacionariedad, Granger causality
- **prophet:** Modelo baseline de Facebook (opcional)

### Utilidades
- **requests:** Descarga de datos de APIs
- **beautifulsoup4:** Web scraping (si aplica)
- **tqdm:** Barras de progreso

---

## 📦 Instalación

### 1. Clonar el repositorio (o descargar archivos)

```bash
cd /home/els4nchez/Videos/TECH/unificacion
```

### 2. Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install pandas numpy scipy matplotlib seaborn
pip install scikit-learn tensorflow keras
pip install transformers torch
pip install statsmodels
pip install jupyter notebook
pip install requests tqdm openpyxl
```

**Archivo requirements.txt completo:**

```
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
tensorflow>=2.13.0
keras>=2.13.0
transformers>=4.30.0
torch>=2.0.0
statsmodels>=0.14.0
jupyter>=1.0.0
notebook>=6.5.0
requests>=2.31.0
tqdm>=4.65.0
openpyxl>=3.1.0
```

---

## 🚀 Ejecución del Proyecto

### Opción 1: Ejecutar Notebooks Secuencialmente

```bash
cd unificacion/notebooks
jupyter notebook
```

Ejecutar en orden:
1. `01_Introduccion_y_Carga_de_Datos.ipynb` ← **COMENZAR AQUÍ**
2. `02_Analisis_Exploratorio_Precios.ipynb`
3. `03_Analisis_Exploratorio_Noticias.ipynb`
4. `04_Deteccion_Anomalias.ipynb`
5. `05_Analisis_Sentimientos.ipynb`
6. `06_Correlacion_y_Causalidad.ipynb`
7. `07_Modelo_LSTM_Unificado.ipynb`
8. `08_Resultados_y_Conclusiones.ipynb`

### Opción 2: Ejecutar Scripts Individuales

```bash
cd unificacion/scripts

# Extracción de datos
python data_extraction.py --symbol XAU-USD --years 2024-2025 --timeframe 1h

# Preprocesamiento
python data_preprocessing.py --input ../datos_horas/ --output ../datos_procesados/

# Detección de outliers
python outlier_detection.py --method IQR --threshold 1.5

# Análisis de sentimientos
python sentiment_analysis.py --model finbert --input noticias_oro_limpias.csv

# Entrenamiento de LSTM
python time_series_models.py --model LSTM --features Close,Volume --window 80

# Tests de causalidad
python causality_tests.py --x sentiment --y returns --lags 5
```

---

## 📈 Resultados Principales

### Análisis Exploratorio

**Precios del Oro (2016-2025):**
- Rango de precios: $1,062 - $2,800+ USD/oz
- Variación total: ~164%
- Volatilidad anualizada: [calcular]%
- Retorno promedio diario: [calcular]%

**Noticias sobre Oro:**
- Artículos relevantes: 5,464
- Cobertura temporal: [X]% de días con noticias
- Promedio: ~1.7 noticias/día
- Picos de cobertura: [identificar eventos clave]

### Detección de Anomalías

**Outliers identificados (método IQR):**
- Total de outliers: [Z] días
- Porcentaje: [W]% del período
- Eventos extremos positivos: [X]
- Eventos extremos negativos: [Y]

### Análisis de Sentimientos

**Distribución de sentimientos:**
- Neutral: [%]
- Negativo: [%]
- Positivo: [%]

**Hallazgos:**
- [Análisis de tendencias temporales]
- [Correlación con movimientos de precios]

### Modelos LSTM

**Performance (conjunto de prueba 2024-2025):**

| Modelo | RMSE | MAE | MAPE | R² | DA |
|--------|------|-----|------|----|----|
| LSTM Univariado | [X] | [Y] | [Z]% | [W] | [V]% |
| LSTM Multivariado | [X] | [Y] | [Z]% | [W] | [V]% |
| LSTM con Sentimiento | [X] | [Y] | [Z]% | [W] | [V]% |
| ARIMA Baseline | [X] | [Y] | [Z]% | [W] | [V]% |

**Interpretación:**
- [Análisis de resultados]
- [Comparación entre modelos]

### Causalidad

**Test de Granger Causality:**
- Sentimiento → Retornos: p-valor = [X] → [Conclusión]
- Sentimiento → Volatilidad: p-valor = [Y] → [Conclusión]
- Retornos → Sentimiento: p-valor = [Z] → [Conclusión]

**Correlación Outliers-Sentimiento:**
- Chi-cuadrado: χ² = [X], p-valor = [Y]
- Cramér's V: [Z] ([efecto pequeño/moderado/grande])
- Conclusión: [Interpretación]

---

## 🔍 Hallazgos Clave

### 1. Capacidad Predictiva de LSTM
- Los modelos LSTM demuestran capacidad [moderada/alta/limitada] para predecir precios del oro
- El modelo [univariado/multivariado/con sentimiento] alcanzó el mejor desempeño
- Horizonte óptimo de predicción: [X] días

### 2. Rol del Sentimiento Noticioso
- [Existe/No existe] evidencia estadística de causalidad sentimiento → precios
- El impacto del sentimiento es más fuerte en períodos de [alta/baja] volatilidad
- Noticias [negativas/positivas] tienen mayor efecto sobre precios

### 3. Anomalías y Eventos
- [X]% de outliers de precios coinciden con noticias de sentimiento extremo
- Los eventos noticiosos preceden movimientos de precios con [Y] días de lag promedio
- Principales eventos identificados: [listar top 5]

### 4. Factor Desestabilizante
- El modelo de estabilidad explica [X]% de la varianza en volatilidad (R²)
- Componentes más influyentes: [ranking de α, β, γ]

---

## 📚 Referencias Bibliográficas

[Por completar con bibliografía en formato APA]

1. Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. Neural computation, 9(8), 1735-1780.

2. Devlin, J., et al. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. NAACL-HLT.

3. Araci, D. (2019). FinBERT: Financial sentiment analysis with pre-trained language models. arXiv preprint arXiv:1908.10063.

4. Granger, C. W. (1969). Investigating causal relations by econometric models and cross-spectral methods. Econometrica, 424-438.

5. Tetlock, P. C. (2007). Giving content to investor sentiment: The role of media in the stock market. The Journal of finance, 62(3), 1139-1168.

6. Fischer, T., & Krauss, C. (2018). Deep learning with long short-term memory networks for financial market predictions. European Journal of Operational Research, 270(2), 654-669.

[... más referencias según avance el proyecto]

---

## 👥 Autores y Contribuciones

**Equipo de Investigación:**
- [Nombre 1]: Extracción de datos, análisis exploratorio de precios
- [Nombre 2]: Desarrollo de modelos LSTM
- [Nombre 3]: Análisis de sentimientos, procesamiento de noticias
- [Nombre 4]: Detección de anomalías, análisis de causalidad
- [Nombre 5]: Documentación científica, integración

---

## 📄 Licencia

[Por definir - MIT / Academic Use Only / etc.]

---

## 🔗 Enlaces Útiles

- **Dukascopy API:** https://www.dukascopy.com/swiss/english/marketwatch/historical/
- **Wall Street Journal:** https://www.wsj.com/
- **HuggingFace Transformers:** https://huggingface.co/transformers/
- **TensorFlow/Keras:** https://www.tensorflow.org/
- **Statsmodels:** https://www.statsmodels.org/

---

## 📞 Contacto

Para preguntas, sugerencias o colaboraciones:
- Email: [correo del equipo]
- Institución: [nombre de la institución]

---

## ✅ Checklist de Progreso

### Extracción de Datos
- [x] Descargar precios del oro (Dukascopy)
- [x] Web scraping de noticias (WSJ)
- [x] Limpieza y validación de datos

### Análisis Exploratorio
- [x] EDA de precios (estadísticas, visualizaciones)
- [ ] Pruebas de estacionariedad
- [ ] Análisis de autocorrelación
- [ ] Descomposición de series temporales
- [ ] EDA de noticias (frecuencia, cobertura)

### Detección de Anomalías
- [ ] Implementación de método IQR
- [ ] Implementación de Z-score modificado
- [ ] Implementación de Isolation Forest
- [ ] Validación cruzada de métodos
- [ ] Identificación de fechas clave

### Análisis de Sentimientos
- [ ] Selección de modelo (FinBERT / RoBERTa)
- [ ] Pipeline de procesamiento
- [ ] Clasificación de títulos
- [ ] Agregación temporal
- [ ] Validación de resultados

### Modelado LSTM
- [ ] Ingeniería de features
- [ ] LSTM univariado
- [ ] LSTM multivariado
- [ ] LSTM con sentimiento
- [ ] Optimización de hiperparámetros
- [ ] Validación cruzada temporal
- [ ] Comparación con baselines

### Correlación y Causalidad
- [ ] Análisis de ventanas temporales
- [ ] Test Chi-cuadrado
- [ ] Test de Granger Causality
- [ ] Modelo de estabilidad
- [ ] Interpretación de resultados

### Documentación
- [x] README principal
- [x] Informe científico (estructura)
- [x] Análisis del estado del proyecto
- [ ] Notebooks documentados
- [ ] Scripts con docstrings
- [ ] Informe final completo

---

**Última actualización:** Diciembre 2025  
**Versión del proyecto:** 1.0  
**Estado:** 🔄 En desarrollo activo
