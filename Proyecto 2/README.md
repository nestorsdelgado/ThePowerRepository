# DataProject: Lógica de Consultas SQL

Proyecto de consultas SQL sobre la base de datos **Pagila** (la versión para PostgreSQL de la clásica *Sakila*), que usa como ejemplo el negocio de una empresa de alquiler de películas con dos tiendas.

---

## Pasos seguidos durante el proyecto

### 1. Crear la base de datos a partir del archivo proporcionado

Se partió del volcado `BBDD_Proyecto_shakila_sinuser.sql`. Se creó una base de datos  vacía y usando el archivo descargado se cargó toda la información, que genera todo el esquema (tablas, tipos y relaciones) y rellena los datos.

### 2. Entender la base de datos

Antes de resolver nada, se exploró la estructura para saber con qué se trabajaba: **15 tablas** organizadas en tres bloques —catálogo de películas (`film`, `category`, `actor` y sus tablas puente `film_category` y `film_actor`), operativa de alquiler (`inventory`, `rental`, `payment`) y localización (`customer`, `store`, `staff`, `address`, `city`, `country`)— y las claves foráneas que las conectan. Se verificó que la carga fuese correcta:

```sql
SELECT count(*) FROM actor;    -- 200
SELECT count(*) FROM film;     -- 1000
SELECT count(*) FROM rental;   -- 16044
```

### 3. Resolver los 64 enunciados

Se resolvieron los 64 ejercicios (filtros, agregaciones, todos los tipos de `JOIN`, subconsultas, vistas, tablas temporales y funciones de ventana). Cada consulta se **ejecutó contra la base real** para validar su resultado, no solo su sintaxis.

---

## Informe de análisis

Todas las cifras proceden de ejecutar consultas de agregación sobre la base cargada.

### Volumen del negocio

| Métrica | Valor |
|---|---|
| Clientes | 599 |
| Alquileres registrados | 16.044 |
| Pagos registrados | 16.049 |
| **Ingresos totales** | **67.416,51 €** |
| Ticket medio por pago | 4,20 € |
| Rango de importe por pago | 0,00 € – 11,99 € |
| Tiendas / empleados | 2 / 2 |

Es un negocio pequeño (dos tiendas, dos empleados) con un ticket medio muy bajo.

### Catálogo

| Métrica | Valor |
|---|---|
| Películas | 1.000 |
| Categorías | 16 |
| Duración (min – media – máx) | 46 – 115,3 – 185 min |
| Tarifas de alquiler | solo 3 precios: 0,99 € / 2,99 € / 4,99 € |
| Coste medio de reposición | 19,98 € |

**Reparto por clasificación de edad (rating):**

| Rating | Películas |
|---|---|
| PG-13 | 223 |
| NC-17 | 210 |
| R | 195 |
| PG | 194 |
| G | 178 |

**Observación sobre la naturaleza de los datos:** el catálogo es de **1.000 películas del año 2006 y están en inglés** (`language_id = 1`), aunque la tabla `language` contiene 6 idiomas (inglés, italiano, japonés, mandarín, francés y alemán): los otros cinco existen en el catálogo pero ninguna película los usa. Además, `original_language_id` es **NULL en el 100 %** de las películas. Por tanto, cualquier análisis por idioma o por año de estreno carece de recorrido en esta base.

### Demanda y estacionalidad

Los alquileres se concentran de forma muy marcada en el **verano de 2005**:

| Mes | Alquileres |
|---|---|
| 2005-05 | 1.156 |
| 2005-06 | 2.311 |
| 2005-07 | **6.709** |
| 2005-08 | 5.686 |
| 2006-02 | 182 |

La actividad arranca en mayo de 2005, alcanza su pico en julio-agosto y luego hay un salto hasta febrero de 2006 con apenas 182 registros (una "cola" de datos, en su mayoría alquileres aún sin devolver).

**Categorías más alquiladas:** la demanda está muy repartida; las cinco primeras se diferencian por muy poco.

| Categoría | Alquileres |
|---|---|
| Sports | 1.179 |
| Animation | 1.166 |
| Action | 1.112 |
| Sci-Fi | 1.101 |
| Family | 1.096 |

**Películas más alquiladas:** *Bucket Brotherhood* (34), *Rocketeer Mother* (33), *Ridgemont Submarine*, *Scalawag Duck* y *Forward Temple* (32 cada una).

### Clientes

Los cinco clientes de mayor gasto acumulan importes moderados y sin valores extremos (el primero gasta poco más que el quinto).

| Cliente | Gasto total |
|---|---|
| Karl Seal | 221,55 € |
| Eleanor Hunt | 216,54 € |
| Clara Shaw | 195,58 € |
| Rhonda Kennedy | 194,61 € |
| Marion Snyder | 194,61 € |

### Inventario y reparto

- Cada película está representada por varias **copias físicas** (4.581 copias para 1.000 títulos). El camino `film → inventory → rental` es lo que hace que una película popular aparezca en decenas de alquileres.
- **42 películas no tienen ninguna copia** en inventario: existen en el catálogo pero nunca han podido alquilarse. Además, hay **1 copia que nunca se ha alquilado**.
- **Reparto:** cada actor ha participado en entre **14 y 42 películas** (media 27,3). No hay ningún actor sin películas.

### Conclusión

Los datos reflejan una empresa de alquiler de películas pequeña, un catálogo general tanto en clasificación de edad como en demanda por género, y una base de clientes homogénea (artificial) para la práctica de este proyecto.