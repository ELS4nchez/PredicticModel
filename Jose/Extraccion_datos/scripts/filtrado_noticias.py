import pandas as pd

# --- CONFIGURACIÓN ---
archivo_entrada = '../data/hipervinculos_wsj.csv'
archivo_salida = '../data/articulos_filtrados_ordenados.csv'
# IMPORTANTE: Cambia esto por el nombre exacto que tiene la 3ra columna en tu CSV
nombre_columna_fecha = 'fecha' 
# ---------------------

# 1. Cargar el archivo
df = pd.read_csv(archivo_entrada)

print(f"Total de registros cargados: {len(df)}")

# 2. Filtrar las filas (primero filtramos para trabajar con menos datos)
# Buscamos que 'url' contenga '/articles/' Y que termine con guion seguido de números
# Patrón: /articles/cualquier-cosa-NUMEROS
filtro = df['url'].str.contains(r'/articles/.*-\d+$', case=False, na=False, regex=True)
df_filtrado = df[filtro].copy() # Usamos .copy() para evitar advertencias de pandas

print(f"Registros después de filtrar por patrón /articles/...-NUMEROS: {len(df_filtrado)}")

# 3. Eliminar duplicados basándonos en la URL (mantener el primero)
df_sin_duplicados = df_filtrado.drop_duplicates(subset=['url'], keep='first')

print(f"Registros después de eliminar duplicados de URL: {len(df_sin_duplicados)}")

# 4. Convertir la columna de fecha a objetos de tiempo reales
# 'errors="coerce"' convierte a NaT (Not a Time) si hay fechas inválidas para que no falle el script
df_sin_duplicados[nombre_columna_fecha] = pd.to_datetime(df_sin_duplicados[nombre_columna_fecha], errors='coerce')

# 5. Eliminar filas con fechas inválidas (NaT)
df_con_fechas_validas = df_sin_duplicados.dropna(subset=[nombre_columna_fecha])

print(f"Registros después de eliminar fechas inválidas: {len(df_con_fechas_validas)}")

# 6. Ordenar por la fecha
# ascending=True  -> Del más antiguo al más reciente
# ascending=False -> Del más reciente al más antiguo
df_ordenado = df_con_fechas_validas.sort_values(by=nombre_columna_fecha, ascending=True)

# 7. Guardar el resultado
# Si quieres guardar la fecha en un formato específico (ej: YYYY-MM-DD), pandas lo hace automático,
# pero el objeto datetime se guarda bien.
df_ordenado.to_csv(archivo_salida, index=False)

print(f"\nProceso finalizado.")
print(f"Se encontraron {len(df_ordenado)} artículos válidos.")
print(f"Archivo guardado en: {archivo_salida}")
print(f"\nLas primeras 5 filas ordenadas son:")
print(df_ordenado.head())