# 🚀 Guía de Instalación y Configuración

## Proyecto: Análisis de Precios del Oro y Sentimientos de Noticias WSJ

---

## 📋 Requisitos del Sistema

### Hardware Mínimo
- **RAM**: 8 GB (recomendado: 16 GB)
- **Espacio en disco**: 5 GB libres
- **Procesador**: CPU con soporte para Python 3.8+

### Software
- **Python**: 3.8, 3.9, 3.10 o 3.11
- **pip**: Versión 21.0 o superior
- **Git**: (opcional, para clonar el repositorio)

---

## 🛠️ Instalación Paso a Paso

### Opción 1: Instalación con venv (Recomendado para principiantes)

```bash
# 1. Navegar al directorio del proyecto
cd /ruta/a/TECH

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
# En Linux/Mac:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate

# 4. Actualizar pip
pip install --upgrade pip

# 5. Instalar todas las dependencias
pip install -r requirements.txt

# 6. Instalar PyTorch CPU (si falla en el paso anterior)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 7. Descargar recursos NLTK (obligatorio)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
```

### Opción 2: Instalación con Conda (Recomendado para usuarios avanzados)

```bash
# 1. Crear entorno conda
conda create -n oro_wsj python=3.10 -y

# 2. Activar entorno
conda activate oro_wsj

# 3. Instalar dependencias base con conda (opcional, más rápido)
conda install -c conda-forge pandas numpy matplotlib seaborn scipy scikit-learn jupyter -y

# 4. Instalar el resto con pip
pip install -r requirements.txt

# 5. Descargar recursos NLTK
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
```

---

## ✅ Verificación de la Instalación

Ejecuta este comando para verificar que todas las librerías están correctamente instaladas:

```bash
python -c "import pandas as pd; import numpy as np; import sklearn; import tensorflow as tf; import transformers; import nltk; import plotly; import statsmodels; print('✅ Todas las librerías instaladas correctamente'); print(f'  - pandas: {pd.__version__}'); print(f'  - numpy: {np.__version__}'); print(f'  - tensorflow: {tf.__version__}')"
```

**Salida esperada:**
```
✅ Todas las librerías instaladas correctamente
  - pandas: 2.x.x
  - numpy: 1.x.x
  - tensorflow: 2.x.x
```

---

## 🗂️ Estructura del Proyecto

Después de la instalación, verifica que tienes esta estructura:

```
TECH/
├── requirements.txt              # Dependencias del proyecto
├── INSTALACION.md               # Este archivo
├── filtrado_noticias.py         # Script de filtrado de noticias
├── data/                        # Datos del proyecto
│   ├── raw/                     # Datos crudos
│   │   └── hipervinculos_wsj.csv
│   └── processed/               # Datos procesados
│       └── articulos_filtrados_ordenados.csv
├── datos_horas/                 # Datos de precios horarios
│   └── XAU_USD_2016-2025_01-12_1h_bars.csv
└── unificacion/                 # Análisis unificado
    ├── notebooks/               # Notebooks Jupyter (01-08)
    ├── datos_procesados/        # Resultados intermedios
    ├── figuras/                 # Gráficos generados
    ├── modelos/                 # Modelos LSTM entrenados
    └── informes/                # Reportes finales
```

---

## 📓 Ejecutar los Notebooks

### 1. Iniciar Jupyter Notebook

```bash
# Con el entorno virtual activado:
jupyter notebook
```

Esto abrirá tu navegador en `http://localhost:8888`

### 2. Orden de Ejecución

**⚠️ IMPORTANTE:** Los notebooks deben ejecutarse en orden secuencial:

1. **01_Introduccion_y_Carga_de_Datos.ipynb**
   - Carga datos de precios y noticias
   - Limpieza inicial
   - ⏱️ ~3-5 minutos

2. **02_EDA_Precios_Oro.ipynb**
   - Análisis exploratorio de precios
   - Tendencias y estacionalidad
   - ⏱️ ~2-3 minutos

3. **03_EDA_Noticias_WSJ.ipynb**
   - Análisis de corpus de noticias
   - Frecuencias y patrones
   - ⏱️ ~3-4 minutos

4. **04_Deteccion_Anomalias.ipynb**
   - Detección de outliers en precios
   - Isolation Forest
   - ⏱️ ~2-3 minutos

5. **05_Analisis_Sentimientos_FinBERT.ipynb**
   - Análisis de sentimientos con FinBERT
   - ⚠️ Primera ejecución descarga modelo (~500MB)
   - ⏱️ ~15-30 minutos (primera vez), ~10 min (subsecuentes)

6. **06_Correlacion_y_Causalidad.ipynb**
   - Correlaciones y causalidad de Granger
   - Integración de datos
   - ⏱️ ~3-5 minutos

7. **07_Modelo_LSTM_Integrado.ipynb**
   - Entrenamiento de modelos LSTM
   - ⚠️ Proceso largo
   - ⏱️ ~20-40 minutos

8. **08_Sintesis_y_Resultados.ipynb**
   - Resumen y conclusiones
   - Generación de reportes
   - ⏱️ ~2-3 minutos

**Tiempo total estimado:** 1-2 horas (primera ejecución completa)

---

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'X'"

```bash
# Asegúrate de tener el entorno virtual activado
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Reinstalar el paquete específico
pip install nombre_paquete
```

### Error al instalar PyTorch

```bash
# Instalar manualmente la versión CPU
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Error: "FileNotFoundError" en notebooks

- Verifica que ejecutaste los notebooks anteriores en orden
- Revisa que los archivos de datos están en las rutas correctas
- Ejecuta el notebook 01 primero para generar archivos procesados

### FinBERT tarda mucho en descargar

- Es normal la primera vez (~500MB)
- El modelo se guarda en cache (`~/.cache/huggingface/`)
- Ejecuciones posteriores serán más rápidas

### Memoria insuficiente (RAM)

```python
# En notebooks, reducir batch_size para FinBERT
# Buscar la celda con:
batch_size = 32  # Cambiar a 16 o 8
```

### Errores con NLTK

```bash
# Descargar recursos manualmente
python -m nltk.downloader punkt stopwords punkt_tab
```

---

## 🔄 Actualizar Dependencias

```bash
# Activar entorno
source .venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Actualizar todas las dependencias
pip install --upgrade -r requirements.txt
```

---

## 🗑️ Desinstalación

```bash
# Desactivar entorno virtual
deactivate

# Eliminar entorno virtual
rm -rf .venv

# O con conda:
conda deactivate
conda env remove -n oro_wsj
```

---

## 📞 Soporte

Si encuentras problemas:

1. Verifica que Python >= 3.8
2. Revisa que todas las dependencias están instaladas
3. Asegúrate de ejecutar notebooks en orden
4. Consulta la sección "Solución de Problemas"

---

## 📝 Notas Adicionales

- **GPU no es necesaria** para este proyecto
- Todos los modelos están optimizados para **CPU**
- Los datos procesados se guardan automáticamente
- Puedes re-ejecutar notebooks individuales sin problemas
- Los modelos entrenados se guardan en `unificacion/modelos/`

---

✅ **¡Listo para empezar!** Navega a `unificacion/notebooks/` y abre el notebook 01.
