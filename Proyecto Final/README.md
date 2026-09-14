# Consumo de los hogares en España en 2024

### Análisis del gasto familiar y su exposición a la inflación (EPF x IPC)

## Descripción

Proyecto de análisis de datos que estudia cómo gastan los hogares españoles y, sobre todo, cómo les afecta la inflación de forma desigual según su nivel de renta. Combina dos fuentes oficiales del Instituto Nacional de Estadística (INE) —la Encuesta de Presupuestos Familiares (EPF) y el Índice de Precios de Consumo (IPC)— para construir un indicador de "inflación sentida" que mide cuánta subida de precios soporta realmente cada tipo de hogar según su cesta de consumo.

El proyecto recorre todo el flujo de un análisis de datos: descarga y limpieza profunda de microdatos, unión de dos fuentes distintas, análisis exploratorio y estadístico en Python, y un dashboard interactivo en Power BI.

**Herramientas y técnicas:** Python (pandas, numpy, matplotlib, seaborn, scipy), análisis exploratorio de datos (EDA), estadística inferencial (contraste de Kruskal-Wallis y correlaciones de Spearman), ponderación de datos de encuesta y visualización interactiva con Power BI.

## Estructura del proyecto

```
Proyecto Final/
├── DATOS/
│   ├── BRUTOS/                     # Datos en bruto del INE (dos fuentes)
│   │   ├── EPFgastos_2024.csv      # EPF - fichero de gastos
│   │   ├── EPFhogar_2024.csv       # EPF - fichero de hogares
│   │   └── IPC_2024.csv            # IPC por CCAA y grupo
│   ├── FINALES/                    # Conjunto de datos final ya unido
│   │   └── epf_ipc_2024_final.csv
│   ├── figuras/                    # 11 figuras generadas por el EDA
│   ├── 01_construir_dataset.py     # Une los 3 CSV en el dataset final
│   ├── eda_epf_ipc_2024.py         # Análisis exploratorio y estadístico
│   ├── eda_epf_ipc_2024.ipynb      # El mismo EDA en formato notebook
│   └── requirements.txt            # Dependencias del proyecto
├── INFORME IPC 2024.pbix           # Dashboard interactivo (Power BI)
├── Informe.md                      # Informe del análisis
├── Informe.pdf                     # Informe del análisis (PDF)
└── README.md
```

## Instalación y requisitos

El proyecto usa Python 3.13. Se recomienda instalar las dependencias dentro de un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate        # en Windows
pip install -r DATOS/requirements.txt
```

Dependencias: pandas, numpy, matplotlib, seaborn, scipy y xlsxwriter.

## Cómo reproducir el análisis

1. **Descargar los datos en bruto** del INE (ver la sección "Fuentes de datos") y colocarlos en `DATOS/BRUTOS/`.
2. **Construir el dataset final.** Desde la carpeta `DATOS/`, ejecutar:
   ```bash
   python 01_construir_dataset.py
   ```
   Genera `FINALES/epf_ipc_2024_final.csv` (dos fuentes unidas, limpias y con etiquetas legibles), y valida el resultado contra las cifras oficiales del INE.
3. **Ejecutar el análisis exploratorio.** Desde `DATOS/`, ejecutar:
   ```bash
   python eda_epf_ipc_2024.py
   ```
   Genera las 11 figuras del análisis en la carpeta `figuras/`.
4. **Abrir el dashboard.** Abrir `INFORME IPC 2024.pbix` con Power BI Desktop, que se conecta al CSV de `DATOS/FINALES/`.

## Pasos seguidos en el proyecto

1. **Adquisición de datos.** Descarga de los microdatos de la EPF 2024 y de la tabla del IPC 2024 desde el INE.
2. **Transformación y limpieza profunda.** Agregación del microdato de gastos (1.856.022 registros) al nivel de hogar por grupo de gasto, selección de variables analíticas y traducción de las variables codificadas a etiquetas legibles con los valores oficiales de la EPF.
3. **Unión de las dos fuentes.** El gasto (EPF) se cruza con los precios (IPC) por comunidad autónoma y grupo de consumo, produciendo un conjunto final de 212.173 filas.
4. **Validación.** La agregación propia reproduce exactamente el gasto total del INE (gasto medio por hogar de 34.044 euros).
5. **Análisis descriptivo, estadístico y visual** en Python, ponderando por el factor de elevación de la muestra.
6. **Dashboard operativo** en Power BI con indicadores clave, filtros y visualizaciones interactivas.

## Fuentes de datos

- INE — Encuesta de Presupuestos Familiares 2024 (microdatos): https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176806&menu=resultados&secc=1254736195147&idp=1254735976608
- INE — Índice de Precios de Consumo 2024, índices por comunidades autónomas y grupos ECOICOP: https://www.ine.es/jaxiT3/Tabla.htm?t=76150

## Resultados y conclusiones

- **El hogar español medio gastó 34.044 euros en 2024** (mediana de 29.468 euros), concentrando casi un tercio del presupuesto en la vivienda y sus suministros (32,4 por ciento), seguida de la alimentación (15,8 por ciento) y el transporte (11,4 por ciento).
- **La composición del gasto cambia con la renta (Ley de Engel):** a menor renta, mayor peso de la alimentación (17,3 por ciento) y la vivienda; a mayor renta, más peso del ocio y la restauración. En los hogares de renta alta la alimentación baja al 8,9 por ciento.
- **Existen diferencias territoriales relevantes,** con la Comunidad de Madrid a la cabeza del gasto por hogar (39.318 euros) y Extremadura en la cola (26.890 euros).
- **La inflación de 2024 no afectó por igual a todos los hogares.** Los de menor renta soportaron una inflación sentida del 3,26 por ciento, frente al 2,91 por ciento de los de mayor renta (media nacional del 2,96 por ciento), al destinar una parte mayor de su presupuesto a las categorías que más se encarecieron.
- **Todas las diferencias analizadas son estadísticamente significativas** (contrastes de Kruskal-Wallis, p < 0,001).

El análisis completo, con su metodología y todas las figuras, está disponible en `Informe.pdf`.

## Próximos pasos

- Ampliar el estudio a varios años para analizar la evolución temporal de la exposición a la inflación.
- Descender a un mayor nivel de detalle de categorías de consumo (subgrupos COICOP).
- Incorporar variables adicionales del hogar para segmentar con más precisión.

## Autor

Néstor — [@nestorsdelgado](https://github.com/nestorsdelgado)
