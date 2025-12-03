#!/usr/bin/env python3
"""
Script de Verificación de Instalación
Proyecto: Análisis Oro & Sentimientos WSJ

Ejecutar: python verificar_instalacion.py
"""

import sys
from pathlib import Path

def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_python_version():
    """Verifica la versión de Python."""
    print_header("1️⃣  Verificando Python")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"✅ Python {version_str}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ ERROR: Se requiere Python 3.8 o superior")
        return False
    return True

def check_libraries():
    """Verifica que todas las librerías estén instaladas."""
    print_header("2️⃣  Verificando Librerías")
    
    libraries = {
        'pandas': 'Manipulación de datos',
        'numpy': 'Cálculos numéricos',
        'matplotlib': 'Visualización',
        'seaborn': 'Visualización estadística',
        'plotly': 'Gráficos interactivos',
        'scipy': 'Análisis científico',
        'sklearn': 'Machine Learning',
        'statsmodels': 'Estadística',
        'tensorflow': 'Deep Learning (LSTM)',
        'torch': 'PyTorch (Transformers)',
        'transformers': 'Modelos NLP',
        'nltk': 'Procesamiento de lenguaje',
        'tqdm': 'Barras de progreso',
    }
    
    all_ok = True
    for lib, description in libraries.items():
        try:
            module = __import__(lib)
            version = getattr(module, '__version__', 'N/A')
            print(f"✅ {lib:15s} {version:10s} - {description}")
        except ImportError:
            print(f"❌ {lib:15s} {'NO INSTALADO':10s} - {description}")
            all_ok = False
    
    return all_ok

def check_nltk_data():
    """Verifica que los recursos NLTK estén descargados."""
    print_header("3️⃣  Verificando Recursos NLTK")
    
    try:
        import nltk
        resources = ['punkt', 'stopwords', 'punkt_tab']
        all_ok = True
        
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}' if 'punkt' in resource else f'corpora/{resource}')
                print(f"✅ {resource}")
            except LookupError:
                print(f"❌ {resource} - NO DESCARGADO")
                all_ok = False
        
        if not all_ok:
            print("\n⚠️  Descarga recursos con:")
            print("   python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')\"")
        
        return all_ok
    except ImportError:
        print("❌ NLTK no está instalado")
        return False

def check_data_files():
    """Verifica que los archivos de datos existan."""
    print_header("4️⃣  Verificando Archivos de Datos")
    
    base_dir = Path(__file__).parent
    
    files_to_check = {
        'Precios del oro': base_dir / 'datos_horas' / 'XAU_USD_2016-2025_01-12_1h_bars.csv',
        'Noticias filtradas': base_dir / 'data' / 'processed' / 'articulos_filtrados_ordenados.csv',
        'Hipervínculos WSJ': base_dir / 'data' / 'raw' / 'hipervinculos_wsj.csv',
    }
    
    all_ok = True
    for name, path in files_to_check.items():
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"✅ {name:25s} ({size_mb:.1f} MB)")
        else:
            print(f"❌ {name:25s} - NO ENCONTRADO")
            print(f"   Ruta esperada: {path}")
            all_ok = False
    
    return all_ok

def check_directories():
    """Verifica que existan los directorios necesarios."""
    print_header("5️⃣  Verificando Estructura de Directorios")
    
    base_dir = Path(__file__).parent
    
    directories = [
        'data/raw',
        'data/processed',
        'datos_horas',
        'unificacion/notebooks',
        'unificacion/datos_procesados',
        'unificacion/figuras',
        'unificacion/modelos',
        'unificacion/informes',
    ]
    
    all_ok = True
    for dir_path in directories:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - NO EXISTE")
            all_ok = False
    
    return all_ok

def test_gpu():
    """Verifica disponibilidad de GPU (opcional)."""
    print_header("6️⃣  Verificando GPU (Opcional)")
    
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ GPU detectada (TensorFlow): {len(gpus)} dispositivo(s)")
            for gpu in gpus:
                print(f"   - {gpu.name}")
        else:
            print("ℹ️  No hay GPU disponible (CPU será usado - normal para este proyecto)")
        
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU detectada (PyTorch): {torch.cuda.get_device_name(0)}")
        else:
            print("ℹ️  PyTorch usando CPU (configuración recomendada)")
        
        return True
    except Exception as e:
        print(f"⚠️  Error al verificar GPU: {e}")
        return True  # No es crítico

def main():
    """Función principal."""
    print("\n" + "█"*70)
    print("█  VERIFICACIÓN DE INSTALACIÓN - Proyecto Oro & WSJ")
    print("█"*70)
    
    checks = [
        ("Python", check_python_version),
        ("Librerías", check_libraries),
        ("NLTK", check_nltk_data),
        ("Archivos de datos", check_data_files),
        ("Directorios", check_directories),
        ("GPU", test_gpu),
    ]
    
    results = {}
    for name, check_func in checks:
        results[name] = check_func()
    
    # Resumen final
    print_header("📊 RESUMEN FINAL")
    
    all_passed = True
    for name, passed in results.items():
        if name == "GPU":  # GPU es opcional
            continue
        status = "✅ OK" if passed else "❌ ERROR"
        print(f"{status:10s} {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ¡INSTALACIÓN COMPLETA Y CORRECTA!")
        print("\nPróximos pasos:")
        print("  1. Abre Jupyter: jupyter notebook")
        print("  2. Navega a: unificacion/notebooks/")
        print("  3. Ejecuta: 01_Introduccion_y_Carga_de_Datos.ipynb")
    else:
        print("⚠️  HAY PROBLEMAS CON LA INSTALACIÓN")
        print("\nRevisa los errores marcados arriba y:")
        print("  1. Instala librerías faltantes: pip install nombre_libreria")
        print("  2. Descarga recursos NLTK")
        print("  3. Verifica archivos de datos")
        print("\nConsulta INSTALACION.md para más ayuda")
    
    print("="*70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
