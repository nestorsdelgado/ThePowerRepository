"""
Proyecto EDA — Campañas de marketing bancario
=============================================
Versión .py del análisis (equivalente al notebook eda_bank_marketing.ipynb).
Ejecuta de principio a fin toda la limpieza, la unión de datasets, el análisis
descriptivo y la generación de figuras.

Uso:
    python eda_bank_marketing.py

Las figuras se guardan en IMAGENES/ y los datos procesados en DATOS/DATOS_PROCESADOS.
El backend de matplotlib se fija en 'Agg' para poder ejecutarlo sin entorno gráfico.
"""
import matplotlib
matplotlib.use("Agg")   # backend no interactivo: permite guardar figuras sin ventana

# # Proyecto EDA — Campañas de marketing bancario
# 
# **Análisis Exploratorio de Datos (EDA) con Python y Pandas**
# 
# Este cuaderno documenta, paso a paso y explicando el *porqué* de cada decisión, el
# análisis exploratorio de las campañas de marketing telefónico de una institución
# bancaria portuguesa cuyo objetivo era que el cliente suscribiese un **depósito a
# plazo** (variable objetivo `y`).
# 
# ## Objetivo del análisis
# 
# Responder a la pregunta de negocio: **¿qué caracteriza a los clientes que sí
# suscriben el depósito?** Es decir, qué variables (perfil del cliente, canal de
# contacto, historial de campañas, contexto macroeconómico) se asocian con una mayor
# tasa de conversión.
# 
# ## Conjuntos de datos
# 
# - **`bank-additional.csv`** — 43.000 registros, uno por interacción de campaña.
# - **`customer-details.xlsx`** — 3 hojas (`2012`, `2013`, `2014`) con los datos
#   demográficos y de comportamiento de los clientes. Se cruzan con el CSV por el
#   identificador único de cliente.
# 
# ## Índice
# 
# 0. Importaciones y configuración
# 1. Carga de datos
# 2. Exploración inicial
# 3. Limpieza y transformación de `bank-additional`
# 4. Limpieza y transformación de `customer-details`
# 5. Unión de los dos conjuntos (`merge`)
# 6. Guardado del dataset procesado
# 7. Análisis descriptivo
# 8. Visualizaciones
# 9. Informe y conclusiones

# ## 0. Importaciones y configuración

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Resolvemos la ruta base del proyecto a partir de la ubicación de este archivo.
# El script está en la raíz del proyecto, así que BASE es la carpeta que lo contiene.
BASE = Path(__file__).resolve().parent
CRUDOS = BASE / "DATOS" / "DATOS_INICIALES"
PROC   = BASE / "DATOS" / "DATOS_PROCESADOS"
IMG    = BASE / "DATOS" / "IMAGENES"
PROC.mkdir(parents=True, exist_ok=True)
IMG.mkdir(parents=True, exist_ok=True)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
sns.set_theme(style="whitegrid")
PALETA = ["#2f6690", "#d9534f"]   # azul = no, rojo = yes

print("Ruta base del proyecto:", BASE)

# ## 1. Carga de datos

# Cargamos el CSV de campañas y el Excel de clientes. El Excel tiene **tres hojas**,
# una por año de alta del cliente. Las leemos todas de golpe con `sheet_name=None`
# (que devuelve un diccionario `{nombre_hoja: DataFrame}`) y las concatenamos en un
# único DataFrame usando una **comprensión de listas**, añadiendo de paso el año de la
# hoja como columna trazable.

bank = pd.read_csv(CRUDOS / "bank-additional.csv")
print("bank-additional:", bank.shape)

hojas = pd.read_excel(CRUDOS / "customer-details.xlsx", sheet_name=None)
print("Hojas del Excel:", list(hojas.keys()))

# Comprensión de listas para concatenar las 3 hojas anexando el año de la hoja
cust = pd.concat(
    [df.assign(anho_alta_hoja=int(nombre)) for nombre, df in hojas.items()],
    ignore_index=True,
)
print("customer-details (3 hojas unidas):", cust.shape)

# ## 2. Exploración inicial

# Antes de tocar nada, radiografiamos ambos conjuntos: estructura, tipos de dato,
# valores nulos y duplicados. Esto guía toda la limpieza posterior.

bank.head()

bank.info()

# Observaciones de esta primera radiografía de `bank`:
# 
# - `Unnamed: 0` es una columna índice sobrante.
# - `cons.price.idx`, `cons.conf.idx`, `euribor3m` y `nr.employed` llegan como **texto**
#   (`object`) porque usan **coma decimal** (`"93,994"`), no punto.
# - `date` es texto en español (`"2-agosto-2019"`).
# - `marital` y `poutcome` vienen en MAYÚSCULAS.
# - Hay columnas `latitude`/`longitude` que **no** aparecen en la documentación.

# Nulos y duplicados en bank
print("Nulos por columna:")
print(bank.isna().sum()[bank.isna().sum() > 0].sort_values(ascending=False))
print("\nFilas duplicadas (ignorando el índice sobrante):",
      bank.drop(columns=["Unnamed: 0"]).duplicated().sum())
print("id_ duplicados:", bank["id_"].duplicated().sum())

# Radiografía del Excel de clientes
print(cust.info())
print("\nNulos:", cust.isna().sum().to_dict())
print("ID duplicados:", cust["ID"].duplicated().sum())
cust.head()

# El Excel está limpio de origen: sin nulos, `ID` único y tipos correctos (incluida
# `Dt_Customer` como fecha). Su columna `ID` es la que nos permitirá cruzarlo con `bank`.

# ## 3. Limpieza y transformación de `bank-additional`

# ### 3.1 Eliminar la columna índice sobrante

bank = bank.drop(columns=["Unnamed: 0"])

# ### 3.2 Convertir los decimales con coma a `float`
# Estas cuatro columnas son numéricas pero llegan como texto con coma decimal.
# Sustituimos la coma por punto y convertimos a `float`. Si no lo hiciéramos, no
# podríamos calcular medias, correlaciones ni graficarlas.

cols_coma = ["cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"]
for c in cols_coma:
    bank[c] = bank[c].str.replace(",", ".", regex=False).astype(float)
bank[cols_coma].dtypes

# ### 3.3 Normalizar categóricas en mayúsculas
# `marital` y `poutcome` vienen en mayúsculas. Las pasamos a minúscula para
# homogeneizar y evitar categorías duplicadas por diferencias de formato.

bank["marital"] = bank["marital"].str.lower()
bank["poutcome"] = bank["poutcome"].str.lower()
print(bank["marital"].unique())
print(bank["poutcome"].unique())

# ### 3.4 Parsear la fecha en español
# `date` es texto tipo `"2-agosto-2019"`. Definimos un **diccionario** que traduce el
# mes en español a su número y una **función** que descompone la cadena y construye un
# `Timestamp`. La función devuelve `NaT` (fecha nula) cuando el valor original ya era
# nulo o no se puede parsear, en lugar de romper la ejecución.

MESES = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12",
}

def parsea_fecha(txt):
    '''Convierte '2-agosto-2019' en Timestamp. Devuelve NaT si no es posible.'''
    if pd.isna(txt):
        return pd.NaT
    try:
        dia, mes, anho = txt.split("-")
        return pd.Timestamp(f"{anho}-{MESES[mes]}-{int(dia):02d}")
    except (ValueError, KeyError):
        return pd.NaT

bank["date"] = bank["date"].apply(parsea_fecha)
# Derivamos año y mes para el análisis temporal
bank["anho_campanha"] = bank["date"].dt.year
bank["mes_campanha"] = bank["date"].dt.month
print("Fechas nulas (NaT) tras el parseo:", bank["date"].isna().sum())
bank[["date", "anho_campanha", "mes_campanha"]].head()

# ### 3.5 `default`, `housing`, `loan`: de binaria numérica a categórica
# Estas tres columnas son 0/1 pero tienen muchos nulos (sobre todo `default`, con casi
# un 21%). **No las imputamos por la moda**: eso falsearía la realidad inflando
# artificialmente el grupo mayoritario. En su lugar convertimos el nulo en una
# categoría propia `"unknown"`. Así conservamos la señal de "dato ausente", que además
# —como veremos— resulta ser informativa por sí misma.

map_bin = {0.0: "no", 1.0: "yes"}
for c in ["default", "housing", "loan"]:
    bank[c] = bank[c].map(map_bin).fillna("unknown")
    print(c, "->", bank[c].value_counts().to_dict())

# ### 3.6 Categóricas de texto con nulos → `"unknown"`
# Mismo criterio para `job`, `education` y `marital`: rellenar el nulo con una
# etiqueta `"unknown"` en vez de inventar una categoría, preservando la información de
# que el dato faltaba.

for c in ["job", "education", "marital"]:
    bank[c] = bank[c].fillna("unknown")
bank[["job", "education", "marital"]].isna().sum()

# ### 3.7 `age`: comparación de dos estrategias de imputación
# `age` tiene ~12% de nulos. Comparamos dos imputaciones para decidir con criterio:
# 1. **Mediana global** — simple.
# 2. **Mediana por profesión (`job`)** — más fina, porque la edad típica varía según el
#    trabajo (p. ej. `student` vs `retired`).
# 
# Usamos la mediana (no la media) por ser robusta frente a valores extremos.

mediana_global = bank["age"].median()
age_global = bank["age"].fillna(mediana_global)
age_por_job = bank["age"].fillna(bank.groupby("job")["age"].transform("median"))

comparacion = pd.DataFrame({
    "original":      bank["age"].describe(),
    "imput_global":  age_global.describe(),
    "imput_por_job": age_por_job.describe(),
})
print("Mediana global de age:", mediana_global)
comparacion.round(3)

# Ambas imputaciones apenas mueven la distribución (media 39.74 vs 39.82; misma mediana
# y percentiles casi idénticos), porque `age` no está fuertemente ligada a `job`. Aun
# así **elegimos la imputación por profesión** por ser conceptualmente más correcta: no
# introduce distorsión y respeta las diferencias por grupo.

bank["age"] = age_por_job
bank["age"].isna().sum()

# ### 3.8 `euribor3m` y `cons.price.idx`: imputación por mediana agrupada
# Son indicadores **macroeconómicos**. En vez de una mediana global ciega, imputamos con
# la mediana **agrupada por `emp.var.rate`** (tasa de variación del empleo, sin nulos),
# que representa el "régimen económico" del momento y está muy correlacionada con ellos.
# Si algún grupo quedara sin mediana, caemos a la mediana global como red de seguridad.

for c in ["euribor3m", "cons.price.idx"]:
    antes = bank[c].isna().sum()
    med_grupo = bank.groupby("emp.var.rate")[c].transform("median")
    bank[c] = bank[c].fillna(med_grupo).fillna(bank[c].median())
    print(f"{c}: {antes} nulos -> {bank[c].isna().sum()} tras la imputación")

# ### 3.9 Nueva columna derivada: `contactado_antes`
# `pdays == 999` es un código que significa "nunca se contactó antes", no un número de
# días real. Creamos una variable categórica explícita para no contaminar los cálculos
# numéricos sobre `pdays` y para poder analizar ese grupo por separado.

bank["contactado_antes"] = np.where(bank["pdays"] == 999, "no", "si")
bank["contactado_antes"].value_counts()

# ### 3.10 `latitude` / `longitude`: decisión razonada de descartarlas
# Estas columnas no están en la documentación. Antes de descartarlas comprobamos si
# aportan información: unicidad, dependencia de otras variables y correlaciones.

print("Pares (lat, long) únicos:", bank[["latitude", "longitude"]].drop_duplicates().shape[0], "de", len(bank))
print("corr(lat, long):", round(bank["latitude"].corr(bank["longitude"]), 4))
print("\nCuantiles latitude:", bank["latitude"].quantile([0, .25, .5, .75, 1]).round(1).tolist())
print("Cuantiles longitude:", bank["longitude"].quantile([0, .25, .5, .75, 1]).round(1).tolist())

# Son **43.000 pares únicos**, repartidos de forma **uniforme** por todo EEUU
# continental (cuantiles equiespaciados), con correlación ≈0 entre sí y sin relación con
# ninguna otra variable. Es decir: coordenadas **sintéticas generadas al azar** (además,
# caen en EEUU cuando el banco es portugués). No aportan señal analizable, así que las
# **eliminamos** dejando constancia del motivo.

bank = bank.drop(columns=["latitude", "longitude"])

# ### 3.11 Estado final de `bank` tras la limpieza

print("Shape:", bank.shape)
print("\nNulos restantes (solo la fecha irrecuperable):")
print(bank.isna().sum()[bank.isna().sum() > 0])
bank.dtypes

# ## 4. Limpieza y transformación de `customer-details`

# El Excel estaba limpio. Solo eliminamos la columna índice sobrante y derivamos el año
# de alta desde `Dt_Customer`. Verificamos además que ese año coincide siempre con la
# hoja de origen (control de calidad); al ser así, la columna del año de hoja es
# redundante y la eliminamos.

cust = cust.drop(columns=["Unnamed: 0"])
cust["anho_alta"] = cust["Dt_Customer"].dt.year

# Control de calidad: ¿el año de alta coincide con la hoja?
print("¿anho_alta coincide siempre con la hoja de origen?",
      (cust["anho_alta"] == cust["anho_alta_hoja"]).all())

cust = cust.drop(columns=["anho_alta_hoja"])   # redundante
print("customer limpio:", cust.shape)
cust.head()

# ## 5. Unión de los dos conjuntos (`merge`)

# Cruzamos por el identificador de cliente (`id_` en bank ↔ `ID` en customer). Usamos un
# `merge` de tipo **outer con `indicator=True`**, que añade una columna `_merge`
# etiquetando cada fila como:
# 
# - `both` — cliente con campaña (los 43.000 registros que analizaremos).
# - `right_only` — cliente **sin campaña** (nunca fue contactado).
# - `left_only` — campaña sin cliente (no debería haber ninguna).
# 
# Así identificamos explícitamente a los clientes sin campaña en lugar de perderlos en
# silencio con un *join* interno.

df = bank.merge(cust, left_on="id_", right_on="ID", how="outer", indicator=True)
print("Resultado del merge:", df.shape)
print(df["_merge"].value_counts())

# Separamos los dos grupos para el análisis
con_campanha = df[df["_merge"] == "both"].copy()
sin_campanha = df[df["_merge"] == "right_only"].copy()
print("Registros CON campaña:", len(con_campanha))
print("Clientes  SIN campaña:", len(sin_campanha))

# Confirmamos que **los 43.000 registros de campaña tienen su cliente** en el Excel
# (0 `left_only`) y que hay **170 clientes registrados que nunca fueron contactados**
# (`right_only`). El análisis principal se hace sobre `con_campanha`; a los 170 sin
# campaña les dedicamos una sección propia (7.6).

# ## 6. Guardado del dataset procesado

# Guardamos el conjunto ya limpio y unido en `datos/procesados/`. Eliminamos la columna
# `ID` (redundante con `id_`). Guardamos tanto el dataset completo (con la marca
# `_merge`) como el subconjunto con campaña, que es el que alimenta el análisis.

df.drop(columns=["ID"]).to_csv(PROC / "datos_procesados.csv", index=False)
con_campanha.drop(columns=["ID"]).to_csv(PROC / "datos_con_campanha.csv", index=False)
print("Guardado en", PROC)
print(" - datos_procesados.csv   ", df.drop(columns=['ID']).shape)
print(" - datos_con_campanha.csv ", con_campanha.drop(columns=['ID']).shape)

# ## 7. Análisis descriptivo

# Trabajamos sobre `con_campanha`. La pregunta que guía todo el análisis es *qué se
# asocia con una mayor tasa de conversión* (`y == "yes"`).

# ### 7.1 Tasa de conversión global y descriptivos numéricos

c = con_campanha   # alias corto

tasa_global = (c["y"] == "yes").mean()
print(f"Tasa de conversión global: {tasa_global:.2%} "
      f"({(c['y']=='yes').sum()} de {len(c)})")

c[["age", "duration", "campaign", "previous", "euribor3m",
   "cons.price.idx", "Income", "NumWebVisitsMonth"]].describe().round(2)

# La conversión global es de **11,3%**: un problema **desbalanceado** (casi 9 de cada 10
# clientes dicen que no). Es el punto de referencia contra el que comparar cada grupo.

# ### 7.2 Función auxiliar para tasa de conversión por grupo

# Definimos una función reutilizable que, dada una columna categórica, devuelve el
# tamaño de cada grupo y su tasa de conversión. Evita repetir el mismo `groupby` una y
# otra vez (buena práctica: no duplicar código).

def tasa_por(col, orden_por_tasa=True):
    '''Devuelve n y tasa de conversión (y=='yes') por categoría de `col`.'''
    resumen = (c.groupby(col)
                 .agg(n=("y", "size"),
                      tasa_conversion=("y", lambda s: (s == "yes").mean())))
    return resumen.sort_values("tasa_conversion", ascending=False) if orden_por_tasa else resumen

tasa_por("poutcome")

# ### 7.3 Conversión por historial de campañas y canal

print("-- Por resultado de campaña previa (poutcome) --")
print(tasa_por("poutcome").round(4), "\n")
print("-- Por si se había contactado antes --")
print(tasa_por("contactado_antes").round(4), "\n")
print("-- Por canal de contacto --")
print(tasa_por("contact").round(4))

# Tres hallazgos muy fuertes:
# 
# - **`poutcome == success`** dispara la conversión al **65,3%** (vs 8,8% cuando no hubo
#   campaña previa). Un cliente que ya aceptó antes es, con diferencia, el mejor objetivo.
# - Coherentemente, **haber sido contactado antes** (`contactado_antes == si`) sube la
#   tasa al **64,0%**.
# - El **canal móvil** (`cellular`, 14,7%) convierte casi el **triple** que el fijo
#   (`telephone`, 5,2%).

# ### 7.4 Conversión por perfil del cliente

for col in ["job", "education", "marital"]:
    print(f"-- {col} --")
    print(tasa_por(col).round(4), "\n")

# - **`job`**: `student` (31,3%) y `retired` (25,2%) encabezan; `blue-collar` (6,9%) y
#   `services` (8,1%) son los más difíciles.
# - **`education`**: la tasa crece con el nivel educativo (salvo `illiterate`, con solo
#   18 casos). `university.degree` convierte al 13,7%.
# - **`marital`**: `single` (13,9%) convierte más que `married` (10,2%).

# ### 7.5 `default` / `housing` / `loan`: tamaños y medias por grupo

# Aquí se ve por qué convertir los nulos en categoría `"unknown"` fue acertado: en
# `default`, el grupo `unknown` convierte menos de la mitad (5,2%) que el grupo `no`
# (12,9%). El "dato ausente" es informativo. Además comparamos las medias de cada grupo.

for col in ["default", "housing", "loan"]:
    print(f"== {col} ==")
    print("Tasa de conversión:")
    print(tasa_por(col).round(4))
    print("Medias por grupo:")
    print(c.groupby(col)[["age", "duration", "Income", "campaign"]].mean().round(2), "\n")

# `housing` y `loan` apenas mueven la conversión (todos los grupos ~11%): son poco
# predictivos. `default` sí distingue (`no` 12,9% vs `unknown` 5,2%).

# ### 7.6 Conversión por franja de edad

# Discretizamos `age` en tramos con `pd.cut` para ver el patrón por edad con claridad.

c["franja_edad"] = pd.cut(c["age"], bins=[16, 25, 35, 45, 55, 65, 100],
                          labels=["17-25", "26-35", "36-45", "46-55", "56-65", "66+"])
tasa_por("franja_edad", orden_por_tasa=False).round(4)

# La conversión describe una **U**: alta en los extremos —jóvenes (17-25: 21,7%) y sobre
# todo mayores (66+: 46,0%)— y baja en el tramo central de edad activa (36-55: ~9%).
# Encaja con el liderazgo de `student` y `retired` por profesión.

# ### 7.7 Contexto macroeconómico y su evolución temporal

# Néstor planteaba: *¿el euríbor y el IPC son estables o cambian con el tiempo?* Lo
# analizamos agregando por trimestre, y de paso miramos su relación con la conversión.

temporal = (c.dropna(subset=["date"])
              .groupby(c["date"].dt.to_period("Q"))
              .agg(euribor=("euribor3m", "mean"),
                   ipc=("cons.price.idx", "mean"),
                   tasa=("y", lambda s: (s == "yes").mean())))
temporal.index = temporal.index.to_timestamp()
print("euribor3m -> std:", round(c["euribor3m"].std(), 3),
      "| rango:", round(c["euribor3m"].min(), 2), "-", round(c["euribor3m"].max(), 2))
print("\nMedia trimestral (primeras filas):")
print(temporal.round(3).head())

corr_euri = c["euribor3m"].corr((c["y"] == "yes").astype(int))
print(f"\nCorrelación euribor3m <-> conversión: {corr_euri:.3f}")

# Dos observaciones, una de ellas crítica sobre la calidad del dato:
# 
# 1. A nivel de **registro**, el euríbor correlaciona **negativamente** con la conversión
#    (**−0,31**): cuando el euríbor está bajo, el cliente suscribe más. Es el patrón
#    económico esperado (con tipos bajos, el depósito compite mejor con alternativas).
# 2. Sin embargo, la **media trimestral del euríbor es prácticamente plana** (~3,6 en
#    todo 2015-2019) pese a tener una desviación enorme (std 1,74; rango 0,63-5,04). Esto
#    significa que **la columna `date` fue asignada de forma independiente al euríbor**:
#    no existe una tendencia temporal real. Es un artefacto del conjunto (sintético), y
#    conviene señalarlo para no sobre-interpretar el eje temporal.

# ### 7.8 Matriz de correlaciones

num_cols = ["age", "duration", "campaign", "previous", "emp.var.rate",
            "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed",
            "Income", "Kidhome", "Teenhome", "NumWebVisitsMonth"]
corr = c[num_cols].corr()
corr.round(2)

# - El bloque macro (`emp.var.rate`, `euribor3m`, `nr.employed`, `cons.price.idx`) está
#   **muy correlacionado internamente** (0,7-0,97): son manifestaciones del mismo ciclo
#   económico (multicolinealidad).
# - Las variables demográficas del Excel (`Income`, `Kidhome`, `Teenhome`,
#   `NumWebVisitsMonth`) tienen correlación ≈0 con todo lo demás: **no se relacionan con
#   la conversión**, lo que sugiere que se generaron de forma independiente al resultado
#   de campaña.

# ### 7.9 Perfil de los 170 clientes sin campaña

print("Income medio  -> sin campaña:", round(sin_campanha["Income"].mean(), 0),
      "| con campaña:", round(con_campanha["Income"].mean(), 0))
print("Altas por año:", sin_campanha["anho_alta"].value_counts().sort_index().to_dict())
sin_campanha[["Income", "Kidhome", "Teenhome", "NumWebVisitsMonth"]].describe().round(2)

# Los 170 clientes nunca contactados tienen un perfil demográfico **muy similar** al del
# resto (ingresos ligeramente menores) y se concentran en altas de **2012**. Son una
# bolsa de clientes disponibles que la campaña no llegó a aprovechar.

# ## 8. Visualizaciones

# Definimos una pequeña función para guardar cada figura en `img/` además de mostrarla,
# y generamos los gráficos que resumen los hallazgos.

def guarda(fig, nombre):
    fig.tight_layout()
    fig.savefig(IMG / nombre, dpi=110, bbox_inches="tight")

def barras_tasa(col, titulo, horizontal=False, ordenar=True):
    tp = tasa_por(col, orden_por_tasa=ordenar)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    if horizontal:
        ax.barh(tp.index.astype(str), tp["tasa_conversion"], color="#2f6690")
        ax.invert_yaxis(); ax.set_xlabel("Tasa de conversión")
    else:
        ax.bar(tp.index.astype(str), tp["tasa_conversion"], color="#2f6690")
        ax.set_ylabel("Tasa de conversión")
        for i, v in enumerate(tp["tasa_conversion"]):
            ax.text(i, v, f"{v:.1%}", ha="center", va="bottom", fontsize=9)
    ax.set_title(titulo)
    return fig

# ### 8.1 Distribución de la variable objetivo

fig, ax = plt.subplots(figsize=(5, 4))
vc = c["y"].value_counts()
ax.bar(vc.index, vc.values, color=PALETA)
for i, v in enumerate(vc.values):
    ax.text(i, v, f"{v}\n({v/len(c):.1%})", ha="center", va="bottom")
ax.set_title("Distribución de la variable objetivo (y)")
ax.set_ylabel("Nº de clientes")
guarda(fig, "01_distribucion_y.png"); plt.show()

# ### 8.2 Conversión por profesión y por resultado de campaña previa

fig = barras_tasa("job", "Tasa de conversión por profesión (job)", horizontal=True)
guarda(fig, "02_conversion_job.png"); plt.show()

fig = barras_tasa("poutcome", "Conversión según campaña previa (poutcome)")
guarda(fig, "03_conversion_poutcome.png"); plt.show()

# ### 8.3 Edad y duración de la llamada según el resultado

fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(data=c, x="y", y="age", hue="y", palette=PALETA, legend=False, ax=ax)
ax.set_title("Distribución de edad según suscripción")
guarda(fig, "04_edad_por_y.png"); plt.show()

fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(data=c, x="y", y="duration", hue="y", palette=PALETA, legend=False, ax=ax)
ax.set_title("Duración de la llamada (segundos) según suscripción")
guarda(fig, "05_duration_por_y.png"); plt.show()

# > **Advertencia sobre `duration`.** Las llamadas de clientes que suscriben son mucho
# > más largas, pero `duration` **solo se conoce al terminar la llamada**: no sirve para
# > predecir *a priori* y, en un modelo, provocaría fuga de información. La incluimos
# > como hallazgo descriptivo, no como palanca de acción.

# ### 8.4 Conversión por franja de edad

fig = barras_tasa("franja_edad", "Tasa de conversión por franja de edad", ordenar=False)
guarda(fig, "06_conversion_edad.png"); plt.show()

# ### 8.5 Euríbor y conversión en el tiempo

fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(temporal.index, temporal["euribor"], color="#2f6690", marker="o", label="euribor3m")
ax1.set_ylabel("euribor3m (media trim.)", color="#2f6690")
ax2 = ax1.twinx()
ax2.plot(temporal.index, temporal["tasa"], color="#d9534f", marker="s", label="conversión")
ax2.set_ylabel("Tasa de conversión", color="#d9534f")
ax1.set_title("Euríbor y tasa de conversión por trimestre")
guarda(fig, "07_euribor_conversion_tiempo.png"); plt.show()

# ### 8.6 Matriz de correlaciones

fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
            square=True, cbar_kws={"shrink": 0.7}, ax=ax)
ax.set_title("Matriz de correlaciones (variables numéricas)")
guarda(fig, "08_correlaciones.png"); plt.show()

# ### 8.7 Ingresos según suscripción y grupos de préstamos

fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(data=c, x="y", y="Income", hue="y", palette=PALETA, legend=False, ax=ax)
ax.set_title("Ingresos (Income) según suscripción")
guarda(fig, "09_income_por_y.png"); plt.show()

fig, axes = plt.subplots(1, 3, figsize=(11, 4))
for ax, col in zip(axes, ["default", "housing", "loan"]):
    vc = c[col].value_counts()
    ax.bar(vc.index, vc.values, color="#2f6690")
    ax.set_title(col)
    for i, v in enumerate(vc.values):
        ax.text(i, v, str(v), ha="center", va="bottom", fontsize=8)
fig.suptitle("Tamaño de los grupos en default / housing / loan")
guarda(fig, "10_grupos_prestamos.png"); plt.show()

# ## 9. Informe y conclusiones

# ### Resumen del proceso
# Partimos de dos fuentes (43.000 interacciones de campaña + 43.170 fichas de cliente en
# un Excel de 3 hojas). Tras **limpiar** (columnas índice sobrantes, decimales con coma,
# categóricas en mayúsculas, fechas en español, nulos tratados con criterio y coordenadas
# sintéticas descartadas) y **unir** ambas fuentes por el identificador de cliente,
# obtuvimos un dataset analizable de 43.000 registros con campaña y detectamos 170
# clientes sin campaña.
# 
# ### Principales hallazgos
# 1. **Problema desbalanceado**: solo el **11,3%** suscribe el depósito.
# 2. **El historial manda**: `poutcome == success` eleva la conversión al **65%**; haber
#    sido contactado antes, al **64%**. La fidelización supera a cualquier variable de
#    perfil.
# 3. **Canal**: el móvil convierte **casi el triple** que el teléfono fijo (14,7% vs 5,2%).
# 4. **Perfil demográfico**: `student` (31%) y `retired` (25%) son los mejores objetivos;
#    la conversión por edad tiene forma de **U** (jóvenes y mayores de 65 arriba, edad
#    media abajo). El nivel educativo alto también ayuda.
# 5. **Contexto macro**: con **euríbor bajo** la conversión sube (correlación −0,31). El
#    bloque de indicadores macro está muy autocorrelacionado.
# 6. **El "dato ausente" informa**: en `default`, el grupo `unknown` convierte menos de la
#    mitad que `no`; tratarlo como categoría (y no imputarlo) fue clave.
# 7. **Limitaciones detectadas**: `duration` no es utilizable como predictor (se conoce a
#    posteriori); las coordenadas y la dimensión temporal parecen sintéticas; las
#    variables demográficas del Excel no se relacionan con la conversión.
# 
# ### Recomendaciones de negocio
# - Priorizar a clientes con **campañas previas exitosas** y **contactar por móvil**.
# - Segmentar por **estudiantes y jubilados** y, en general, por los **extremos de edad**.
# - Aprovechar **ventanas de euríbor bajo** para intensificar las campañas.
# - Recuperar la bolsa de **clientes nunca contactados** como objetivo de futuras acciones.
