# 🔬 Diagnóstico: Problema en la Extracción de Noticias WSJ

**Fecha:** 2 de diciembre de 2025  
**Analista:** Sistema de análisis automatizado  
**Archivos analizados:** `hipervinculos_wsj.csv`, `articulos_filtrados_ordenados.csv`

---

## 📋 Resumen Ejecutivo

**HALLAZGO PRINCIPAL:** El script de web scraping del Wall Street Journal cambió su 
método de extracción entre agosto 2020 y enero 2021, causando una caída del **94%** 
en el volumen de artículos capturados.

### ⚠️ Severidad del Problema

- **Impacto:** CRÍTICO
- **Período afectado:** Agosto 2020 - Presente (2025)
- **Datos perdidos:** ~150,000 artículos estimados
- **Sesgo resultante:** 95.8% del corpus final proviene de 2016-2020

---

## 🔍 Análisis Detallado

### 1. Evidencia del Cambio en el Método

#### **Período Pre-Cambio (2016 - Julio 2020)**

```
Método: Extracción selectiva de artículos
Precisión: 99% artículos reales
Patrón: Solo URLs con /articles/...-[números]

Volumen mensual promedio: 2,000 artículos/mes
Total extraído: ~162,000 artículos
```

#### **Transición (Agosto 2020 - Diciembre 2020)**

```
Evento: Cambio en el script de scraping
Caída mensual: De 1,718 (julio) → 454 (octubre)
Precisión degradada: 78% artículos reales
```

#### **Período Post-Cambio (2021 - 2025)**

```
Método: Extracción indiscriminada de todos los hipervínculos
Precisión: 0.2% - 11% artículos reales
Contaminación: 89-99% URLs de navegación/menús

Volumen mensual promedio: 180 artículos/mes
Total extraído: ~11,000 artículos
```

---

## 📊 Datos Cuantitativos

### Composición del Dataset Original

| Archivo | Registros | Artículos Reales | URLs Navegación | % Precisión |
|---------|-----------|------------------|-----------------|-------------|
| `hipervinculos_wsj.csv` | 294,610 | 188,469 | 106,141 | 63.97% |

### Distribución Temporal de Artículos Reales

| Año  | Total Registros | Artículos | % Artículos | Estado |
|------|----------------|-----------|-------------|---------|
| 2016 | 58,037 | 57,365 | 98.84% | ✅ Excelente |
| 2017 | 45,613 | 45,308 | 99.33% | ✅ Excelente |
| 2018 | 36,245 | 35,925 | 99.12% | ✅ Excelente |
| 2019 | 23,420 | 23,142 | 98.81% | ✅ Excelente |
| 2020 | 20,437 | 15,972 | 78.15% | ⚠️ Degradado |
| 2021 | 20,109 | 2,139 | 10.64% | ❌ Malo |
| 2022 | 19,303 | 6,424 | 33.28% | ❌ Malo |
| 2023 | 18,926 | 2,099 | 11.09% | ❌ Malo |
| 2024 | 24,736 | 48 | 0.19% | 🔴 Crítico |
| 2025 | 27,784 | 47 | 0.17% | 🔴 Crítico |

### Evolución Mensual del Punto de Quiebre (2020)

```
Mes       Artículos    Cambio
-------------------------------
Enero     2,024       (baseline)
Febrero   1,821       -10%
Marzo     1,885       +4%
Abril     1,851       -2%
Mayo      1,976       +7%
Junio     2,047       +4%
Julio     1,718       -16%
Agosto    1,150       -33%  ⚠️ INICIO DEL PROBLEMA
Sept      751         -35%
Octubre   454         -40%
Nov       125         -72%
Diciembre 170         -26%
```

---

## 🎯 Causa Raíz

### Hipótesis Principal: Cambio en la Lógica de Scraping

**Comportamiento Antiguo (2016-2019):**
```python
# Pseudocódigo del método original
for page in wsj_pages:
    articles = page.find_all('article')  # Solo artículos
    for article in articles:
        url = article.find('a')['href']
        if matches_pattern(url, r'/articles/.*-\d+$'):
            save_to_csv(url)
```

**Comportamiento Nuevo (2020+):**
```python
# Pseudocódigo del método defectuoso
for page in wsj_pages:
    all_links = page.find_all('a')  # TODOS los enlaces
    for link in all_links:
        url = link['href']
        save_to_csv(url)  # No filtra por tipo
```

### Consecuencias:

1. **Contaminación masiva:** 36% del dataset son URLs inútiles
   - Menús de navegación (`/world`, `/business`, `/tech`)
   - Enlaces a secciones (`/news/archive/`)
   - Videos y multimedia (`/video/series/`)
   - Páginas de login/logout

2. **Pérdida de cobertura:** En lugar de capturar más artículos, 
   captura menos porque el script se distrae con navegación

3. **Inconsistencia temporal:** Dataset no comparable entre períodos

---

## ✅ Validación del Post-Procesamiento

### Archivo: `filtrado_noticias.py`

**Estado:** ✅ FUNCIONA CORRECTAMENTE

```python
# Filtro aplicado
filtro = df['url'].str.contains(r'/articles/.*-\d+$', regex=True)
```

**Resultados:**
- ✅ Elimina 106,141 URLs inútiles (36% del total)
- ✅ Retiene 188,469 artículos reales (64%)
- ✅ Patrón regex es correcto y preciso
- ✅ Todos los títulos con "gold" pasan el filtro

**Conclusión:** El problema NO está en el post-procesamiento, 
sino en la **fase de extracción original**.

---

## 🛠️ Soluciones Propuestas

### Opción 1: Corto Plazo (IMPLEMENTADA)

**Estado:** ✅ Completado

- [x] Documentar limitación en metodología
- [x] Actualizar informe científico con sección de limitaciones
- [x] Análisis ponderado por densidad temporal
- [x] Conclusiones basadas principalmente en 2016-2020

**Ventajas:**
- No requiere trabajo adicional
- Resultados actuales son válidos con caveat documentado

**Desventajas:**
- Dataset sigue incompleto para años recientes
- Análisis sesgado hacia período pre-2021

---

### Opción 2: Largo Plazo (RECOMENDADA)

**Estado:** ⏳ Pendiente

1. **Identificar script original de scraping**
   - Buscar en repositorio/historial
   - Contactar con quien desarrolló el scraping original

2. **Corregir método de extracción**
   ```python
   # Implementación correcta
   def scrape_wsj_articles(date):
       page = fetch_wsj_archive(date)
       articles = page.select('article.WSJTheme--story')  # Solo artículos
       for article in articles:
           url = article.select_one('a')['href']
           if '/articles/' in url and url.endswith(tuple('0123456789')):
               title = article.select_one('h3').text
               save_article(title, url, date)
   ```

3. **Re-ejecutar scraping para 2020-2025**
   - Validar que capture >95% artículos reales
   - Comparar con muestra existente para verificar consistencia

4. **Integrar nuevos datos**
   - Merge con dataset existente
   - Verificar no hay duplicados
   - Re-ejecutar análisis completo

**Esfuerzo estimado:** 40-80 horas
- 8h: Análisis de script original
- 16h: Corrección y testing
- 24h: Re-scraping (depende de velocidad)
- 8h: Integración y validación
- 8h: Re-ejecución de análisis

**Ventajas:**
- Dataset completo y balanceado
- Análisis más robusto para todo el período
- Elimina sesgo temporal

**Desventajas:**
- Requiere tiempo significativo
- Puede enfrentar restricciones de acceso WSJ
- Riesgo de rate limiting/bloqueo

---

### Opción 3: Alternativa (EXPLORATORIA)

**Estado:** 💡 Propuesta

**Complementar con fuentes adicionales:**

1. **APIs de noticias financieras:**
   - NewsAPI.org (40,000 artículos/mes gratis)
   - GDELT Project (archivo global de noticias)
   - Bloomberg API (requiere suscripción)
   - Alpha Vantage News (gratis, limitado)

2. **Implementación:**
   ```python
   # Ejemplo con NewsAPI
   from newsapi import NewsApiClient
   
   newsapi = NewsApiClient(api_key='YOUR_KEY')
   articles = newsapi.get_everything(
       q='gold OR "gold price" OR bullion',
       sources='the-wall-street-journal',
       from_param='2021-01-01',
       to='2025-12-31',
       language='en'
   )
   ```

3. **Validación cruzada:**
   - Comparar artículos de API vs WSJ scrapeado
   - Verificar overlap para período 2016-2020
   - Validar consistencia de análisis de sentimientos

**Ventajas:**
- Datos estructurados y limpios
- Cobertura temporal completa
- Mayor diversidad de fuentes

**Desventajas:**
- Puede no incluir todos los artículos WSJ
- Diferentes sesgos de cobertura
- Costos potenciales de API

---

## 📊 Impacto en Resultados del Estudio

### Análisis Afectados:

1. **Análisis de Sentimientos (Moderado)**
   - ⚠️ Sentimientos sesgados hacia 2016-2020
   - ⚠️ Menor muestra para validar tendencias recientes
   - ✅ Resultados válidos para período con datos

2. **Granger Causality (Alto)**
   - ❌ Desbalance temporal puede sesgar tests
   - ⚠️ Lag optimization menos confiable
   - ⚠️ P-values pueden ser artificialmente altos

3. **Modelo LSTM (Moderado)**
   - ⚠️ Entrenamiento sesgado hacia período antiguo
   - ⚠️ Predicciones para 2024-2025 menos confiables
   - ✅ Arquitectura y metodología siguen siendo válidas

4. **Detección de Outliers (Bajo)**
   - ✅ Precios del oro no afectados
   - ⚠️ Asociación outliers-noticias menos representativa
   - ⚠️ Ventana ±3 días menos efectiva para años recientes

---

## 🎓 Lecciones Aprendidas

### Para Futuros Proyectos de Web Scraping:

1. **Validación continua:**
   - Implementar checks de volumen mensual
   - Alertas automáticas cuando caída >20%
   - Logs detallados de tipos de URLs capturadas

2. **Testing robusto:**
   - Unit tests para patrones de extracción
   - Validación de estructura HTML
   - Muestras aleatorias periódicas

3. **Documentación:**
   - Registrar cambios en código de scraping
   - Versionar scripts con fechas
   - Mantener historial de modificaciones

4. **Backup y auditoría:**
   - Guardar snapshots mensuales
   - Comparaciones período a período
   - Detección temprana de anomalías

---

## 📞 Contacto y Seguimiento

**Responsable:** [Asignar responsable]  
**Prioridad:** Alta  
**Fecha límite:** [Definir según opción elegida]

**Próximos pasos:**
1. [ ] Decidir qué opción implementar (1, 2, o 3)
2. [ ] Asignar recursos y tiempo
3. [ ] Iniciar implementación
4. [ ] Actualizar resultados según nuevos datos

---

## 📚 Referencias

- **Notebook de análisis:** `pruebas_observaciones/Analisis_Volumen_Noticias.ipynb`
- **Limitaciones documentadas:** `pruebas_observaciones/LIMITACION_DATOS_NOTICIAS.md`
- **Dataset original:** `hipervinculos_wsj.csv` (294,610 registros)
- **Dataset procesado:** `articulos_filtrados_ordenados.csv` (188,469 artículos)
- **Dataset final:** `noticias_oro_limpias.csv` (13,434 noticias)

---

**Última actualización:** 2 de diciembre de 2025
