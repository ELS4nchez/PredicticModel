# Limitación Identificada: Desbalance Temporal en Datos de Noticias


### 4.2.3 Limitaciones de la Fuente de Datos de Noticias

**Desbalance temporal en corpus de noticias:** 

El dataset de noticias del Wall Street Journal presenta una caída abrupta en 
volumen a partir de 2021, probablemente debido a cambios en el proceso de web 
scraping o modificaciones en la estructura del sitio web del WSJ. 

**Distribución temporal:**
- 2016-2020: ~178,000 artículos totales (promedio 35,600/año)
- 2021-2025: ~10,700 artículos totales (promedio 2,140/año)
- Caída de volumen: -94% entre 2020 y 2021

Aunque el porcentaje de noticias relevantes al oro se mantiene consistente 
(4-8% en todos los años), indicando que el filtrado por palabras clave funciona 
correctamente, el volumen absoluto reducido en años recientes puede afectar la 
representatividad del análisis de sentimientos para el período 2021-2025.

**Distribución final del corpus:**
- Total noticias sobre oro: 13,434
- Período 2016-2020: 12,875 noticias (95.8% del total)
- Período 2021-2025: 559 noticias (4.2% del total)

**Impacto en resultados:** 

Los análisis de causalidad y correlación podrían estar sesgados hacia el período 
2016-2020 donde existe mayor densidad de datos. Los resultados de tests de Granger 
Causality y análisis de lag optimization deben interpretarse considerando este 
desbalance temporal. La menor representatividad de datos post-2021 es una 
limitación importante del estudio que debe considerarse al generalizar conclusiones.


---
**Fecha de análisis:** 2 de diciembre de 2025
**Archivo de análisis:** `Analisis_Volumen_Noticias.ipynb`
