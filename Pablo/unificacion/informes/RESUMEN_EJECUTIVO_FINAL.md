
# RESUMEN EJECUTIVO
## Predicción de Precios del Oro con Análisis de Sentimientos de Noticias

**Fecha:** 2025-12-03
**Equipo:** Análisis de Datos - Proyecto Oro

---

## 1. DATOS PROCESADOS

- **Precios del oro:** 3,614 días (2016-01-03 a 2025-11-24)
- **Noticias analizadas:** 18,776 artículos del Wall Street Journal
- **Outliers detectados:** 132 eventos anómalos en precios
- **Dataset integrado:** 2,273 días con precios y sentimientos

## 2. METODOLOGÍA

### 2.1 Análisis de Sentimientos
- **Modelo:** FinBERT (ProsusAI/finbert)
- **Clasificación:** Positivo, Neutral, Negativo
- **Distribución:**
  - Positivo: 0.0%
  - Neutral: 0.0%
  - Negativo: 0.0%

### 2.2 Detección de Anomalías
- **Métodos:** IQR, Z-Score, Isolation Forest
- **Consenso:** Outliers detectados por ≥2 métodos

### 2.3 Modelos LSTM
- **Arquitectura:** 256-128-64 units, dropout 0.2
- **Secuencias:** 60 días lookback
- **División:** 60% train / 20% val / 20% test

## 3. RESULTADOS PRINCIPALES

### 3.1 Correlación y Causalidad
- **Lag óptimo:** -6 días
- **Correlación máxima:** -0.0696
- **Test de Granger:** NO SIGNIFICATIVO

### 3.2 Performance de Modelos

**LSTM Base (sin sentimiento):**
- RMSE: $472.94
- MAE: $406.75
- R²: -0.3901

**LSTM + Sentimiento:**
- RMSE: $634.65
- MAE: $563.84
- R²: -1.5031

**Mejora con sentimiento:**
- RMSE: -34.19%
- MAE: -38.62%
- R²: -285.35%

## 4. CONCLUSIONES

1. **Valor predictivo del sentimiento:** El sentimiento NO mejora significativamente las predicciones.

2. **Causalidad:** No se encontró causalidad Granger significativa.

3. **Anomalías:** Se detectaron 132 eventos anómalos en el precio del oro, algunos coincidentes con noticias de sentimiento extremo.

## 5. TRABAJO FUTURO

- Incorporar más fuentes de noticias (Reuters, Bloomberg)
- Analizar contenido completo de artículos
- Modelos más sofisticados (Transformers)
- Indicadores macroeconómicos adicionales
- Estrategias de trading basadas en sentimiento

---

**Archivos generados:**
- 8 tablas de resultados (CSV)
- 2 figuras principales (HTML + PNG)
- Modelos entrenados (Keras .keras)
- Datasets procesados (CSV)
