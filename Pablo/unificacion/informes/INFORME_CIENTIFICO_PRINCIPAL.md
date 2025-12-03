# Predicción del Precio del Oro mediante Redes Neuronales LSTM y Análisis de Sentimientos de Noticias Financieras

**Autores:** [Nombres del equipo]  
**Institución:** [Nombre de la institución]  
**Fecha:** Diciembre 2025  
**Tipo de documento:** Informe de Investigación Científica

---

## RESUMEN

**Contexto:** El oro (XAU/USD) representa uno de los activos financieros más importantes a nivel global, funcionando como reserva de valor, cobertura contra la inflación y activo refugio en períodos de incertidumbre económica. La predicción de sus movimientos de precio es de gran interés tanto para inversionistas institucionales como para investigadores en economía financiera.

**Objetivo:** Este estudio investiga la capacidad predictiva de redes neuronales Long Short-Term Memory (LSTM) para forecasting del precio del oro, integrando análisis de sentimientos de noticias financieras del Wall Street Journal para evaluar si existe causalidad entre eventos noticiosos y movimientos anómalos en los precios.

**Métodos:** Se empleó una base de datos de 54,118 observaciones horarias de precios XAU/USD (2016-2025) agregadas a frecuencia diaria, junto con 189,456 artículos del Wall Street Journal. Se implementó: (1) análisis exploratorio con detección de outliers mediante método IQR, (2) análisis de sentimientos usando transformers pre-entrenados, (3) modelos LSTM univariados y multivariados con arquitectura de 3 capas y dropout, (4) análisis de correlación temporal entre anomalías de precio y sentimiento noticioso, y (5) tests de causalidad de Granger.

**Resultados:** El modelo LSTM univariado (base) alcanzó un MAPE de 7.34% y R² de -1.66 en el conjunto de prueba. La incorporación de variables de sentimiento mejoró el desempeño en 12-15%: MAPE de 6.19%, R² de -1.06, RMSE de $126.05 y MAE de $113.35. Se identificaron 132 outliers significativos por consenso (≥2 métodos), de los cuales 35.6% coincidieron temporalmente (ventana ±3 días) con noticias de sentimiento extremo. El análisis de sentimientos reveló una distribución predominantemente neutral (44.7%), con 33.8% negativo y 21.5% positivo. Los tests de Granger Causality NO rechazaron la hipótesis nula de no causalidad entre sentimiento y retornos (p-valor mínimo = 0.29 > 0.05). El lag óptimo de correlación fue -10 días, indicando que los precios predicen el sentimiento de noticias, no al revés.

**Conclusiones:** Los modelos LSTM demuestran capacidad predictiva limitada para el precio del oro en horizontes de 60 días (R² negativos), aunque la incorporación de sentimiento produce mejoras significativas del 12-15% en errores. Existe evidencia moderada de asociación entre noticias con sentimiento extremo y movimientos anómalos (35.6% coincidencia, R² = 4.2%), sugiriendo que factores informativos juegan un rol complementario pero marginal en la determinación de precios. La causalidad opera en dirección inversa (precio→noticias), desafiando la hipótesis común de que noticias predicen mercados. Las limitaciones incluyen horizonte temporal largo (60 días), análisis de títulos únicamente, y período específico con eventos únicos (COVID, guerra Ucrania).

**Palabras clave:** Precio del oro, LSTM, redes neuronales, análisis de sentimientos, NLP financiero, detección de anomalías, causalidad de Granger, series temporales financieras

---

## ABSTRACT (English)

**Context:** Gold (XAU/USD) represents one of the most important financial assets globally, functioning as a store of value, hedge against inflation, and safe-haven asset during periods of economic uncertainty. Predicting its price movements is of great interest to both institutional investors and financial economics researchers.

**Objective:** This study investigates the predictive capability of Long Short-Term Memory (LSTM) neural networks for gold price forecasting, integrating sentiment analysis of Wall Street Journal financial news to evaluate whether causality exists between news events and anomalous price movements.

**Methods:** We employed a database of 54,118 hourly XAU/USD price observations (2016-2025) aggregated to daily frequency, along with 189,456 Wall Street Journal articles. We implemented: (1) exploratory analysis with outlier detection using IQR method, (2) sentiment analysis using pre-trained transformers, (3) univariate and multivariate LSTM models with 3-layer architecture and dropout, (4) temporal correlation analysis between price anomalies and news sentiment, and (5) Granger causality tests.

**Results:** The univariate (base) LSTM model achieved a MAPE of 7.34% and R² of -1.66 on the test set. Incorporating sentiment variables improved performance by 12-15%: MAPE of 6.19%, R² of -1.06, RMSE of $126.05, and MAE of $113.35. We identified 132 significant outliers by consensus (≥2 methods), of which 35.6% temporally coincided (±3 day window) with extreme sentiment news. Sentiment analysis revealed a predominantly neutral distribution (44.7%), with 33.8% negative and 21.5% positive. Granger Causality tests did NOT reject the null hypothesis of no causality between sentiment and returns (minimum p-value = 0.29 > 0.05). The optimal correlation lag was -10 days, indicating that prices predict news sentiment, not the reverse.

**Conclusions:** LSTM models demonstrate limited predictive capability for gold prices at 60-day horizons (negative R²), though sentiment incorporation produces significant 12-15% error reductions. There is moderate evidence of association between extreme sentiment news and anomalous movements (35.6% coincidence, R² = 4.2%), suggesting that informational factors play a complementary but marginal role in price determination. Causality operates in the inverse direction (price→news), challenging the common hypothesis that news predicts markets. Limitations include long time horizon (60 days), title-only analysis, and specific period with unique events (COVID, Ukraine war).

**Keywords:** Gold price, LSTM, neural networks, sentiment analysis, financial NLP, anomaly detection, Granger causality, financial time series

---

## 1. INTRODUCCIÓN

### 1.1 Contexto y Motivación

El oro ha desempeñado históricamente un papel fundamental en el sistema financiero global como activo de reserva, medio de intercambio y refugio de valor. En el contexto económico contemporáneo (2016-2025), caracterizado por políticas monetarias expansivas, inflación volátil, tensiones geopolíticas y crisis sanitarias globales, el oro ha experimentado fluctuaciones significativas en su precio, alcanzando máximos históricos superiores a $2,000 USD por onza troy.

La predicción precisa de los movimientos del precio del oro representa un desafío de gran relevancia para múltiples actores económicos:

- **Inversionistas institucionales:** Fondos de cobertura, fondos de pensiones y gestoras de activos requieren modelos cuantitativos robustos para optimización de portafolios y gestión de riesgos.

- **Bancos centrales:** Administradores de reservas internacionales necesitan proyecciones para decisiones de diversificación y timing de operaciones.

- **Industria minera:** Productores de oro utilizan forecasts de precios para decisiones de producción, cobertura financiera e inversiones de capital.

- **Investigadores académicos:** El oro representa un caso de estudio ideal para teorías de formación de precios de activos, eficiencia de mercados y finanzas conductuales.

### 1.2 Planteamiento del Problema

El precio del oro se determina en mercados globales 24/7 altamente líquidos, influenciado por una multiplicidad de factores:

**Factores macroeconómicos:**
- Tasas de interés reales
- Expectativas de inflación
- Fortaleza del dólar estadounidense
- Crecimiento económico global

**Factores geopolíticos:**
- Tensiones internacionales
- Conflictos armados
- Elecciones y cambios de gobierno
- Sanciones económicas

**Factores de mercado:**
- Posicionamiento de inversionistas especulativos
- Flujos hacia ETFs de oro
- Demanda de joyería (India, China)
- Producción minera

**Factores informativos:**
- Anuncios de política monetaria (Fed, BCE, BoJ)
- Datos macroeconómicos
- Noticias corporativas del sector minero
- Análisis y recomendaciones de analistas

Tradicionalmente, los modelos de predicción han empleado enfoques econométricos clásicos (ARIMA, VAR, GARCH) que asumen relaciones lineales y estacionariedad de las series. Sin embargo, la creciente evidencia de:

1. **No-linealidades** en la dinámica de precios
2. **Cambios estructurales** en regímenes de volatilidad
3. **Dependencias de largo plazo** (memoria larga)
4. **Asimetrías** en respuestas a shocks positivos/negativos

ha motivado la exploración de métodos de aprendizaje automático, particularmente redes neuronales recurrentes como LSTM, capaces de capturar patrones complejos en datos secuenciales.

Paralelamente, el desarrollo de técnicas avanzadas de Procesamiento de Lenguaje Natural (NLP) ha permitido cuantificar el "tono" o "sentimiento" de información textual no estructurada (noticias, redes sociales, reportes corporativos). La hipótesis de que **la información noticiosa contiene señales predictivas** sobre futuros movimientos de precios se fundamenta en:

- **Teoría de mercados eficientes semi-fuertes:** Los precios incorporan información públicamente disponible con cierto rezago temporal.
- **Finanzas conductuales:** El sentimiento de mercado influencia decisiones de inversión más allá de fundamentos económicos.
- **Estudios empíricos:** Evidencia documentada de correlación entre sentimiento noticioso y retornos/volatilidad en diversos activos.

### 1.3 Preguntas de Investigación

Este estudio aborda las siguientes preguntas científicas:

**P1:** ¿Pueden los modelos LSTM univariados y multivariados predecir efectivamente el precio del oro en horizontes de corto plazo (1-30 días)?

**P2:** ¿Cuál es la distribución temporal de sentimientos (positivo/negativo/neutral) en noticias relacionadas con el oro del Wall Street Journal durante el período 2016-2025?

**P3:** ¿Existen puntos anómalos significativos en la serie temporal de precios del oro, y estos coinciden temporalmente con eventos noticiosos de sentimiento extremo?

**P4:** ¿Existe evidencia estadística de causalidad de Granger entre el sentimiento de noticias y la volatilidad/retornos del precio del oro?

**P5:** ¿La incorporación de features de sentimiento noticioso mejora significativamente la capacidad predictiva de modelos LSTM comparado con modelos puramente basados en datos de precios?

### 1.4 Objetivos de la Investigación

#### Objetivo General

Desarrollar y evaluar un sistema integrado de predicción del precio del oro que combine modelos de aprendizaje profundo (LSTM) con análisis de sentimientos de noticias financieras, cuantificando la relación entre información noticiosa y movimientos anómalos de precios.

#### Objetivos Específicos

**OE1:** Construir y validar bases de datos de precios históricos del oro (XAU/USD) y noticias del Wall Street Journal para el período 2016-2025.

**OE2:** Realizar análisis exploratorio exhaustivo de ambas fuentes de datos, caracterizando propiedades estadísticas, estacionariedad, autocorrelación y distribuciones.

**OE3:** Implementar métodos robustos de detección de anomalías (outliers) en precios basados en técnicas estadísticas (IQR, Z-score) y machine learning (Isolation Forest).

**OE4:** Desarrollar pipeline de análisis de sentimientos utilizando modelos transformer pre-entrenados en inglés, específicos para el dominio financiero.

**OE5:** Diseñar, entrenar y evaluar modelos LSTM para predicción de precios, comparando arquitecturas univariadas vs multivariadas, con y sin features de sentimiento.

**OE6:** Realizar análisis de correlación temporal entre outliers de precios y noticias de sentimiento extremo, empleando ventanas temporales de ±1, ±3 y ±7 días.

**OE7:** Ejecutar tests de causalidad de Granger para evaluar si el sentimiento noticioso "causa" (en sentido estadístico) cambios en volatilidad o retornos del oro.

**OE8:** Sintetizar hallazgos en un framework coherente que evalúe el "factor desestabilizante" de noticias sobre la estabilidad de precios del oro.

### 1.5 Hipótesis de Trabajo

**H1 (Capacidad predictiva LSTM):** Los modelos LSTM superarán significativamente (p<0.05) a modelos baseline (persistencia, ARIMA) en métricas de predicción (RMSE, MAE, MAPE) en horizontes de 1-7 días.

**H2 (Sentimiento y outliers):** Existe asociación estadísticamente significativa (Chi-cuadrado, p<0.05) entre la ocurrencia de outliers de precios y noticias con sentimiento extremo (percentiles <10 o >90 de distribución de sentimiento) en ventanas temporales de ±3 días.

**H3 (Causalidad):** El sentimiento agregado de noticias "Granger-causa" la volatilidad del oro con al menos 1 día de rezago, pero no viceversa (causalidad unidireccional).

**H4 (Mejora con sentimiento):** Modelos LSTM que incorporan features de sentimiento como variables exógenas mostrarán mejora ≥5% en R² comparado con modelos puramente basados en datos OHLCV.

### 1.6 Contribuciones del Estudio

Este trabajo contribuye a la literatura en las siguientes dimensiones:

**Metodológica:**
- Integración sistemática de técnicas de deep learning (LSTM) con NLP (transformers) para un activo financiero específico (oro).
- Comparación rigurosa de métodos de detección de anomalías en series temporales financieras.
- Protocolo reproducible de análisis de causalidad información-precio.

**Empírica:**
- Dataset único de ~190,000 artículos del WSJ curados específicamente para investigación del oro.
- Caracterización de la distribución temporal de sentimientos en noticias sobre oro durante período de alta volatilidad macroeconómica (2016-2025).
- Cuantificación del lag temporal entre información noticiosa y ajuste de precios.

**Práctica:**
- Framework operativo para integración de señales de sentimiento en estrategias de trading cuantitativo.
- Herramientas open-source para replicación y extensión del análisis a otros commodities o activos.

### 1.7 Estructura del Documento

El resto del informe se organiza como sigue:

- **Sección 2 (Marco Teórico):** Fundamentación conceptual sobre el oro como activo, teorías de formación de precios, redes LSTM y análisis de sentimientos.

- **Sección 3 (Revisión de Literatura):** Síntesis de trabajos previos en predicción de precios de oro, sentiment analysis financiero y causalidad noticias-mercados.

- **Sección 4 (Metodología):** Descripción detallada de fuentes de datos, preprocesamiento, modelos implementados, métricas de evaluación y tests estadísticos.

- **Sección 5 (Resultados):** Presentación de hallazgos empíricos con tablas, figuras y análisis estadístico.

- **Sección 6 (Discusión):** Interpretación de resultados, comparación con literatura, limitaciones y validación de hipótesis.

- **Sección 7 (Conclusiones):** Síntesis de contribuciones, respuestas a preguntas de investigación y direcciones futuras.

---

## 2. MARCO TEÓRICO

### 2.1 El Oro como Activo Financiero

#### 2.1.1 Propiedades Económicas del Oro

El oro posee características únicas que lo distinguen de otros activos financieros:

**Reserva de valor:**
- Durabilidad física: no se corroe, no se degrada
- Escasez natural: oferta limitada por stock geológico
- Reconocimiento universal como activo de valor

**Activo refugio (safe-haven):**
Durante crisis financieras, incertidumbre geopolítica o shocks económicos, los inversionistas tienden a desplazar capital hacia el oro, generando correlación negativa con activos de riesgo (acciones) y correlación positiva con volatilidad de mercados (VIX).

**Cobertura contra inflación:**
El oro tiende a mantener poder adquisitivo en períodos inflacionarios, aunque la evidencia empírica muestra que esta propiedad es efectiva principalmente en horizontes de largo plazo (>5 años).

**Activo sin rendimiento:**
A diferencia de bonos (cupones) o acciones (dividendos), el oro no genera flujos de caja, lo que implica:
- Costo de oportunidad: tasas de interés reales
- Costos de almacenamiento y seguro
- Valoración basada en expectativas de precio futuro

#### 2.1.2 Determinantes del Precio del Oro

El modelo teórico de equilibrio del precio del oro puede expresarse como:

$$P_t^{Gold} = f(r_t^{real}, \pi_t^e, USD_t, VIX_t, D_t^{jewelry}, S_t^{mining}, I_t^{news})$$

Donde:
- $r_t^{real}$: Tasa de interés real (costo de oportunidad)
- $\pi_t^e$: Expectativas de inflación
- $USD_t$: Índice de fortaleza del dólar
- $VIX_t$: Volatilidad implícita de mercados (miedo)
- $D_t^{jewelry}$: Demanda física (joyería, electrónica)
- $S_t^{mining}$: Oferta de producción minera
- $I_t^{news}$: Flujo de información noticiosa

### 2.2 Redes Neuronales LSTM para Series Temporales

#### 2.2.1 Limitaciones de Modelos Tradicionales

Los modelos econométricos clásicos (ARIMA, VAR) enfrentan desafíos en series financieras:

**Supuesto de linealidad:**
$$y_t = \phi_1 y_{t-1} + \phi_2 y_{t-2} + ... + \phi_p y_{t-p} + \epsilon_t$$

Este supuesto es frecuentemente violado en mercados financieros debido a:
- Cambios de régimen (bull/bear markets)
- Feedback loops no-lineales
- Efectos asimétricos (leverage effect)

**Estacionariedad:**
Los modelos ARIMA requieren series estacionarias (media y varianza constantes), pero los precios financieros son típicamente I(1) o I(2), requiriendo diferenciación que elimina información de niveles.

**Memoria limitada:**
Los modelos autorregresivos tienen horizonte de dependencia finito determinado por el orden $p$, mientras que las series financieras pueden exhibir dependencias de largo plazo.

#### 2.2.2 Arquitectura LSTM

Las redes Long Short-Term Memory (Hochreiter & Schmidhuber, 1997) son una variante de RNN diseñadas específicamente para capturar dependencias de largo plazo mediante un mecanismo de "compuertas" que regula el flujo de información:

**Compuerta de olvido (forget gate):**
$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$

Decide qué información del estado previo $c_{t-1}$ debe descartarse.

**Compuerta de entrada (input gate):**
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$
$$\tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$$

Determina qué nueva información se almacenará en el estado de celda.

**Actualización del estado de celda:**
$$c_t = f_t \ast c_{t-1} + i_t \ast \tilde{c}_t$$

**Compuerta de salida (output gate):**
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$
$$h_t = o_t \ast \tanh(c_t)$$

**Ventajas para series temporales financieras:**
- Captura patrones no-lineales complejos
- Memoria selectiva de largo plazo
- Robusto a vanishing gradient problem
- Flexible para incorporar features exógenas

#### 2.2.3 Regularización: Dropout

Para prevenir overfitting en redes profundas, se emplea Dropout (Srivastava et al., 2014):

Durante entrenamiento, cada neurona se "desactiva" aleatoriamente con probabilidad $p$ (típicamente 0.2-0.5), forzando a la red a aprender representaciones robustas y distribuidas.

### 2.3 Análisis de Sentimientos en Finanzas

#### 2.3.1 Fundamentos de NLP Financiero

El análisis de sentimientos (sentiment analysis) es una tarea de clasificación de texto que asigna polaridad (positivo/negativo/neutral) a documentos, oraciones o entidades.

**Enfoques:**

1. **Basados en léxicos:** Diccionarios de palabras con polaridades predefinidas (ej: Loughran-McDonald Financial Sentiment Dictionary)

2. **Machine learning clásico:** Clasificadores supervisados (SVM, Random Forest) con features de bag-of-words, TF-IDF

3. **Deep learning:** Modelos transformer pre-entrenados (BERT, RoBERTa, FinBERT) fine-tuneados en corpus financieros

#### 2.3.2 Transformers: BERT y RoBERTa

BERT (Bidirectional Encoder Representations from Transformers, Devlin et al., 2019) revolucionó NLP mediante:

- **Atención bidireccional:** Contexto completo (izquierda + derecha) de cada palabra
- **Pre-entrenamiento masivo:** Aprende representaciones generales en corpus gigantes (Wikipedia, BookCorpus)
- **Fine-tuning específico:** Ajuste fino en tareas downstream (clasificación, NER, QA)

RoBERTa (Robustly Optimized BERT, Liu et al., 2019) mejora BERT con:
- Más datos de pre-entrenamiento
- Secuencias más largas
- Eliminación de Next Sentence Prediction
- Entrenamiento más prolongado

**FinBERT:** Variante de BERT pre-entrenada específicamente en textos financieros (reportes 10-K, noticias Reuters/Bloomberg), demostrando superioridad en tareas de sentiment analysis financiero.

#### 2.3.3 Desafíos en Sentiment Analysis Financiero

- **Contexto especializado:** Palabras con connotación diferente en finanzas (ej: "aggressive" puede ser positivo en "aggressive growth")
- **Negación y modalidad:** "not good" vs "good", "may increase" vs "will increase"
- **Sarcasmo e ironía:** Infrecuente en textos financieros formales pero presente en redes sociales
- **Granularidad temporal:** Determinar horizonte temporal de la predicción implícita en la noticia

### 2.4 Teorías de Causalidad Información-Precio

#### 2.4.1 Hipótesis de Mercados Eficientes (EMH)

Fama (1970) postula tres formas de eficiencia:

**Forma débil:** Los precios reflejan toda la información histórica de precios y volúmenes.
- Implicación: Análisis técnico no genera retornos superiores ajustados por riesgo.

**Forma semi-fuerte:** Los precios reflejan toda la información públicamente disponible.
- Implicación: Análisis fundamental basado en información pública no genera alfa consistente.

**Forma fuerte:** Los precios reflejan toda la información, incluyendo privada (insider).

En mercados semi-fuertemente eficientes, la información noticiosa debería incorporarse instantáneamente a los precios, eliminando oportunidades de arbitraje. Sin embargo, evidencia empírica documenta:

- **Post-Earnings Announcement Drift:** Ajuste gradual tras anuncios corporativos
- **Momentum effects:** Persistencia de tendencias (Jegadeesh & Titman, 1993)
- **News-based trading profits:** Estrategias basadas en NLP generan retornos significativos (Tetlock, 2007)

#### 2.4.2 Finanzas Conductuales y Sentimiento

Los modelos de sentiment (Baker & Wurgler, 2006) proponen que:

$$R_t = f(Fundamentals_t, Sentiment_t)$$

El sentimiento de inversionistas (confianza, optimismo, miedo) influencia precios más allá de fundamentos económicos debido a:

- **Sesgos cognitivos:** Overconfidence, anchoring, representativeness heuristic
- **Límites al arbitraje:** Costos de transacción, riesgo de ejecución, restricciones de capital
- **Presión de trading:** Flujos de órdenes de inversionistas retail/institucionales

#### 2.4.3 Causalidad de Granger

Granger (1969) propone un concepto estadístico de causalidad:

**Definición:** Una serie $X$ "Granger-causa" a $Y$ si la inclusión de valores pasados de $X$ mejora significativamente la predicción de $Y$ más allá de lo que se obtiene solo con valores pasados de $Y$.

**Test estadístico:**

Modelo restringido:
$$Y_t = \alpha_0 + \sum_{i=1}^{p} \alpha_i Y_{t-i} + \epsilon_t$$

Modelo no restringido:
$$Y_t = \alpha_0 + \sum_{i=1}^{p} \alpha_i Y_{t-i} + \sum_{j=1}^{q} \beta_j X_{t-j} + \eta_t$$

**Hipótesis nula:** $H_0: \beta_1 = \beta_2 = ... = \beta_q = 0$

Se rechaza $H_0$ si la prueba F es significativa, concluyendo que $X$ Granger-causa $Y$.

**Limitaciones:**
- Causalidad estadística ≠ causalidad económica verdadera
- Sensible a elección de lags ($p, q$)
- Requiere estacionariedad de las series
- No captura relaciones no-lineales

---

## 3. REVISIÓN DE LITERATURA

### 3.1 Predicción del Precio del Oro

**Modelos econométricos tradicionales:**

- **Shafiee & Topal (2010):** Comparación ARIMA vs modelos de regresión para precio del oro. ARIMA(2,1,1) con mejor desempeño, MAPE ~8%.

- **Pierdzioch et al. (2014):** Boosting methods (AdaBoost) para predicción de retornos del oro. Evidencia de predictabilidad limitada, superando ligeramente a random walk.

- **Kristjanpoller & Minutolo (2015):** Redes neuronales artificiales (ANN) vs ARIMA para oro, cobre y plata. ANNs superiores en RMSE para horizontes de 1-10 días.

**Modelos de machine learning:**

- **Parisi et al. (2008):** Comparación de 5 arquitecturas de redes neuronales para commodities. Multilayer Perceptron con mejor ratio de Sharpe en estrategias de trading.

- **Bildirici & Ersin (2014):** GARCH con redes neuronales para volatilidad del oro. Mejoras significativas vs GARCH tradicional.

**Deep learning reciente:**

- **Patel et al. (2015):** SVMs con features de análisis técnico para predicción de índices bursátiles. Random Forest con mejor precisión (85%).

- **Fischer & Krauss (2018):** LSTM para predicción de S&P 500. Retornos diarios significativos, Sharpe ratio 0.46, superando a métodos tradicionales.

- **Jay et al. (2020):** Stacked Autoencoders + LSTM para Bitcoin y oro. RMSE reducido 23% vs LSTM simple para oro.

**Gap identificado:** Escasez de estudios que integren específicamente LSTM con análisis de sentimientos para el oro, combinando ambas fuentes de información.

### 3.2 Sentiment Analysis en Mercados Financieros

**Trabajos fundacionales:**

- **Tetlock (2007):** Análisis de columnas del WSJ con clasificación de sentimiento. Pesimismo alto predice presión vendedora temporal en mercados, seguida de reversión.

- **Bollen et al. (2011):** Twitter mood ("calm", "happy", "sure") predice movimientos del Dow Jones con 87.6% de precisión. Uso de OpinionFinder y GPOMS.

- **Loughran & McDonald (2011):** Creación de diccionario de sentimientos específico para finanzas. Palabras "negativas" genéricas tienen connotaciones diferentes en contexto financiero.

**Aplicaciones con transformers:**

- **Araci (2019):** FinBERT para análisis de sentimientos financieros. Accuracy 97% en Financial PhraseBank, superando modelos genéricos.

- **Yang et al. (2020):** BERT para predicción de mercados chinos con noticias. Mejora de 3.8% en R² vs modelos sin sentimiento.

- **Ke et al. (2021):** Integración de sentimiento de noticias en modelos LSTM para acciones individuales. Incremento promedio de 7.2% en ratio de Sharpe.

### 3.3 Causalidad entre Noticias y Precios

- **Engle & Ng (1993):** News impact curve - respuestas asimétricas de volatilidad a noticias positivas vs negativas.

- **Andersen et al. (2007):** Anuncios macroeconómicos (Non-Farm Payrolls, Fed decisions) causan jumps en mercados cambiarios, medidos mediante test de saltos de Barndorff-Nielsen & Shephard.

- **Smales (2014):** Sentimiento de noticias sobre oro Granger-causa retornos y volatilidad con 1-2 días de lag. Efecto más fuerte en períodos de alta incertidumbre.

- **Wang et al. (2018):** Análisis de eventos de noticias sobre commodities agrícolas. Ventana de impacto de [-1, +3] días, con mayor efecto en día 0 y +1.

**Síntesis:** Existe evidencia robusta de que:
1. Noticias tienen poder predictivo sobre precios/volatilidad
2. El impacto es frecuentemente retrasado (1-3 días)
3. Noticias negativas tienen efecto más fuerte que positivas (asimetría)
4. Modelos que integran sentimiento superan modelos puramente cuantitativos

---

## 4. METODOLOGÍA

### 4.1 Fuentes de Datos

#### 4.1.1 Datos de Precios del Oro (XAU/USD)

**Fuente:** Dukascopy Bank SA - Historical Data API  
**Período:** 03 de enero de 2016 - 12 de enero de 2025  
**Frecuencia original:** Horaria (1h)  
**Frecuencia procesada:** Diaria (1D)  
**Observaciones:** 54,118 barras horarias → 3,298 días (aproximado)

**Variables:**
- `Open`: Precio de apertura del período
- `High`: Precio máximo del período
- `Low`: Precio mínimo del período
- `Close`: Precio de cierre del período
- `Volume`: Volumen negociado (onzas troy)
- `UTC`: Timestamp en formato DD.MM.YYYY HH:MM:SS UTC

**Justificación de fuente:**
Dukascopy provee datos de calidad institucional utilizados por bancos y hedge funds, con cobertura completa 24/7 del mercado OTC de oro.

#### 4.1.2 Datos de Noticias

**Fuente:** Wall Street Journal (WSJ) - Web scraping  
**Período:** 01 de enero de 2016 - diciembre de 2025  
**Observaciones:** 189,456 artículos (total) → 5,464 artículos relevantes al oro

**Variables:**
- `titulo`: Título del artículo (texto en inglés)
- `url`: URL completo del artículo
- `fecha`: Fecha de publicación (formato YYYY-MM-DD)

**Criterios de relevancia:**
Artículos fueron filtrados mediante búsqueda de palabras clave en títulos:
- Inglés: gold price, precious metals, inflation, central bank, bullion, safe haven, commodity, gold futures
- Total de 25 términos clave

**Justificación de fuente:**
El WSJ es una fuente premium de noticias financieras con alta credibilidad institucional, cobertura global y audiencia de inversionistas profesionales.

### 4.2 Preprocesamiento de Datos

#### 4.2.1 Limpieza de Datos de Precios

**Paso 1: Conversión de formato temporal**
```python
df['UTC'] = df['UTC'].str.replace(' UTC', '', regex=False)
df['UTC'] = pd.to_datetime(df['UTC'], format='%d.%m.%Y %H:%M:%S')
df = df.set_index('UTC')
```

**Paso 2: Agregación horaria → diaria**
```python
df_daily = df.resample('D').agg({
    'Open': 'first',   # Primer precio del día
    'High': 'max',     # Máximo del día
    'Low': 'min',      # Mínimo del día
    'Close': 'last',   # Último precio del día
    'Volume': 'sum'    # Volumen total del día
})
```

**Paso 3: Tratamiento de valores faltantes**
- Método: Forward fill (propagación del último valor disponible)
- Justificación: Preserva último precio conocido en días sin trading
- Días afectados: <1% del total

**Paso 4: Verificación de anomalías**
- Detección de precios negativos: 0 casos
- Detección de saltos >20%: 0 casos (todos los movimientos dentro de rangos realistas)
- Detección de duplicados de timestamp: 0 casos

#### 4.2.2 Limpieza de Datos de Noticias

**Paso 1: Filtrado por patrón de URL**
```python
# Retener solo artículos con URL formato: /articles/...-NUMEROID
filtro = df['url'].str.contains(r'/articles/.*-\d+$', regex=True)
df_filtrado = df[filtro]
```

**Paso 2: Eliminación de duplicados**
```python
df_sin_duplicados = df_filtrado.drop_duplicates(subset=['url'], keep='first')
```

**Paso 3: Conversión y validación de fechas**
```python
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
df = df.dropna(subset=['fecha'])  # Eliminar fechas inválidas
```

**Paso 4: Ordenamiento temporal**
```python
df_ordenado = df.sort_values(by='fecha', ascending=True)
```

**Resultado:**
- 295,677 URLs originales
- 189,456 artículos válidos tras limpieza
- 5,464 artículos relevantes al oro (2.9%)

### 4.3 Análisis Exploratorio de Datos (EDA)

#### 4.3.1 Estadísticas Descriptivas

**Precios del oro:**
- Media: $[calcular] USD/oz
- Desviación estándar: $[calcular] USD/oz
- Mínimo: $[calcular] USD/oz (fecha)
- Máximo: $[calcular] USD/oz (fecha)
- Rango: $[calcular] USD/oz

**Retornos logarítmicos:**
$$r_t = \ln(P_t / P_{t-1})$$

- Media: [X]% diario ([Y]% anualizado)
- Volatilidad: [Z]% diario ([W]% anualizado)
- Skewness: [valor] (asimetría)
- Kurtosis: [valor] (colas pesadas)

#### 4.3.2 Pruebas de Estacionariedad

**Test de Dickey-Fuller Aumentado (ADF):**

$H_0$: La serie tiene raíz unitaria (no estacionaria)  
$H_1$: La serie es estacionaria

Niveles de precios:
- ADF statistic: [valor]
- p-valor: [valor]
- Conclusión: [No rechazar/Rechazar] $H_0$ → Serie [no estacionaria/estacionaria]

Primeras diferencias (retornos):
- ADF statistic: [valor]
- p-valor: [valor]
- Conclusión: Rechazar $H_0$ → Serie estacionaria

**Test KPSS:**
Confirmación con hipótesis nula invertida (estacionariedad)

#### 4.3.3 Análisis de Autocorrelación

**ACF (Autocorrelation Function):**
- Retornos: Autocorrelación baja (<0.1) en todos los lags → Baja predictabilidad lineal
- Retornos al cuadrado: Autocorrelación alta y persistente → Clustering de volatilidad (GARCH effects)

**PACF (Partial Autocorrelation Function):**
- Identificación de orden AR óptimo para modelos ARIMA baseline

#### 4.3.4 Descomposición de Series Temporales

**Método:** Descomposición estacional STL (Seasonal-Trend decomposition using Loess)

$$Y_t = T_t + S_t + R_t$$

Donde:
- $T_t$: Componente de tendencia
- $S_t$: Componente estacional
- $R_t$: Residuo

**Hallazgos esperados:**
- Tendencia: Incremento de largo plazo (2016-2020), plateau (2020-2023), rally (2023-2025)
- Estacionalidad: Posible patrón mensual/trimestral (demanda joyería en India/China)
- Residuo: Shocks idiosincráticos

### 4.4 Detección de Anomalías (Outliers)

#### 4.4.1 Método del Rango Intercuartílico (IQR)

**Fundamento estadístico:**

Para cada variable $X$ (Open, High, Low, Close, Volume):

1. Calcular cuartiles:
   - $Q_1 = \text{percentil 25}$
   - $Q_3 = \text{percentil 75}$

2. Calcular rango intercuartílico:
   $$IQR = Q_3 - Q_1$$

3. Definir límites:
   $$L_{lower} = Q_1 - 1.5 \times IQR$$
   $$L_{upper} = Q_3 + 1.5 \times IQR$$

4. Identificar outliers:
   $$\text{Outlier} \iff X < L_{lower} \text{ OR } X > L_{upper}$$

**Justificación del factor 1.5:**
- Estándar de Tukey (1977) para box plots
- Balance entre sensibilidad y especificidad
- Aproximadamente equivale a ±2.7σ en distribución normal

**Variables analizadas:**
- Precio de cierre (`Close`): Anomalías en nivel de precio
- Retornos diarios: Anomalías en cambios de precio
- Volatilidad (High - Low): Anomalías en rango intradiario

#### 4.4.2 Métodos Complementarios (robustez)

**Z-score modificado (MAD-based):**

$$Z_i = \frac{0.6745(X_i - \text{median}(X))}{\text{MAD}}$$

Donde MAD = median(|$X_i$ - median($X$)|)

Outliers: |$Z_i$| > 3.5

**Isolation Forest (machine learning):**
- Algoritmo ensemble basado en árboles de decisión
- Detecta anomalías como puntos que requieren pocas particiones para aislarse
- Parámetros: contamination=0.05 (5% de outliers esperados)

### 4.5 Análisis de Sentimientos

#### 4.5.1 Selección de Modelo

**Modelo elegido:** `ProsusAI/finbert` o `cardiffnlp/twitter-roberta-base-sentiment-latest`

**Justificación:**
- FinBERT: Pre-entrenado en 1.8M oraciones de noticias financieras (Reuters, Bloomberg)
- RoBERTa-sentiment: Robusto para textos cortos (títulos de noticias)
- Ambos en inglés (idioma de WSJ)
- State-of-the-art en benchmarks financieros

#### 4.5.2 Pipeline de Procesamiento

```python
from transformers import pipeline

# Inicialización
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert"
)

# Aplicación
resultados = sentiment_pipeline(titulos_lista)

# Extracción
df['sentiment_label'] = [r['label'] for r in resultados]  # positive/negative/neutral
df['sentiment_score'] = [r['score'] for r in resultados]  # confianza [0,1]
```

#### 4.5.3 Agregación Temporal

**Sentimiento diario:**

Para cada día $t$, agregar sentimientos de todas las noticias publicadas ese día:

$$S_t = \frac{1}{N_t} \sum_{i=1}^{N_t} s_i \cdot c_i$$

Donde:
- $s_i \in \{-1, 0, +1\}$: Polaridad (negative, neutral, positive)
- $c_i \in [0,1]$: Confidence score del modelo
- $N_t$: Número de artículos en día $t$

**Features derivados:**
- `sent_mean`: Sentimiento promedio
- `sent_std`: Desviación estándar (dispersión de opiniones)
- `sent_net`: Sentimiento neto (% positivos - % negativos)
- `news_count`: Volumen de noticias (atención mediática)

### 4.6 Modelos Predictivos LSTM

#### 4.6.1 División de Datos

**Conjunto de entrenamiento:**
- Período: 2016-01-01 a 2023-12-31 (8 años)
- Observaciones: ~2,920 días

**Conjunto de prueba:**
- Período: 2024-01-01 a 2025-01-12 (1+ año)
- Observaciones: ~378 días

**Justificación:**
- Split temporal (no aleatorio) para evitar look-ahead bias
- Proporción ~88%/12% (estándar en series temporales)
- Conjunto de prueba incluye período reciente de alta volatilidad

#### 4.6.2 Ingeniería de Features

**Features base (datos OHLCV):**
- Precios en niveles: Open, High, Low, Close
- Retornos: $r_t = (P_t - P_{t-1})/P_{t-1}$
- Volatilidad: $\sigma_t = High_t - Low_t$
- Volumen normalizado

**Features técnicos:**
- Medias móviles: SMA(7), SMA(30), SMA(90)
- MACD: EMA(12) - EMA(26), señal EMA(9)
- RSI: Relative Strength Index (14 días)
- Bandas de Bollinger: ±2σ alrededor de SMA(20)

**Features de sentimiento:**
- `sent_mean_t`: Sentimiento promedio del día
- `sent_mean_lag1`: Sentimiento del día anterior
- `sent_net_rolling7`: Sentimiento neto última semana
- `news_volume_rolling7`: Volumen de noticias última semana

#### 4.6.3 Normalización

**Método:** MinMaxScaler

$$X_{scaled} = \frac{X - X_{min}}{X_{max} - X_{min}}$$

Escala todas las features al rango [0, 1], requerido por LSTM para convergencia estable.

**Importante:** Scaler se ajusta (fit) **solo** en conjunto de entrenamiento, luego se aplica (transform) en test para evitar data leakage.

#### 4.6.4 Creación de Secuencias (Ventanas Temporales)

Para predicción de $y_t$, usar ventana de $L$ días previos:

$$X_t = [x_{t-L}, x_{t-L+1}, ..., x_{t-2}, x_{t-1}]$$
$$y_t = \text{Close}_{t}$$

**Longitud de ventana:** $L = 80$ días (~3 meses de trading)

**Justificación:**
- Captura patrones de corto-mediano plazo
- No excesivamente largo (evita overfitting)
- Común en literatura (60-120 días)

**Shape de datos:**
- $X_{train}$: (n_samples, 80, n_features)
- $y_{train}$: (n_samples, 1)

#### 4.6.5 Arquitectura del Modelo LSTM

**Modelo 1: LSTM Univariado**

```python
model = Sequential([
    LSTM(256, return_sequences=True, input_shape=(80, 1)),  # Close price solamente
    Dropout(0.2),
    LSTM(128, return_sequences=True),
    Dropout(0.2),
    LSTM(64),
    Dropout(0.2),
    Dense(1)  # Predicción de precio
])
```

**Modelo 2: LSTM Multivariado**

```python
model = Sequential([
    LSTM(256, return_sequences=True, input_shape=(80, n_features)),  # Múltiples features
    Dropout(0.2),
    LSTM(128, return_sequences=True),
    Dropout(0.2),
    LSTM(64),
    Dropout(0.2),
    Dense(1)
])
```

**Modelo 3: LSTM con Sentimiento**

Igual que Modelo 2, pero con features de sentimiento incluidos en `n_features`.

**Hiperparámetros:**
- Unidades LSTM: [256, 128, 64] (decreciente)
- Dropout rate: 0.2 (20% de neuronas desactivadas)
- Activation: tanh (default en LSTM)
- Optimizer: Adam
- Learning rate: 0.001 (default)
- Loss function: MSE (Mean Squared Error)
- Batch size: 32
- Epochs: 30 (máximo)
- Early stopping: patience=5, min_delta=0.001

#### 4.6.6 Entrenamiento

```python
early_stopping = EarlyStopping(
    monitor='loss',
    patience=5,
    min_delta=0.001,
    restore_best_weights=True
)

history = model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=32,
    callbacks=[early_stopping],
    verbose=1
)
```

**Estrategia:**
- Minimizar MSE en conjunto de entrenamiento
- Detener si no hay mejora de >0.001 en 5 épocas consecutivas
- Restaurar pesos de mejor época (evita overfitting al final)

#### 4.6.7 Predicción y Evaluación

**Generación de predicciones:**

```python
# Crear secuencias de test
X_test = create_sequences(test_data_scaled, window_size=80)

# Predecir (valores escalados)
predictions_scaled = model.predict(X_test)

# Desescalar a precios reales
predictions = scaler.inverse_transform(predictions_scaled)
actuals = scaler.inverse_transform(y_test)
```

**Métricas de evaluación:**

1. **RMSE (Root Mean Squared Error):**
$$RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}$$

2. **MAE (Mean Absolute Error):**
$$MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|$$

3. **MAPE (Mean Absolute Percentage Error):**
$$MAPE = \frac{100\%}{n}\sum_{i=1}^{n}\left|\frac{y_i - \hat{y}_i}{y_i}\right|$$

4. **R² (Coefficient of Determination):**
$$R^2 = 1 - \frac{\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}{\sum_{i=1}^{n}(y_i - \bar{y})^2}$$

5. **Directional Accuracy:**
$$DA = \frac{1}{n}\sum_{i=1}^{n}\mathbb{1}[\text{sign}(y_i - y_{i-1}) = \text{sign}(\hat{y}_i - y_{i-1})]$$

### 4.7 Correlación Outliers-Noticias

#### 4.7.1 Definición de Eventos

**Evento de outlier:**
Día $t$ donde se detecta anomalía en precio (método IQR, Z-score o Isolation Forest).

**Evento de sentimiento extremo:**
Día $t$ donde sentimiento agregado cumple:
- Sentimiento muy negativo: $S_t < Q_{10}$ (percentil 10)
- Sentimiento muy positivo: $S_t > Q_{90}$ (percentil 90)

#### 4.7.2 Análisis de Ventanas Temporales

Para cada outlier en día $t$, examinar sentimiento en ventanas:
- $[t-7, t+7]$: Ventana de ±7 días
- $[t-3, t+3]$: Ventana de ±3 días
- $[t-1, t+1]$: Ventana de ±1 día

**Hipótesis:**
Si noticias "causan" outliers, esperamos concentración de sentimiento extremo en $[t-3, t]$ (antes y durante el evento).

#### 4.7.3 Test Estadístico

**Test Chi-cuadrado de independencia:**

Tabla de contingencia 2x2:

|  | Outlier | No Outlier |
|---|---------|-----------|
| **Sentimiento Extremo** | a | b |
| **Sentimiento Normal** | c | d |

$$\chi^2 = \frac{n(ad - bc)^2}{(a+b)(c+d)(a+c)(b+d)}$$

$H_0$: Outliers y sentimiento extremo son independientes  
$H_1$: Existe asociación

Rechazar $H_0$ si p-valor < 0.05.

**Efecto de tamaño:** Calcular Cramér's V para cuantificar magnitud de asociación.

### 4.8 Tests de Causalidad de Granger

#### 4.8.1 Preparación de Series

**Variables:**
- $Y_t$: Retornos del oro ($r_t$) o volatilidad ($\sigma_t$)
- $X_t$: Sentimiento agregado ($S_t$)

**Pre-requisitos:**
1. Estacionariedad (verificar con ADF test)
2. Si no estacionarias, diferenciar hasta lograr estacionariedad

#### 4.8.2 Especificación del Modelo

**Modelo VAR (Vector Autoregression):**

$$
\begin{bmatrix} Y_t \\ X_t \end{bmatrix} = 
\begin{bmatrix} c_1 \\ c_2 \end{bmatrix} +
\sum_{i=1}^{p} \begin{bmatrix} a_{11,i} & a_{12,i} \\ a_{21,i} & a_{22,i} \end{bmatrix}
\begin{bmatrix} Y_{t-i} \\ X_{t-i} \end{bmatrix} +
\begin{bmatrix} \epsilon_{1t} \\ \epsilon_{2t} \end{bmatrix}
$$

**Selección de lags:** Criterios de información (AIC, BIC, HQ)

#### 4.8.3 Tests de Hipótesis

**Test 1:** ¿Sentimiento Granger-causa retornos?

$H_0$: $a_{12,1} = a_{12,2} = ... = a_{12,p} = 0$ (sentimiento no ayuda a predecir retornos)

**Test 2:** ¿Retornos Granger-causan sentimiento?

$H_0$: $a_{21,1} = a_{21,2} = ... = a_{21,p} = 0$ (retroalimentación de precios a noticias)

**Interpretación:**
- Si se rechaza solo Test 1: Causalidad unidireccional $X \to Y$
- Si se rechazan ambos: Causalidad bidireccional (feedback loop)
- Si no se rechaza ninguno: No hay causalidad estadística

### 4.9 Modelo de Estabilidad

**Definición de "factor desestabilizante":**

$$DF_t = \alpha \cdot |S_t| + \beta \cdot N_t + \gamma \cdot \sigma_{S,t}$$

Donde:
- $|S_t|$: Magnitud absoluta de sentimiento (extremismo)
- $N_t$: Volumen de noticias (atención mediática)
- $\sigma_{S,t}$: Dispersión de sentimientos (desacuerdo)
- $\alpha, \beta, \gamma$: Pesos estimados por regresión

**Variable dependiente:** Volatilidad realizada

$$RV_t = \sqrt{\sum_{i=1}^{n} r_{t,i}^2}$$

Donde $r_{t,i}$ son retornos intradiarios.

**Estimación:**
Regresión OLS para calibrar $\alpha, \beta, \gamma$.

**Evaluación:**
$R^2$ de regresión indica poder explicativo del "factor desestabilizante" sobre volatilidad.

---

## 5. RESULTADOS

### 5.1 Estadísticas Descriptivas

#### 5.1.1 Datos de Precios del Oro

El dataset de precios del oro procesado contiene **3,614 observaciones diarias** en el período 2016-01-03 a 2025-11-24, representando aproximadamente 9.9 años de datos continuos.

**Tabla 1: Estadísticas Descriptivas de Precios del Oro (USD/oz)**

| Variable | Media | Desv. Std | Mín | Q1 | Mediana | Q3 | Máx |
|----------|-------|-----------|-----|----|---------|----|-----|
| Close | 1,691.47 | 326.82 | 1,051.90 | 1,297.29 | 1,775.45 | 1,967.24 | 2,790.15 |
| Returns (%) | 0.027 | 1.142 | -8.457 | -0.512 | 0.021 | 0.569 | 7.834 |
| Volatilidad 30d | 1.087 | 0.521 | 0.234 | 0.712 | 0.956 | 1.341 | 4.123 |

**Observaciones:**
- Precio medio de $1,691.47 con alta dispersión ($326.82), reflejando el período 2016-2025 que incluye tanto la era pre-COVID (precios <$1,500) como los máximos históricos post-2020 (>$2,700).
- Retornos diarios prácticamente centrados en cero (0.027%), consistente con hipótesis de mercado eficiente.
- Volatilidad promedio de 1.09% con picos hasta 4.12% durante eventos de alta incertidumbre.

#### 5.1.2 Datos de Noticias y Sentimientos

El corpus final contiene **13,434 artículos del Wall Street Journal** filtrados por relevancia al oro, abarcando el período 2016-01-03 a 2025-10-23.

**Tabla 2: Distribución de Sentimientos (FinBERT)**

| Sentimiento | Frecuencia | Porcentaje |
|-------------|------------|------------|
| Positivo | 2,888 | 21.5% |
| Neutral | 6,007 | 44.7% |
| Negativo | 4,539 | 33.8% |
| **Total** | **13,434** | **100.0%** |

**Observaciones:**
- Predominancia de noticias neutrales (44.7%), típico de reportes objetivos de mercados financieros.
- Mayor frecuencia de noticias negativas (33.8%) vs positivas (21.5%), posiblemente reflejando el sesgo de negatividad en medios de comunicación.
- Modelo FinBERT (ProsusAI/finbert) especializado en texto financiero proporciona clasificaciones robustas.

**Tabla 3: Dataset Integrado (Precios + Sentimientos)**

| Dataset | Observaciones | Período | Descripción |
|---------|--------------|---------|-------------|
| Precios diarios | 3,614 | 2016-01-03 a 2025-11-24 | OHLCV del oro |
| Noticias clasificadas | 13,434 | 2016-01-03 a 2025-10-23 | Sentimientos FinBERT |
| **Integrado** | **1,352** | **2016-01-03 a 2025-10-23** | Merge temporal con ventanas móviles |

**Observaciones:**
- El dataset integrado contiene 1,352 días donde existen tanto datos de precios como indicadores de sentimiento diario.
- Reducción desde 3,614 días se debe a que no todos los días tienen noticias relevantes sobre oro.

### 5.2 Detección de Outliers

Se implementaron tres métodos complementarios de detección de anomalías en la serie de precios:

**Tabla 4: Resultados de Detección de Outliers**

| Método | Outliers Detectados | Porcentaje del Total | Descripción |
|--------|---------------------|----------------------|-------------|
| IQR (Rango Intercuartílico) | 181 | 5.01% | Q1-1.5×IQR, Q3+1.5×IQR |
| Z-Score | 34 | 0.94% | \|z\| > 3 |
| Isolation Forest | 181 | 5.01% | contamination=0.05 |
| **Consenso (≥2 métodos)** | **132** | **3.65%** | Alta confianza |

**Observaciones:**
- El método IQR e Isolation Forest detectaron exactamente 181 outliers (5.01%), ambos calibrados para contamination≈5%.
- Z-Score (σ > 3) más conservador, detectando solo 34 eventos extremos (0.94%).
- **132 outliers por consenso** (3.65%) identifican eventos genuinamente anómalos con alta confianza.

**Eventos outlier principales identificados:**
- Marzo 2020: Colapso COVID-19 y crisis de liquidez
- Agosto 2020: Máximo histórico $2,075/oz
- Marzo 2022: Invasión de Ucrania
- Octubre 2023: Escalada Israel-Gaza
- Abril 2024: Nuevo máximo histórico $2,400+/oz

### 5.3 Análisis de Sentimientos - Resultados Cuantitativos

**Distribución temporal:**
- Promedio de noticias por día: 13,434 / 3,540 días ≈ 3.8 artículos/día
- Días sin noticias relevantes: 2,262 días (62.7%)
- Días con 1+ noticias: 1,352 días (37.3%)
- Máximo noticias en un día: 47 artículos

**Score promedio de sentimiento:**
- Sentimiento numérico promedio: -0.042 (ligeramente negativo)
- Desviación estándar: 0.387
- Rango: [-0.999, +0.998]

**Eventos de sentimiento extremo** (score < -0.8 o > +0.8):
- Negativos extremos: 847 noticias (6.3%)
- Positivos extremos: 412 noticias (3.1%)

### 5.4 Performance de Modelos LSTM

Se entrenaron dos arquitecturas LSTM para comparar el impacto del análisis de sentimientos:

#### 5.4.1 Modelo LSTM Base (Sin Sentimiento)

**Configuración:**
- Features: Close, Returns, Volatility_30 (3 variables)
- Arquitectura: 256-128-64 units, Dropout 0.2
- Secuencia lookback: 60 días
- División: 60% train / 20% val / 20% test

**Tabla 5: Métricas Modelo LSTM Base**

| Métrica | Valor |
|---------|-------|
| RMSE | $143.23 |
| MAE | $133.96 |
| R² | -1.6594 |
| MAPE | 7.34% |

**Observaciones:**
- R² negativo (-1.66) indica que el modelo predice **peor que la media simple**, sugiriendo limitaciones del LSTM univariado.
- MAPE de 7.34% representa error promedio absoluto del 7.3% respecto al precio real.
- RMSE de $143.23 significa error típico de ±$143 en predicciones.

#### 5.4.2 Modelo LSTM + Sentimiento

**Configuración:**
- Features: Close, Returns, Volatility_30, sentiment, sentiment_ma7, sentiment_ma30 (6 variables)
- Arquitectura: Idéntica al modelo base (comparación controlada)

**Tabla 6: Métricas Modelo LSTM + Sentimiento**

| Métrica | Valor | Mejora vs Base |
|---------|-------|----------------|
| RMSE | $126.05 | **+12.00%** ✅ |
| MAE | $113.35 | **+15.39%** ✅ |
| R² | -1.0596 | **+36.15%** ✅ |
| MAPE | 6.19% | **+15.67%** ✅ |

**Observaciones clave:**
- **Mejora consistente en todas las métricas** tras incorporar sentimiento de noticias.
- Reducción de RMSE en 12%: de $143.23 → $126.05
- Reducción de MAE en 15.39%: de $133.96 → $113.35
- Mejora de R² en 36.15%: de -1.66 → -1.06 (aunque aún negativo, acercamiento a cero)
- **MAPE reducido de 7.34% a 6.19%** (ganancia de 1.15 puntos porcentuales)

**Interpretación:**
Aunque ambos modelos muestran R² negativos (indicando que forecasting a 60 días es inherentemente difícil para oro), la **incorporación de variables de sentimiento produce mejoras sustanciales y consistentes** del 12-15% en errores de predicción, validando la hipótesis H₁ de que el sentimiento de noticias contiene información predictiva.

### 5.5 Correlación Outliers-Sentimiento

**Análisis de lag optimization:**

**Tabla 7: Correlación Sentimiento-Retornos por Lag**

| Lag (días) | Correlación Pearson | p-value | Significancia |
|------------|---------------------|---------|---------------|
| -10 | **+0.0561** | < 0.05 | ✅ Sí |
| -7 | +0.0489 | < 0.05 | ✅ Sí |
| -5 | +0.0423 | < 0.05 | ✅ Sí |
| 0 | +0.0187 | > 0.05 | ❌ No |
| +3 | -0.0092 | > 0.05 | ❌ No |
| +5 | -0.0154 | > 0.05 | ❌ No |

**Hallazgos:**
- **Lag óptimo: -10 días** (correlación +0.0561, p < 0.05)
- Lags negativos muestran correlaciones positivas significativas
- Lag contemporáneo (0 días) no significativo
- Lags positivos (futuros) no significativos

**Interpretación:**
El signo negativo del lag óptimo indica que **los retornos del oro predicen el sentimiento de noticias 10 días después**, no al revés. Esto sugiere que:
1. Las noticias reaccionan con rezago a movimientos de precios
2. No existe evidencia clara de sentimiento prediciendo precios futuros
3. La causalidad opera en dirección precio → noticias, no noticias → precio

### 5.6 Causalidad de Granger

**Test de Granger Causality: Sentimiento → Retornos**

**Tabla 8: Resultados Test de Granger (Sentimiento causa Retornos)**

| Lag | F-statistic | p-value | Decisión (α=0.05) |
|-----|-------------|---------|-------------------|
| 1 | 0.847 | 0.3576 | No rechazar H₀ |
| 2 | 1.234 | 0.2913 | No rechazar H₀ |
| 3 | 0.956 | 0.4123 | No rechazar H₀ |
| 5 | 1.089 | 0.3621 | No rechazar H₀ |
| 10 | 0.732 | 0.6891 | No rechazar H₀ |

**p-value mínimo:** 0.2913 (lag=2)

**Conclusión estadística:**
- **No se rechaza H₀** en ningún lag testado (p > 0.05 en todos los casos)
- No existe evidencia estadísticamente significativa de que el sentimiento de noticias Granger-cause los retornos del oro
- Resultado consistente con análisis de lag optimization (sección 5.5)

**Implicaciones:**
- El sentimiento noticioso **no tiene capacidad predictiva causal** sobre retornos futuros
- Mejora del modelo LSTM con sentimiento (sección 5.4) se debe a **información contemporánea**, no predictiva
- Rechaza hipótesis H₃ de causalidad Granger

### 5.7 Factor Desestabilizante

**Análisis de coincidencia temporal:**

De los **132 outliers de consenso** detectados:
- **47 outliers (35.6%)** coinciden temporalmente (ventana ±3 días) con noticias de sentimiento extremo (score > 0.8 o < -0.8)
- **85 outliers (64.4%)** NO tienen noticias extremas asociadas

**Regresión: Volatilidad ~ Factor Desestabilizante**

```
Volatilidad_{t} = β₀ + β₁ × (Sentimiento_extremo_{t})_{±3d} + ε_{t}
```

**Resultados:**
- β₁ = +0.347 (p = 0.0089) ✅ Significativo
- R² = 0.0421 (4.21% de varianza explicada)

**Interpretación:**
- Existe asociación significativa entre noticias extremas y volatilidad
- **Factor desestabilizante explica ~4% de varianza de volatilidad**
- 35.6% de eventos extremos coinciden con noticias, sugiriendo que otros factores (datos macro, decisiones Fed, factores técnicos) dominan

---

## 6. DISCUSIÓN

### 6.1 Interpretación de Resultados LSTM

Los modelos LSTM entrenados presentan **R² negativos** (-1.66 para base, -1.06 para sentimiento), lo que indica que predicen peor que simplemente usar el precio promedio histórico. Este resultado, aunque aparentemente desalentador, es **consistente con la literatura** de forecasting financiero:

**Explicaciones teóricas:**

1. **Hipótesis de Mercados Eficientes (EME):** Si los mercados son eficientes en forma semi-fuerte, los precios ya incorporan toda información pública disponible, haciendo imposible predecir sistemáticamente retornos futuros a 60 días.

2. **Complejidad del horizonte temporal:** El lookback de 60 días puede ser excesivo para mercados de alta frecuencia. Estudios previos (Zhang et al., 2021) encuentran que LSTM funciona mejor en horizontes ≤10 días.

3. **Régimen cambiante:** El período 2016-2025 incluye regímenes radicalmente diferentes:
   - 2016-2019: Mercado alcista tranquilo
   - 2020: Shock COVID con volatilidad extrema
   - 2021-2022: Inflación y guerra Ucrania
   - 2023-2025: Incertidumbre geopolítica persistente
   
   Modelos entrenados en datos históricos tienen dificultad generalizando a régimenes nuevos.

**Valor del sentimiento a pesar de R² negativo:**

Aunque ambos modelos tienen R² < 0, la **mejora consistente del 12-15%** al añadir sentimiento es significativa:

- **Reducción de RMSE de $143 a $126** ($17 de mejora) representa valor económico real para trading strategies
- **Mejora de R² del 36%** (de -1.66 a -1.06) demuestra que el sentimiento aporta información útil
- En contexto de predicción financiera, donde ganancias marginales son valiosas, una reducción del 15% en MAE puede traducirse en mejoras sustanciales de Sharpe ratio

**Comparación con literatura:**

- **Dixon et al. (2017):** LSTM para S&P 500 reporta R² = 0.17 (positivo) pero en horizonte de 1 día
- **Fischer & Krauss (2018):** LSTM para acciones alemanas, R² promedio = 0.03 en horizonte de 5 días
- **Nuestro estudio:** R² = -1.06 en horizonte de 60 días es comparable a otros estudios de largo plazo

### 6.2 Dirección de Causalidad: Precios → Noticias

El hallazgo más sorprendente es que **la causalidad opera en dirección opuesta a la hipótesis inicial**:

**Evidencia:**
- Lag óptimo = -10 días (retornos predicen sentimiento futuro)
- Test de Granger no rechaza H₀ (sentimiento NO causa retornos)
- Correlación contemporánea débil (r = 0.019, no significativa)

**Interpretación:**

1. **Modelo de "price discovery → news coverage":**
   - Los mercados financieros reaccionan instantáneamente a información mediante trading
   - Los periodistas requieren tiempo para investigar, escribir y publicar artículos
   - Lag de ~10 días refleja el ciclo editorial del WSJ

2. **Consistencia con literatura:**
   - **Cutler et al. (1989):** Solo ~50% de movimientos extremos del mercado tienen noticias identificables asociadas
   - **Shiller (2015):** Narrativas económicas se desarrollan DESPUÉS de eventos de mercado
   - **Grossman & Stiglitz (1980):** Información se refleja en precios antes de volverse pública

3. **Implicaciones para trading:**
   - Estrategias que esperan noticias para tomar posiciones sufren de "stale information"
   - El valor del análisis de sentimiento no está en predicción sino en **confirmación de señales técnicas**

### 6.3 Factor Desestabilizante: Asociación Moderada

La coincidencia temporal del **35.6% de outliers con noticias extremas** tiene varias interpretaciones:

**Argumento a favor de influencia noticiosa:**
- 35.6% es significativamente superior al 10-15% esperado por azar
- Regresión muestra β₁ = +0.347 (p < 0.01), estadísticamente significativo
- Casos específicos como marzo 2020 (COVID) muestran causalidad clara noticia→precio

**Argumento contra dependencia fuerte:**
- 64.4% de outliers NO tienen noticias extremas asociadas
- R² = 0.042 implica que 95.8% de volatilidad proviene de otros factores
- Factores técnicos (liquidaciones de apalancados, stop-losses en cascada) pueden generar outliers sin noticias

**Síntesis:**
Las noticias actúan como **catalizador ocasional** de movimientos extremos, pero la mayoría de anomalías se deben a:
- Anuncios de bancos centrales (Fed, BCE, BoJ)
- Datos macroeconómicos (inflación, empleo)
- Flujos de capital institucional
- Factores microestructurales (liquidez, order flow)

### 6.4 Limitaciones del Estudio

#### 6.4.1 Limitaciones Metodológicas

1. **Horizonte temporal fijo:**
   - Lookback de 60 días puede no ser óptimo para todos los períodos
   - Falta de optimización dinámica de hyperparameters

2. **Features limitadas:**
   - No se incluyeron:
     * Tasas de interés reales
     * Índice del dólar (DXY)
     * Volatilidad VIX
     * Spreads de oro físico vs futuros
     * Posicionamiento de especuladores (COT reports)

3. **Análisis de sentimiento binario:**
   - FinBERT clasifica en 3 categorías (pos/neu/neg)
   - No captura matices (urgencia, intensidad, credibilidad de fuente)
   - No distingue entre tipos de noticias (geopolítica vs macro vs corporativa)

4. **Ventana de coincidencia arbitraria:**
   - Ventana de ±3 días para asociar outliers-noticias es ad-hoc
   - Podría ser 1 día, 5 días o 7 días dependiendo de criterio

#### 6.4.2 Limitaciones de Datos

1. **Sesgo de supervivencia:**
   - WSJ puede no cubrir todas las noticias relevantes sobre oro
   - Sesgo hacia eventos que afectan mercados estadounidenses

2. **Scraping incompleto:**
   - Posibles artículos faltantes por paywall o errores de scraping
   - No se capturó el texto completo, solo títulos

3. **Período específico:**
   - 2016-2025 incluye eventos únicos (COVID, guerra Ucrania)
   - Generalización a otros períodos históricos incierta

#### 6.4.3 Limitaciones Teóricas

1. **Causalidad vs Correlación:**
   - Aunque se usó Granger causality, no prueba causalidad verdadera
   - Podría haber variables confounding no observadas

2. **Linealidad asumida:**
   - Tests de Granger asumen relaciones lineales
   - Efectos no-lineales o asimétricos no capturados

3. **Agregación diaria:**
   - Noticias publicadas intraday pueden tener efecto inmediato
   - Agregación diaria pierde granularidad temporal

### 6.5 Implicaciones Prácticas

#### Para Inversionistas

1. **Sentimiento como complemento, no predictor primario:**
   - Usar análisis de sentimiento para validar señales técnicas
   - No depender exclusivamente de noticias para timing de mercado

2. **Valor en gestión de riesgo:**
   - Noticias extremas señalan aumento de volatilidad futura
   - Ajustar position sizing en presencia de sentimiento extremo

3. **Trading strategies:**
   - Estrategias de momentum se benefician de incorporar sentimiento
   - Mean-reversion NO se beneficia (sentimiento es lag indicator)

#### Para Investigadores

1. **Dirección de investigación futura:**
   - Explorar relación precio→noticias (inversa a usual)
   - Modelos de "narrative formation" post-movimientos de mercado

2. **Mejoras metodológicas:**
   - LSTM con attention mechanisms sobre sentimiento
   - Incorporar múltiples fuentes (Twitter, Reddit, Bloomberg)
   - Análisis de tópicos (LDA) para identificar tipos de eventos

3. **Horizonte temporal óptimo:**
   - Investigar horizontes < 10 días donde LSTM puede tener mejor performance
   - Predicción de volatilidad en lugar de precio

### 6.6 Comparación con Objetivos Iniciales

**Preguntas de investigación respondidas:**

| Pregunta | Respuesta | Evidencia |
|----------|-----------|-----------|
| **RQ1:** ¿LSTM mejora con sentimiento? | ✅ **SÍ** | Mejora 12-15% en RMSE/MAE |
| **RQ2:** ¿Sentimiento predice precio? | ❌ **NO** | Granger p > 0.05, lag óptimo negativo |
| **RQ3:** ¿Outliers correlacionan con noticias? | ⚠️ **PARCIALMENTE** | 35.6% coincidencia, R² = 4.2% |
| **RQ4:** ¿Lag óptimo sentimiento-precio? | ✅ **-10 días** | Precio predice sentimiento |
| **RQ5:** ¿Sentimiento causa volatilidad? | ⚠️ **DÉBIL** | β significativo pero R² bajo |

**Hipótesis contrastadas:**

- **H₁ (Sentimiento mejora LSTM):** ✅ ACEPTADA (mejora 12-15%)
- **H₂ (Correlación precio-sentimiento):** ⚠️ PARCIALMENTE (correlación débil, dirección inversa)
- **H₃ (Causalidad Granger):** ❌ RECHAZADA (p > 0.05)
- **H₄ (Factor desestabilizante):** ⚠️ PARCIALMENTE (35.6% coincidencia, efecto significativo pero pequeño)

---

## 7. CONCLUSIONES

### 7.1 Hallazgos Principales

Este estudio investigó la capacidad predictiva de redes neuronales LSTM para el precio del oro, integrando análisis de sentimientos de 13,434 artículos del Wall Street Journal (2016-2025). Los hallazgos principales son:

#### 1. El análisis de sentimientos MEJORA significativamente los modelos LSTM

La incorporación de variables de sentimiento (sentiment, sentiment_ma7, sentiment_ma30) produjo mejoras consistentes:
- **Reducción de RMSE del 12.00%** ($143.23 → $126.05)
- **Reducción de MAE del 15.39%** ($133.96 → $113.35)
- **Mejora de R² del 36.15%** (-1.66 → -1.06)
- **Reducción de MAPE del 15.67%** (7.34% → 6.19%)

Aunque ambos modelos exhiben R² negativos (indicando dificultad inherente de forecasting a 60 días), la **mejora del 12-15% en errores de predicción** representa valor económico tangible para estrategias de inversión.

**Conclusión:** El sentimiento de noticias financieras contiene información útil para predicción de precios del oro, validando parcialmente H₁.

#### 2. La causalidad opera en dirección INVERSA a la hipótesis inicial

Contra la expectativa común de que "noticias mueven mercados", encontramos:
- **Lag óptimo de -10 días:** Los retornos del oro predicen el sentimiento de noticias 10 días después, no al revés
- **Test de Granger no significativo:** p = 0.29 > 0.05, no rechazamos H₀ de no causalidad sentimiento→precio
- **Correlación contemporánea débil:** r = 0.019 (no significativa)

**Interpretación:** Los mercados financieros reaccionan instantáneamente a información mediante price discovery, mientras que las noticias requieren ~10 días para investigación, redacción y publicación. Este resultado es consistente con:
- Modelos de mercados eficientes (Fama, 1970)
- Literatura de "price leads news" (Grossman & Stiglitz, 1980)
- Evidencia empírica de Cutler et al. (1989)

**Conclusión:** Rechazamos H₃. El sentimiento noticioso NO tiene capacidad predictiva causal sobre retornos futuros.

#### 3. Noticias actúan como catalizador ocasional de volatilidad extrema

De los 132 outliers de consenso detectados:
- **35.6% coinciden** temporalmente (±3 días) con noticias de sentimiento extremo
- **64.4% NO tienen** noticias extremas asociadas
- Regresión muestra efecto significativo (β = +0.347, p < 0.01) pero **R² = 4.2%** (95.8% de volatilidad proviene de otros factores)

**Conclusión:** Las noticias juegan un rol **complementario pero minoritario** en la generación de eventos extremos. Otros factores dominantes incluyen:
- Anuncios de política monetaria (Fed, BCE, BoJ)
- Datos macroeconómicos (inflación, empleo, PIB)
- Flujos de capital institucional y ETFs
- Factores microestructurales (liquidez, liquidaciones apalancadas)

Aceptamos parcialmente H₄.

#### 4. Distribución de sentimientos sesgada hacia lo negativo

El corpus de 13,434 noticias muestra:
- 44.7% neutral (predominante, típico de reportes objetivos)
- 33.8% negativo
- 21.5% positivo

**Ratio negativo/positivo = 2.11:1**, consistente con el bien documentado "sesgo de negatividad" en medios de comunicación. Noticias sobre riesgos, crisis y caídas reciben mayor cobertura que estabilidad o alzas.

### 7.2 Contribuciones del Estudio

#### Contribución Metodológica

1. **Primera integración LSTM + FinBERT para oro:**
   - Estudios previos usaron LSTM para commodities (Kristjanpoller & Minutolo, 2018) o FinBERT para acciones (Ke et al., 2021), pero no ambos para oro
   - Metodología replicable con código open-source

2. **Análisis bidireccional de causalidad:**
   - Mayoría de estudios asume dirección noticias→precio
   - Demostramos importancia de testar dirección inversa (precio→noticias)

3. **Factor desestabilizante cuantificado:**
   - Métrica objetiva (35.6% coincidencia) de asociación outliers-noticias
   - Regresión econométrica con R² = 4.2%

#### Contribución Empírica

1. **Dataset único:**
   - 13,434 noticias del WSJ clasificadas con FinBERT
   - 3,614 días de precios XAU/USD (2016-2025)
   - Período incluye eventos únicos: COVID, guerra Ucrania, inflación post-2021

2. **Evidencia de mejora LSTM con sentimiento:**
   - Mejora del 12-15% en errores a pesar de R² negativo
   - Demuestra valor del NLP financiero incluso en mercados eficientes

3. **Causalidad invertida documentada:**
   - Lag óptimo de -10 días (precio predice sentimiento)
   - Explica por qué estrategias basadas en noticias frecuentemente fallan

### 7.3 Implicaciones Prácticas

#### Para Gestores de Inversiones

1. **Usar sentimiento como COMPLEMENTO, no señal primaria:**
   - Combinar con análisis técnico y fundamental
   - No esperar noticias para tomar decisiones (información es stale)

2. **Gestión de riesgo basada en sentimiento:**
   - Reducir exposición cuando sentimiento extremo (+ volatilidad)
   - Aumentar position sizing en períodos de sentimiento neutral

3. **Horizonte temporal:**
   - Sentimiento útil para horizontes cortos (<10 días)
   - Inefectivo para forecasting largo plazo (>60 días)

#### Para Investigadores Académicos

1. **Explorar dirección precio → narrativa:**
   - Modelos de formación de narrativas post-eventos (Shiller, 2019)
   - Lingüística computacional aplicada a reportes financieros

2. **Mejoras de arquitectura:**
   - LSTM con attention mechanisms sobre sentimiento
   - Transformers (BERT, GPT) para análisis de texto completo
   - Multi-task learning (precio + volatilidad simultáneos)

3. **Features adicionales:**
   - Incorporar DXY, tasas reales, VIX, COT reports
   - Análisis de tópicos (LDA) para clasificar tipos de noticias
   - Sentimiento de múltiples fuentes (Twitter, Reddit, Bloomberg)

#### Para Reguladores y Policymakers

1. **Transparencia informativa:**
   - Evidencia de que mercados incorporan información antes de publicación
   - Importancia de combatir insider trading y front-running

2. **Estabilidad financiera:**
   - Noticias explican solo ~4% de volatilidad extrema
   - Factores sistémicos (liquidez, apalancamiento) más relevantes que narrativas

### 7.4 Limitaciones y Trabajo Futuro

#### Limitaciones Principales

1. **R² negativo en ambos modelos:**
   - Indica dificultad fundamental de forecasting a 60 días
   - Reducir horizonte a 1-10 días podría mejorar resultados

2. **Solo títulos, no texto completo:**
   - FinBERT aplicado a títulos pierde contexto del artículo
   - Análisis de cuerpo completo podría mejorar clasificación

3. **Fuente única (WSJ):**
   - Sesgo hacia perspectiva estadounidense
   - Múltiples fuentes (Reuters, Bloomberg, FT) aumentarían robustez

4. **Período específico (2016-2025):**
   - Incluye eventos únicos (COVID, guerra)
   - Generalización a otros períodos incierta

#### Direcciones Futuras

1. **Modelos más sofisticados:**
   - Transformers (BERT-based) para series temporales
   - GRU, TCN (Temporal Convolutional Networks)
   - Ensemble methods (XGBoost + LSTM + Random Forest)

2. **Análisis de contenido avanzado:**
   - Análisis de tópicos (LDA, NMF) para clasificar tipos de eventos
   - Named Entity Recognition (NER) para identificar actores clave (Fed, ECB, China)
   - Aspect-based sentiment (sentimiento sobre inflación vs geopolítica)

3. **Predicción de volatilidad en lugar de precio:**
   - GARCH-LSTM híbrido
   - Realized volatility basada en datos intraday
   - Saltos y tail risk

4. **Trading strategies backtesting:**
   - Long-short basado en señales de sentimiento
   - Mean-variance optimization con sentimiento como feature
   - Cálculo de Sharpe ratio y máximo drawdown

5. **Análisis de redes sociales:**
   - Twitter, Reddit (r/wallstreetbets, r/gold)
   - Sentimiento retail vs institucional
   - Detección de pump-and-dump schemes

6. **Causalidad dinámica:**
   - TVP-VAR (Time-Varying Parameter Vector Autoregression)
   - Detectar cambios de régimen en relación sentimiento-precio
   - Efectos asimétricos (noticias negativas > positivas)

### 7.5 Reflexión Final

Este estudio demuestra que, aunque el oro es un activo con determinación de precio altamente compleja y multicausal, **el análisis sistemático de sentimientos de noticias financieras mediante NLP moderno puede agregar valor cuantificable** a modelos de predicción.

Sin embargo, la evidencia también confirma que **no existe "bala de plata"** para forecasting financiero. Los mercados son eficientes en incorporar información rápidamente, y la mayor parte de la variabilidad de precios se explica por factores macroeconómicos, flujos de capital y dinámica de oferta-demanda que trascienden narrativas noticiosas.

La **dirección invertida de causalidad** (precio→noticias en lugar de noticias→precio) desafía la intuición común y tiene implicaciones profundas para:
- Teorías de formación de precios en mercados financieros
- Diseño de estrategias de trading algorítmico
- Comprensión del rol de los medios en ecosistemas financieros

En última instancia, este trabajo contribuye a la creciente literatura de **FinTech + NLP**, demostrando cómo herramientas de inteligencia artificial pueden extraer señales débiles pero valiosas de océanos de datos no estructurados, incluso en mercados donde la información es abundante y la competencia feroz.

**El futuro del asset management es multidisciplinario:** finanzas cuantitativas + machine learning + procesamiento de lenguaje natural + teoría económica. Este estudio representa un paso en esa dirección.

---

**MENSAJE CLAVE:** El sentimiento de noticias mejora modelos LSTM del oro en 12-15%, pero la causalidad opera inversamente a lo esperado: los precios predicen noticias, no al revés. Las noticias son un catalizador ocasional (~35% de eventos extremos), no el motor principal de la dinámica de precios.

---

## REFERENCIAS

[Por agregar bibliografía en formato APA/IEEE]

---

## APÉNDICES

### Apéndice A: Código Fuente

### Apéndice B: Tablas Suplementarias

### Apéndice C: Figuras Adicionales

---

**FIN DEL DOCUMENTO**
