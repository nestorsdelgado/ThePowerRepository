## 📊 Análisis de la Tasa de Paro en España (2002–2026)

Análisis exploratorio de las tasas de paro en España por comunidad autónoma, grupo de edad y sexo, a partir de datos trimestrales del INE. El proyecto incluye transformación de datos, análisis descriptivo, dashboard interactivo y un informe de conclusiones (en este archivo).

## 📖 Descripción

Este proyecto analiza la evolución de la tasa de paro en España entre 2002 y 2026, con datos desagregados por comunidad autónoma, grupo de edad y sexo. El objetivo es identificar patrones históricos, comparar territorios y detectar brechas por género y edad, usando Excel como herramienta de análisis y visualización.

## 🗂 Estructura del Proyecto

```
ThePowerRepository/
├── Proyecto 1/
├── Datos originales/           # Archivo original descargado del INE
│   └── Tasas_de_paro_...xlsx   # Fuente: https://www.ine.es
├── Proyecto_Paro_España.xlsx   # Archivo principal con todo el proceso
└── README.md                   # Este archivo
```

El archivo Excel contiene las siguientes hojas:

| Hoja | Contenido |
|---|---|
| `Datos originales` | Tabla del INE sin modificar |
| `Datos` | Proceso de transformación con fórmulas visibles |
| `Datos - limpios` | Dataset final en formato largo, listo para análisis |
| `Análisis` | Tablas dinámicas con el análisis descriptivo |
| `Dashboard` | Panel interactivo con gráficos y segmentadores |

---

## 🛠 Instalación y Requisitos

Este proyecto no requiere instalación de software adicional. Solo es necesario:

- Microsoft Excel (versión web o de escritorio)

---

# 🔄 Transformación y Limpieza de Datos

**Origen de los datos:** INE — Encuesta de Población Activa (EPA). Tabla: *Tasas de paro por distintos grupos de edad, sexo y comunidad autónoma*. Descargada en formato Excel desde [https://www.ine.es](https://www.ine.es).

**Problema de partida:** Los datos del INE llegan en formato "pivotado" (ancho y apilado): los territorios en columnas, los trimestres y grupos de edad apilados en filas, con bloques separados por sexo. Este formato no es analizable directamente con tablas dinámicas ni gráficos.

**Proceso de transformación (hoja `Datos`):**

Se construyó manualmente un sistema de despivotado usando fórmulas Excel (sin Power Query), basado en un índice secuencial (columna `Índice`) y cuatro sub-índices que descomponen cada fila de salida en sus coordenadas exactas dentro de la tabla original:

- `Índice - Territorio`: posición del territorio (0–9) dentro del ciclo de 10 CCAA
- `Índice - Edad`: posición del grupo de edad (0–3) dentro del ciclo de 4 franjas
- `Índice - Trimestre`: posición del trimestre (0–96) dentro del ciclo de 97 trimestres
- `Índice - Sexo`: bloque de sexo (0=Hombres, 1=Mujeres)

La lógica funciona como un sistema de base mixta: el territorio cambia más rápido (cada fila), luego la edad (cada 10 filas), luego el trimestre (cada 40 filas) y finalmente el sexo (cada 3.880 filas). Con este sistema, una única fórmula `DESREF` copiada hacia abajo genera automáticamente las filas de la tabla final.

**Decisiones de limpieza aplicadas en `Datos - limpios`:**

- Se mantienen solo las 4 categorías de edad finas (De 16 a 19 años, De 20 a 24 años, De 25 a 54 años, De 55 y más años), eliminando las categorías agregadas (Total, Menores de 25, 25 y más) para evitar doble conteo en los análisis y gráficos.
- Se mantienen solo Hombres y Mujeres como categorías de sexo, eliminando "Ambos sexos" por el mismo motivo.
- Se elimina "Total Nacional" como territorio, ya que los KPIs del dashboard lo calculan directamente mediante fórmulas sobre el dataset completo.
- Se detectaron 2 valores `..` en la columna Tasa (paro), correspondientes a datos no disponibles del INE por muestra insuficiente (Hombres, De 16 a 19 años, País Vasco, en dos trimestres concretos). Estos se marcaron como `N/D` en la columna `Tasa (paro) - limpia` de la hoja `Datos`.

**Chequeos de calidad realizados:**

| Chequeo | Resultado |
|---|---|
| Valor mínimo de Tasa | 0,74% ✅ |
| Valor máximo de Tasa | 100% ✅ (plausible en grupos de edad muy jóvenes) |
| Celdas vacías en Tasa | 0 ✅ |
| Errores residuales | 0 ✅ |
| Filas duplicadas | 0 ✅ |
| Tipo de dato correcto | 0 errores (excluyendo N/D) ✅ |

---

## 📊 Análisis Descriptivo

El análisis se realizó mediante 4 tablas dinámicas en la hoja `Análisis`, todas conectadas a los mismos segmentadores del dashboard:

**1. Evolución temporal (Trimestre × Tasa media)**
Permite ver la trayectoria histórica de la tasa de paro desde 2002T1 hasta 2026T1.

**2. Ranking por Comunidad Autónoma (Territorio × Tasa media)**
Comparación del paro medio histórico entre las 10 CCAA del dataset, ordenadas de mayor a menor.

**3. Distribución por Grupo de Edad (Edad × Tasa media)**
Comparación de las 4 franjas de edad finas, sin solapamiento entre categorías.

**4. Tabla cruzada Sexo × Territorio**
Muestra la tasa media de Hombres y Mujeres por comunidad, permitiendo identificar la brecha de género en cada territorio.

---

## 📈 Resultados y Conclusiones

- La tasa de paro en España alcanzó su máximo histórico en torno a 2013T1 (~40%), como consecuencia de la crisis financiera de 2008. Desde entonces descendió de forma sostenida hasta mínimos recientes en 2026T1 (~15-18% en promedio de las franjas de edad).

- Andalucía y Canarias son consistentemente las comunidades con mayor tasa de paro (33,9% y 32,2% de media histórica respectivamente), mientras que País Vasco registra la menor (21,3%).

- El paro juvenil es estructuralmente muy elevado: la franja de 16 a 19 años tiene una tasa media del 48,3%, cuatro veces superior a la de los mayores de 55 años (12,0%).

- En todas las comunidades autónomas sin excepción, la tasa de paro de las Mujeres supera a la de los Hombres. La brecha más amplia se observa en Castilla-La Mancha (32,99% vs 24,47%, una diferencia de más de 8 puntos porcentuales).

- La pandemia de 2020 generó un repunte visible en la serie temporal, aunque de menor magnitud que la crisis de 2008, y la recuperación posterior fue más rápida.

---

## 🔄 Próximos Pasos

- Incorporar datos de más comunidades autónomas (actualmente el dataset cubre solo las 10 más grandes).
- Ampliar el análisis con variables adicionales como nivel educativo o sector de actividad.
- Automatizar la actualización del dataset cada trimestre cuando el INE publique nuevos datos.
- Explorar la correlación entre la tasa de paro juvenil y indicadores educativos por comunidad.

---

## ✒️ Autores

- **Néstor Suárez Delgado**
- [@nestorsdelgado](https://github.com/nestorsdelgado)

---

## 📌 Fuente de los datos

Instituto Nacional de Estadística (INE) — Encuesta de Población Activa (EPA).
URL: [https://www.ine.es/jaxiT3/Datos.htm?t=65334](https://www.ine.es/jaxiT3/Datos.htm?t=65334)
