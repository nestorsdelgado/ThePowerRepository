"""
01_construir_dataset.py
==============================================================================
De TRES ficheros en bruto a UN único conjunto de datos, ya LEGIBLE.

  Gastos (1 fila = una partida de gasto de un hogar)  --agregar-->  hogar x grupo
  Hogar  (1 fila = un hogar)                           --unir NUMERO-->
  IPC    (1 fila = precio de una CCAA y un grupo)      --unir CCAA+GRUPO-->

Robustez / legibilidad:
  · Detecta solo el separador decimal de cada CSV de entrada (punto o coma).
  · Traduce las variables codificadas del INE a etiquetas legibles usando los
    VALORES OFICIALES de la documentación EPF 2024 (no se inventa nada).
  · Escribe el resultado en CSV y en XLSX generado desde Python (números como
    números: inmune a la configuración regional de Excel).

Estructura esperada (este .py va en la carpeta raíz):
  carpeta_del_proyecto/
  ├── 01_construir_dataset.py
  ├── BRUTOS/    <- EPFgastos_2024.csv, EPFhogar_2024.csv, IPC_2024.csv
  └── FINALES/   <- aquí se guardan los resultados
==============================================================================
"""

from pathlib import Path
import pandas as pd

# --- Rutas -----------------------------------------------------------------
BASE    = Path(__file__).resolve().parent
BRUTOS  = BASE / "BRUTOS"
FINALES = BASE / "FINALES"
FINALES.mkdir(parents=True, exist_ok=True)


# --- Utilidad: detectar el separador decimal de un CSV ---------------------
def detectar_decimal(path, sep, encoding, columna):
    """Mira una columna numérica de muestra y devuelve ',' o '.' según cuál
    se use como separador decimal. Así da igual cómo venga descargado."""
    muestra = pd.read_csv(path, sep=sep, encoding=encoding,
                          usecols=[columna], dtype=str, nrows=500)[columna].dropna()
    prop_coma  = muestra.str.contains(r"\d,\d").mean()    # p.ej. "97,657"
    prop_punto = muestra.str.contains(r"\d\.\d").mean()   # p.ej. "834081.59"
    dec = "," if prop_coma > prop_punto else "."
    print(f"   · decimal detectado en {Path(path).name}: '{dec}'")
    return dec


# --- Utilidad: traducir código -> etiqueta ---------------------------------
def etiquetar(serie, mapping, defecto="No consta"):
    """Convierte una columna de códigos numéricos en etiquetas de texto.
    Los códigos no contemplados o vacíos se marcan como 'No consta'."""
    codigo = pd.to_numeric(serie, errors="coerce").astype("Int64")
    return codigo.map(mapping).astype("object").fillna(defecto)


# --- Diccionarios de etiquetas ---------------------------------------------
# Grupos COICOP 2018 / ECOICOP ver.2
GRUPO_NOMBRE = {
    "01": "Alimentos y bebidas no alcohólicas",
    "02": "Bebidas alcohólicas y tabaco",
    "03": "Vestido y calzado",
    "04": "Vivienda, agua, electricidad, gas y otros combustibles",
    "05": "Muebles, artículos del hogar y mantenimiento del hogar",
    "06": "Sanidad",
    "07": "Transporte",
    "08": "Información y comunicaciones",
    "09": "Actividades recreativas, deporte y cultura",
    "10": "Enseñanza",
    "11": "Restaurantes y servicios de alojamiento",
    "12": "Seguros y servicios financieros",
    "13": "Cuidado personal, protección social y otros",
}

# Valores oficiales de la documentación de usuario EPF 2024 (INE)
MAP_TAMANO = {1: "Una persona", 2: "Dos personas", 3: "Tres personas",
              4: "Cuatro personas", 5: "Cinco personas", 6: "Seis o más personas"}
MAP_SEXOSP = {1: "Hombre", 6: "Mujer"}
MAP_ESTUDIOS = {1: "Inferior a 1ª etapa de Secundaria", 2: "Primera etapa de Secundaria",
                3: "Segunda etapa de Secundaria", 4: "Educación Superior"}
MAP_SITUACT = {1: "Trabajando", 2: "Parado/a", 3: "Jubilado/a o retirado/a",
               4: "Incapacidad laboral permanente", 5: "Estudiante",
               6: "Tareas del hogar", 7: "Otra inactividad"}
MAP_REGTEN = {1: "Propiedad sin hipoteca", 2: "Propiedad con hipoteca", 3: "Alquiler",
              4: "Alquiler reducido", 5: "Cesión semigratuita", 6: "Cesión gratuita"}
MAP_TIPOCASA = {1: "Chalé o casa grande", 2: "Casa media", 3: "Casa económica o alojamiento"}
MAP_NACION = {1: "Solo española", 2: "Solo extranjera", 3: "Española y extranjera"}
MAP_INTERIN = {0: "No consta", 1: "Menos de 500 €", 2: "500 – 1.000 €", 3: "1.000 – 1.500 €",
               4: "1.500 – 2.000 €", 5: "2.000 – 2.500 €", 6: "2.500 – 3.000 €",
               7: "3.000 – 5.000 €", 8: "5.000 – 7.000 €", 9: "7.000 – 9.000 €",
               10: "9.000 € y más"}
MAP_FUENPRIN = {1: "Cuenta propia, rentas y capital", 2: "Trabajo por cuenta ajena",
                3: "Pensiones, subsidios y prestaciones", -9: "No consta"}
MAP_TAMAMU = {1: "100.000 hab. o más", 2: "50.000 – 100.000 hab.", 3: "20.000 – 50.000 hab.",
              4: "10.000 – 20.000 hab.", 5: "Menos de 10.000 hab."}
MAP_DENSIDAD = {1: "Densamente poblada", 2: "Intermedia", 3: "Diseminada"}
MAP_ZONARES = {1: "Urbana alta", 2: "Urbana media", 3: "Urbana inferior", 4: "Rural"}

# ---------------------------------------------------------------------------
# PASO 1 · GASTOS -> HOGAR x GRUPO  (cambiamos el grano por agregación)
# ---------------------------------------------------------------------------
print("PASO 1 · Leyendo y agregando GASTOS...")
F_GASTOS = BRUTOS / "EPFgastos_2024.csv"
dec_g = detectar_decimal(F_GASTOS, "\t", "latin1", "GASTO")
gastos = pd.read_csv(F_GASTOS, sep="\t", encoding="latin1", decimal=dec_g,
                     usecols=["NUMERO", "CODIGO", "GASTO"], dtype={"CODIGO": str})
gastos["GRUPO"] = gastos["CODIGO"].str.zfill(5).str[:2]          # "01111" -> "01"
agg = (gastos.groupby(["NUMERO", "GRUPO"], as_index=False)
             .agg(gasto_grupo_elev=("GASTO", "sum"),
                  n_partidas=("GASTO", "size")))
print(f"   {len(gastos):>10,} partidas  ->  {len(agg):>10,} filas hogar x grupo")

# ---------------------------------------------------------------------------
# PASO 2 · HOGAR  (29 variables con valor analítico)
# ---------------------------------------------------------------------------
print("PASO 2 · Leyendo HOGAR...")
F_HOGAR = BRUTOS / "EPFhogar_2024.csv"
dec_h = detectar_decimal(F_HOGAR, "\t", "latin1", "FACTOR")
COLS_HOGAR = ["NUMERO", "ANOENC", "CCAA", "NUTS1", "CAPROV", "TAMAMU", "DENSIDAD",
              "ZONARES", "FACTOR", "NMIEMB", "TAMANO", "NUMACTI", "NUMOCUP",
              "NNINOSD", "NHIJOSD", "UC1", "EDADSP", "SEXOSP", "ESTUDREDSP",
              "SITUACTSP", "NACIONASP", "REGTEN", "TIPOCASA", "NHABIT", "SUPERF",
              "INTERIN", "FUENPRINRED", "IMPEXAC", "GASTOT"]
hogar = pd.read_csv(F_HOGAR, sep="\t", encoding="latin1", decimal=dec_h,
                    usecols=COLS_HOGAR)
hogar["CCAA"] = hogar["CCAA"].astype(int).astype(str).str.zfill(2)   # 17 -> "17"
print(f"   {len(hogar):>10,} hogares x {hogar.shape[1]} columnas")

# ---------------------------------------------------------------------------
# PASO 3 · UNIÓN 1 · hogar x grupo + atributos del hogar (clave: NUMERO)
# ---------------------------------------------------------------------------
print("PASO 3 · Uniendo gasto con atributos del hogar (por NUMERO)...")
base = agg.merge(hogar, on="NUMERO", how="left")
print(f"   {len(base):>10,} filas x {base.shape[1]} columnas")

# ---------------------------------------------------------------------------
# PASO 4 · IPC (segunda fuente): índice e inflación 2024 por CCAA x grupo
# ---------------------------------------------------------------------------
print("PASO 4 · Preparando IPC 2024...")
F_IPC = BRUTOS / "IPC_2024.csv"
dec_i = detectar_decimal(F_IPC, "\t", "utf-8-sig", "Total")
ipc = pd.read_csv(F_IPC, sep="\t", encoding="utf-8-sig", decimal=dec_i)
ipc.columns = ["ccaa_txt", "grupo_txt", "tipo", "periodo", "valor"]
ipc = ipc[ipc["periodo"] == 2024].copy()
ipc["ccaa"]  = ipc["ccaa_txt"].str.extract(r"^(\d{2})")     # descarta 'Nacional'
ipc["grupo"] = ipc["grupo_txt"].str.extract(r"^(\d{2})")    # descarta 'Índice general'
ipc = ipc.dropna(subset=["ccaa", "grupo"])
idx = ipc[ipc["tipo"] == "Media anual"].rename(
        columns={"valor": "ipc_indice_2024"})[["ccaa", "grupo", "ipc_indice_2024"]]
var = ipc[ipc["tipo"].str.startswith("Variación")].rename(
        columns={"valor": "ipc_var_anual_2024"})[["ccaa", "grupo", "ipc_var_anual_2024"]]
ipc_final = idx.merge(var, on=["ccaa", "grupo"], how="left")
ccaa_nombre = (ipc.assign(n=ipc["ccaa_txt"].str.replace(r"^\d{2}\s*", "", regex=True))
                  .drop_duplicates("ccaa").set_index("ccaa")["n"].to_dict())
print(f"   {len(ipc_final):>10,} celdas CCAA x grupo (19 x 13)")

# ---------------------------------------------------------------------------
# PASO 5 · UNIÓN 2 · añadimos el IPC (clave: CCAA + GRUPO) << une las 2 fuentes
# ---------------------------------------------------------------------------
print("PASO 5 · Uniendo con el IPC (por CCAA + GRUPO)...")
final = (base.merge(ipc_final, left_on=["CCAA", "GRUPO"],
                    right_on=["ccaa", "grupo"], how="left")
              .drop(columns=["ccaa", "grupo"]))
print(f"   {len(final):>10,} filas x {final.shape[1]} columnas")

# ---------------------------------------------------------------------------
# PASO 6 · Etiquetas de grupo/CCAA y gasto en euros por hogar (= elevado / FACTOR)
# ---------------------------------------------------------------------------
final["grupo_nombre"]    = final["GRUPO"].map(GRUPO_NOMBRE)
final["ccaa_nombre"]     = final["CCAA"].map(ccaa_nombre)
final["gasto_grupo_eur"] = (final["gasto_grupo_elev"] / final["FACTOR"]).round(2)

# ---------------------------------------------------------------------------
# PASO 6b · Traducción de las variables codificadas a etiquetas legibles
#   Se conservan los códigos originales (para ordenar los ordinales en Power BI)
#   y se añaden columnas de texto con los valores oficiales de la EPF 2024.
# ---------------------------------------------------------------------------
print("PASO 6b · Mapeando variables codificadas (valores oficiales EPF 2024)...")
final["tamano_hogar"]           = etiquetar(final["TAMANO"], MAP_TAMANO)
final["sexo_sp"]                = etiquetar(final["SEXOSP"], MAP_SEXOSP)
final["nivel_estudios_sp"]      = etiquetar(final["ESTUDREDSP"], MAP_ESTUDIOS)
final["situacion_actividad_sp"] = etiquetar(final["SITUACTSP"], MAP_SITUACT)
final["regimen_tenencia"]       = etiquetar(final["REGTEN"], MAP_REGTEN)
final["tipo_vivienda"]          = etiquetar(final["TIPOCASA"], MAP_TIPOCASA)
final["nacionalidad_sp"]        = etiquetar(final["NACIONASP"], MAP_NACION)
final["intervalo_ingresos"]     = etiquetar(final["INTERIN"], MAP_INTERIN)
final["fuente_ingresos"]        = etiquetar(final["FUENPRINRED"], MAP_FUENPRIN)
final["tamano_municipio"]       = etiquetar(final["TAMAMU"], MAP_TAMAMU)
final["densidad_municipio"]     = etiquetar(final["DENSIDAD"], MAP_DENSIDAD)
final["zona_residencia"]        = etiquetar(final["ZONARES"], MAP_ZONARES)

# ---------------------------------------------------------------------------
# PASO 7 · Validación contra el INE y guardado (CSV + XLSX correcto)
# ---------------------------------------------------------------------------
th = final.groupby("NUMERO").agg(e=("gasto_grupo_elev", "sum"),
                                 g=("GASTOT", "first"), f=("FACTOR", "first"))
dif = ((th.e - th.g) / th.g * 100).abs().max()
gasto_medio = th.e.sum() / th.f.sum()

out_csv  = FINALES / "epf_ipc_2024_final.csv"
out_xlsx = FINALES / "epf_ipc_2024_final.xlsx"
final.to_csv(out_csv, index=False, encoding="utf-8")
final.to_excel(out_xlsx, index=False, engine="xlsxwriter")

print("\n" + "=" * 62)
print("RESULTADO · un único conjunto de datos, legible")
print("=" * 62)
print(f"  Dimensiones : {final.shape[0]:,} filas x {final.shape[1]} columnas")
print(f"  QA vs GASTOT: diferencia máxima {dif:.4f} %   (debe ser 0)")
print(f"  Gasto medio : {gasto_medio:,.2f} EUR/hogar    (oficial INE ~34.044)")
print(f"  Guardado    : {out_csv.name}  y  {out_xlsx.name}  (en FINALES)")
