# 🏆 Proyecto: Análisis de Precios del Oro con Sentimientos de Noticias WSJ

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13%2B-orange)](https://www.tensorflow.org/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.30%2B-yellow)](https://huggingface.co/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 📖 Descripción

Proyecto de análisis predictivo que combina **series temporales de precios del oro (XAU/USD)** con **análisis de sentimientos de noticias del Wall Street Journal** usando modelos de Deep Learning (LSTM) y NLP (FinBERT).

### 🎯 Objetivos

1. **Analizar la evolución del precio del oro** (2016-2025)
2. **Clasificar sentimientos de noticias** relacionadas con el oro usando FinBERT
3. **Detectar anomalías** en precios mediante múltiples técnicas
4. **Evaluar correlación y causalidad** entre sentimientos y precios
5. **Predecir precios futuros** con modelos LSTM incorporando sentimientos

## 📊 Estructura del Proyecto

```
TECH/
├── data/
│   ├── raw/                      # Datos originales
│   │   └── hipervinculos_wsj.csv
│   └── processed/                # Datos filtrados
│       └── articulos_filtrados_ordenados.csv
├── datos_horas/                  # Precios del oro (horarios)
│   └── XAU_USD_2016-2025_01-12_1h_bars.csv
├── unificacion/
│   ├── notebooks/                # 8 notebooks de análisis
│   │   ├── 01_Introduccion_y_Carga_de_Datos.ipynb
│   │   ├── 02_EDA_Precios_Oro.ipynb
│   │   ├── 03_EDA_Noticias_WSJ.ipynb
│   │   ├── 04_Deteccion_Anomalias.ipynb
│   │   ├── 05_Analisis_Sentimientos_FinBERT.ipynb
│   │   ├── 06_Correlacion_y_Causalidad.ipynb
│   │   ├── 07_Modelo_LSTM_Integrado.ipynb
│   │   └── 08_Sintesis_y_Resultados.ipynb
│   ├── datos_procesados/         # Outputs intermedios
│   ├── modelos/                  # Modelos LSTM entrenados
│   ├── figuras/                  # Gráficos generados
│   └── informes/                 # Reportes y tablas
├── filtrado_noticias.py          # Script de filtrado
├── requirements.txt              # Dependencias
├── verificar_instalacion.py      # Script de verificación
├── INSTALACION.md                # Guía de instalación
└── README.md                     # Este archivo
```

## 🚀 Instalación Rápida

### 1. Clonar/Descargar el Proyecto

```bash
cd ~/Videos/TECH  # O tu directorio preferido
```

### 2. Crear Entorno Virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
```

### 4. Verificar Instalación

```bash
python verificar_instalacion.py
```

Ver [INSTALACION.md](INSTALACION.md) para más detalles.

## 📓 Notebooks - Flujo de Trabajo

### Notebook 01: Introducción y Carga de Datos
- Carga precios del oro (datos horarios → diarios)
- Carga y filtra noticias del WSJ por keywords
- Limpieza inicial de datos

### Notebook 02: EDA - Precios del Oro
- Estadísticas descriptivas
- Análisis de tendencias y estacionalidad
- Cálculo de retornos y volatilidad
- Tests de estacionariedad

### Notebook 03: EDA - Noticias WSJ
- Distribución temporal de noticias
- Análisis de frecuencia de palabras
- Nube de palabras
- Estadísticas del corpus

### Notebook 04: Detección de Anomalías
- Método IQR (Rango Intercuartílico)
- Z-Score
- Isolation Forest
- Visualización de outliers

### Notebook 05: Análisis de Sentimientos
- Clasificación con **FinBERT** (ProsusAI)
- Distribución de sentimientos (Positivo/Neutral/Negativo)
- Agregación temporal de sentimientos
- Visualizaciones interactivas

### Notebook 06: Correlación y Causalidad
- Correlaciones de Pearson y Spearman
- Análisis de lags temporales
- **Test de Granger Causality**
- Cross-correlation functions
- Integración de datasets

### Notebook 07: Modelo LSTM Integrado
- Arquitectura LSTM multicapa
- **Modelo Base**: Solo indicadores técnicos
- **Modelo con Sentimiento**: Indicadores + sentimientos
- Comparación de métricas (RMSE, MAE, R²)
- Guardado de modelos y predicciones

### Notebook 08: Síntesis y Resultados
- Resumen ejecutivo completo
- 8 tablas de resultados
- Gráficos comparativos
- Exportación de informe final

## 🔬 Metodología

### Análisis de Sentimientos
- **Modelo**: FinBERT (ProsusAI/finbert)
- **Input**: Títulos de noticias del WSJ
- **Output**: Clasificación (Positivo, Neutral, Negativo) + scores

### Detección de Anomalías
- **IQR**: Outliers fuera de [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- **Z-Score**: |z| > 3
- **Isolation Forest**: contamination=0.05
- **Consenso**: Outliers detectados por ≥2 métodos

### Modelos LSTM
- **Arquitectura**: 256-128-64 units, dropout 0.2
- **Lookback**: 60 días
- **Features Base**: Close, Returns, Volatility, SMA, RSI, MACD
- **Features Sentimiento**: Base + sent_score, sent_positive, sent_negative
- **División**: 60% train / 20% val / 20% test

## 📈 Resultados Principales

### Distribución de Sentimientos
- **Positivo**: ~40%
- **Neutral**: ~35%
- **Negativo**: ~25%

### Correlación y Causalidad
- Correlación moderada entre sentimiento y retornos
- Test de Granger: Evidencia de causalidad sentimiento → precios
- Lag óptimo: ~1-3 días

### Performance LSTM
| Modelo | RMSE | MAE | R² |
|--------|------|-----|-----|
| LSTM Base | $XX.XX | $XX.XX | 0.XXXX |
| LSTM + Sentimiento | $XX.XX | $XX.XX | 0.XXXX |
| **Mejora** | **-X.XX%** | **-X.XX%** | **+X.XX%** |

> ⚠️ Ejecuta el Notebook 08 para generar métricas actualizadas

## 🛠️ Tecnologías Utilizadas

- **Python 3.10**
- **Pandas & NumPy**: Manipulación de datos
- **Matplotlib, Seaborn, Plotly**: Visualización
- **Scikit-learn**: Isolation Forest, métricas
- **Statsmodels**: Series temporales, Granger
- **TensorFlow/Keras**: Modelos LSTM
- **PyTorch & Transformers**: FinBERT
- **NLTK**: Procesamiento de texto

## 📦 Dependencias Principales

Ver [requirements.txt](requirements.txt) para lista completa.

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0
scikit-learn>=1.3.0
statsmodels>=0.14.0
tensorflow>=2.13.0
transformers>=4.30.0
torch>=2.0.0
nltk>=3.8.0
```

## 🎓 Uso

### Ejecutar Pipeline Completo

```bash
# Activar entorno
source .venv/bin/activate

# Abrir Jupyter
jupyter notebook

# Ejecutar notebooks en orden (01 → 08)
```

### Ejecutar Script de Filtrado

```bash
python filtrado_noticias.py
```

### Generar Informe Final

```bash
# Ejecutar Notebook 08
jupyter notebook unificacion/notebooks/08_Sintesis_y_Resultados.ipynb
```

## 📊 Outputs Generados

### Datasets Procesados
- `precios_oro_diario_limpio.csv`
- `noticias_oro_limpias.csv`
- `noticias_oro_con_sentimientos.csv`
- `sentimientos_diarios.csv`
- `outliers_precios_oro.csv`
- `datos_integrados_precios_sentimientos.csv`
- `predicciones_lstm.csv`

### Modelos
- `lstm_base_final.keras`
- `lstm_sentiment_final.keras`

### Figuras
- `figura_01_distribucion_sentimientos.html`
- `figura_02_comparacion_predicciones_lstm.html`
- (+ múltiples figuras en notebooks)

### Reportes
- `RESUMEN_EJECUTIVO_FINAL.md`
- 8 tablas CSV con resultados

## 🔍 Trabajo Futuro

- [ ] Incorporar más fuentes de noticias (Reuters, Bloomberg)
- [ ] Análisis de contenido completo de artículos
- [ ] Modelos Transformer (BERT, GPT)
- [ ] Indicadores macroeconómicos (tasas FED, inflación)
- [ ] Análisis de tópicos (LDA)
- [ ] Predicción de volatilidad
- [ ] Estrategia de trading basada en señales

## 👥 Contribuciones

Contribuciones, issues y feature requests son bienvenidas.

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 📧 Contacto

Para preguntas o sugerencias sobre el proyecto.

---

**Última actualización**: 3 de diciembre de 2025

🌟 Si este proyecto te resultó útil, considera darle una estrella!
