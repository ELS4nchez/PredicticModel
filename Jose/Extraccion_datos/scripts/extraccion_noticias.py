#!/usr/bin/env python3
"""
Script para extraer todos los hipervínculos de páginas de WSJ.
Extrae todos los enlaces encontrados en la página sin filtrado.
Usa Selenium para manejar contenido dinámico cargado con JavaScript.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime, timedelta
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def extraer_articulos_wsj(fecha="2016/01/01"):
    """
    Extrae todos los hipervínculos de WSJ para una fecha específica usando Selenium.
    Args:
        fecha: Fecha en formato "YYYY/MM/DD"
    Returns:
        Lista de diccionarios con 'titulo' y 'url' de cada enlace
    """
    url = f"https://www.wsj.com/news/archive/{fecha}"
    # Configurar opciones de Chrome para máximo rendimiento
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')  # Nuevo modo headless más rápido
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-images')  # No cargar imágenes
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Bloquear imágenes
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_experimental_option('prefs', {
        'profile.managed_default_content_settings.images': 2,  # Bloquear imágenes
        'profile.managed_default_content_settings.stylesheets': 2,  # Bloquear CSS
        'profile.managed_default_content_settings.javascript': 1,  # Permitir JS (necesario)
    })
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.page_load_strategy = 'eager'  # No esperar a que todo cargue
    articulos = []
    driver = None
    try:
        print(f"Iniciando navegador Chrome para {fecha}...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"Conectando a: {url}")
        driver.get(url)
        # Esperar solo lo mínimo necesario
        print("Esperando carga...")
        time.sleep(1.5)  # Reducido al mínimo
        # Scroll rápido
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)  # Medio segundo
        # Obtener el HTML completo después de que JavaScript haya cargado
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Buscar todos los enlaces <a> en la página (SIN FILTRADO)
        todos_enlaces = soup.find_all('a', href=True)
        print(f"Total de enlaces encontrados: {len(todos_enlaces)}")
        
        enlaces_unicos = set()
        for enlace in todos_enlaces:
            href = enlace.get('href', '')
            
            # Convertir enlaces relativos a absolutos
            if href.startswith('/'):
                href = 'https://www.wsj.com' + href
            elif not href.startswith('http'):
                continue  # Ignorar enlaces que no son http/https
            
            # Agregar todos los enlaces únicos sin filtrar
            if href not in enlaces_unicos:
                enlaces_unicos.add(href)
                # Obtener el título del enlace
                titulo = enlace.get_text(strip=True)
                # Si no hay texto en el enlace, buscar en elementos padres o hermanos
                if not titulo:
                    parent = enlace.parent
                    if parent:
                        titulo = parent.get_text(strip=True)
                articulos.append({
                    'titulo': titulo if titulo else 'Sin título',
                    'url': href,
                    'fecha': fecha
                })
        print(f"\n✓ Se encontraron {len(articulos)} enlaces únicos para {fecha}\n")
    except Exception as e:
        print(f"✗ Error para {fecha}: {e}")
    finally:
        if driver:
            driver.quit()
    return articulos

def guardar_csv(articulos, nombre_archivo="../data/hipervinculos_wsj.csv"):
    """Guarda todos los hipervínculos en un archivo CSV, agregando si ya existe y evitando duplicados"""
    existing_urls = set()
    file_exists = os.path.exists(nombre_archivo)
    if file_exists:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_urls.add(row['url'])
    
    nuevos_articulos = [art for art in articulos if art['url'] not in existing_urls]
    
    if nuevos_articulos:
        mode = 'a' if file_exists else 'w'
        with open(nombre_archivo, mode, newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['titulo', 'url', 'fecha'])
            if not file_exists:
                writer.writeheader()
            writer.writerows(nuevos_articulos)
        print(f"✓ {len(nuevos_articulos)} hipervínculos nuevos agregados a: {nombre_archivo}")
    else:
        print(f"✓ No hay hipervínculos nuevos para agregar a: {nombre_archivo}")

def obtener_ultima_fecha_csv(nombre_archivo="../data/hipervinculos_wsj.csv"):
    """Obtiene la última fecha registrada en el CSV para reanudar la extracción."""
    if not os.path.exists(nombre_archivo):
        return None
    
    ultima_fecha = None
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or 'fecha' not in reader.fieldnames:
                return None
            
            for row in reader:
                fecha_str = row.get('fecha')
                if fecha_str:
                    try:
                        # Intentar parsear la fecha
                        fecha = datetime.strptime(fecha_str, "%Y/%m/%d")
                        if ultima_fecha is None or fecha > ultima_fecha:
                            ultima_fecha = fecha
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Advertencia al leer última fecha: {e}")
        return None
        
    return ultima_fecha

def main():
    """Función principal con procesamiento paralelo continuo sin esperas"""
    print("=" * 70)
    print("EXTRACTOR DE HIPERVÍNCULOS DE WSJ (MODO RÁPIDO)")
    print("=" * 70)

    # Definir rango de fechas: desde enero 2023 hasta octubre 2025
    start_date = datetime(2018, 6, 18)
    end_date = datetime(2025, 10, 31)
    
    # Verificar si hay datos previos para reanudar
    ultima_fecha = obtener_ultima_fecha_csv()
    if ultima_fecha:
        print(f"✓ Se encontró historial hasta: {ultima_fecha.strftime('%Y/%m/%d')}")
        start_date = ultima_fecha + timedelta(days=1)
        print(f"✓ Reanudando extracción desde: {start_date.strftime('%Y/%m/%d')}")
    else:
        print(f"✓ Iniciando extracción desde: {start_date.strftime('%Y/%m/%d')}")

    if start_date > end_date:
        print("! Todas las fechas en el rango ya han sido procesadas.")
        return
    
    # Generar lista de fechas
    fechas = []
    current_date = start_date
    while current_date <= end_date:
        fechas.append(current_date.strftime("%Y/%m/%d"))
        current_date += timedelta(days=1)
    
    print(f"\nProcesando {len(fechas)} fechas con 3 navegadores simultáneos (sin esperas)...\n")
    
    # Pool global con 3 workers que trabajan continuamente
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Enviar todas las tareas (el pool maneja automáticamente mantener 3 activos)
        future_to_fecha = {executor.submit(extraer_articulos_wsj, fecha): fecha for fecha in fechas}
        
        # Procesar resultados conforme terminan (sin bloquear)
        for future in as_completed(future_to_fecha):
            fecha = future_to_fecha[future]
            try:
                articulos = future.result(timeout=30)
                if articulos:
                    print(f"✓ {fecha}: {len(articulos)} enlaces - Guardando...")
                    guardar_csv(articulos)
                else:
                    print(f"✗ {fecha}: Sin enlaces")
            except Exception as e:
                print(f"✗ {fecha}: Error - {e}")
    
    print("\n" + "=" * 70)
    print("PROCESO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()