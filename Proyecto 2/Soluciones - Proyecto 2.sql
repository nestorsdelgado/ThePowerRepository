-- ============================================================================
-- 1. Crea el esquema de la BBDD.
-- ----------------------------------------------------------------------------
-- El esquema (tablas actor, film, category, film_actor, film_category, customer,
-- rental, payment, inventory, address, city, country, language, staff, store,
-- el tipo ENUM 'mpaa_rating' y el dominio 'year') se crea al ejecutar el volcado
-- proporcionado (BBDD_Proyecto_shakila_sinuser.sql). Para inspeccionarlo:
-- ============================================================================
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;


-- ============================================================================
-- 2. Nombres de todas las películas con clasificación por edades de 'R'.
-- ============================================================================
SELECT title
FROM film
WHERE rating = 'R';


-- ============================================================================
-- 3. Nombres de los actores con actor_id entre 30 y 40.
-- ============================================================================
SELECT actor_id, first_name, last_name
FROM actor
WHERE actor_id BETWEEN 30 AND 40;


-- ============================================================================
-- 4. Películas cuyo idioma coincide con el idioma original.
--    (En Pagila original_language_id es NULL en todas -> devuelve 0 filas.)
-- ============================================================================
SELECT title --, language_id , original_language_id 
FROM film
WHERE language_id = original_language_id;


-- ============================================================================
-- 5. Películas ordenadas por duración de forma ascendente.
-- ============================================================================
SELECT title, length
FROM film
ORDER BY length ASC;


-- ============================================================================
-- 6. Nombre y apellido de los actores que tengan 'Allen' en su apellido.
-- ============================================================================
SELECT first_name, last_name
FROM actor
WHERE last_name ILIKE '%allen%';


-- ============================================================================
-- 7. Cantidad total de películas en cada clasificación (rating).
-- ============================================================================
SELECT rating, COUNT(*) AS total_peliculas
FROM film
GROUP BY rating
ORDER BY rating;


-- ============================================================================
-- 8. Títulos que son 'PG-13' o tienen duración mayor a 3 horas (>180 min).
-- ============================================================================
SELECT title
FROM film
WHERE rating = 'PG-13' OR length > 180;


-- ============================================================================
-- 9. Variabilidad (varianza) de lo que costaría reemplazar las películas.
-- ============================================================================
SELECT VARIANCE(replacement_cost) AS varianza_reemplazo
FROM film;


-- ============================================================================
-- 10. Mayor y menor duración de una película.
-- ============================================================================
SELECT MAX(length) AS duracion_maxima,
       MIN(length) AS duracion_minima
FROM film;


-- ============================================================================
-- 11. Coste del antepenúltimo alquiler ordenado por día. (de cada día)
-- ============================================================================
WITH t AS (
    SELECT r.rental_id, r.rental_date, p.amount,
           ROW_NUMBER() OVER (PARTITION BY r.rental_date::date -- Para dividir las flas por día
                              ORDER BY r.rental_date DESC, r.rental_id DESC) AS pos_desde_final
    FROM rental r
    LEFT JOIN payment p ON p.rental_id = r.rental_id
) -- Ahora sabemos todas las películas alquiladas cada día de forma cronológica de última a primera
SELECT rental_date::date AS dia, rental_id, amount -- La información que queremos ver
FROM t
WHERE pos_desde_final = 3 -- el 3º empezando por el final = antepenúltimo
ORDER BY dia;


-- ============================================================================
-- 12. Títulos que NO sean ni 'NC-17' ni 'G'.
-- ============================================================================
SELECT title
FROM film
WHERE rating NOT IN ('NC-17', 'G');


-- ============================================================================
-- 13. Promedio de duración de las películas por clasificación (rating).
-- ============================================================================
SELECT rating, AVG(length) AS duracion_media
FROM film
GROUP BY rating
ORDER BY rating;


-- ============================================================================
-- 14. Títulos con duración mayor a 180 minutos.
-- ============================================================================
SELECT title
FROM film
WHERE length > 180;


-- ============================================================================
-- 15. ¿Cuánto dinero ha generado en total la empresa?
-- ============================================================================
SELECT SUM(amount) AS ingresos_totales
FROM payment;


-- ============================================================================
-- 16. Los 10 clientes con mayor valor de id.
-- ============================================================================
SELECT *
FROM customer
ORDER BY customer_id DESC
LIMIT 10;


-- ============================================================================
-- 17. Nombre y apellido de los actores de la película 'Egg Igby'.
-- ============================================================================
SELECT a.first_name, a.last_name
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN film f        ON fa.film_id = f.film_id
WHERE f.title = 'EGG IGBY';


-- ============================================================================
-- 18. Todos los nombres de películas únicos.
-- ============================================================================
SELECT DISTINCT title
FROM film;


-- ============================================================================
-- 19. Títulos que son comedias y duran más de 180 minutos.
-- ============================================================================
SELECT f.title
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c       ON fc.category_id = c.category_id
WHERE c.name = 'Comedy' AND f.length > 180;


-- ============================================================================
-- 20. Categorías con promedio de duración superior a 110 minutos.
-- ============================================================================
SELECT c.name, AVG(f.length) AS duracion_media
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f           ON fc.film_id = f.film_id
GROUP BY c.name
HAVING AVG(f.length) > 110
ORDER BY duracion_media DESC;


-- ============================================================================
-- 21. Media de duración del alquiler de las películas (rental_duration).
-- ============================================================================
SELECT AVG(rental_duration) AS media_duracion_alquiler
FROM film;


-- ============================================================================
-- 22. Columna con el nombre y apellidos de todos los actores/actrices.
-- ============================================================================
SELECT first_name || ' ' || last_name AS nombre_completo
FROM actor;


-- ============================================================================
-- 23. Número de alquileres por día, ordenados por cantidad descendente.
-- ============================================================================
SELECT rental_date::date AS dia, COUNT(*) AS num_alquileres
FROM rental
GROUP BY rental_date::date
ORDER BY num_alquileres DESC;


-- ============================================================================
-- 24. Películas con duración superior al promedio.
-- ============================================================================
SELECT title, length
FROM film
WHERE length > (SELECT AVG(length) FROM film)
ORDER BY length DESC;


-- ============================================================================
-- 25. Número de alquileres registrados por mes.
-- ============================================================================
SELECT TO_CHAR(rental_date, 'YYYY-MM') AS mes, COUNT(*) AS num_alquileres
FROM rental
GROUP BY TO_CHAR(rental_date, 'YYYY-MM')
ORDER BY mes;


-- ============================================================================
-- 26. Promedio, desviación estándar y varianza del total pagado.
-- ============================================================================
SELECT AVG(amount)      AS promedio,
       STDDEV(amount)   AS desviacion_estandar,
       VARIANCE(amount) AS varianza
FROM payment;


-- ============================================================================
-- 27. Películas que se alquilan por encima del precio medio (rental_rate).
-- ============================================================================
SELECT title, rental_rate
FROM film
WHERE rental_rate > (SELECT AVG(rental_rate) FROM film)
ORDER BY rental_rate DESC;


-- ============================================================================
-- 28. IDs de actores que han participado en más de 40 películas.
-- ============================================================================
SELECT actor_id, COUNT(*) AS num_peliculas
FROM film_actor
GROUP BY actor_id
HAVING COUNT(*) > 40
ORDER BY num_peliculas DESC;


-- ============================================================================
-- 29. Todas las películas y, si están en inventario, su cantidad disponible.
-- ============================================================================
SELECT f.title, COUNT(i.inventory_id) AS cantidad_disponible
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
GROUP BY f.film_id, f.title
ORDER BY f.title;


-- ============================================================================
-- 30. Actores y número de películas en las que han actuado.
-- ============================================================================
SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS num_peliculas
FROM actor a
LEFT JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id, a.first_name, a.last_name
ORDER BY num_peliculas DESC;


-- ============================================================================
-- 31. Todas las películas y sus actores (incluso películas sin actores).
-- ============================================================================
SELECT f.title, a.first_name, a.last_name
FROM film f
LEFT JOIN film_actor fa ON f.film_id = fa.film_id
LEFT JOIN actor a       ON fa.actor_id = a.actor_id
ORDER BY f.title;


-- ============================================================================
-- 32. Todos los actores y sus películas (incluso actores sin películas).
-- ============================================================================
SELECT a.first_name, a.last_name, f.title
FROM actor a
LEFT JOIN film_actor fa ON a.actor_id = fa.actor_id
LEFT JOIN film f        ON fa.film_id = f.film_id
ORDER BY a.last_name, a.first_name;


-- ============================================================================
-- 33. Todas las películas y todos los registros de alquiler (FULL OUTER JOIN).
-- ============================================================================
SELECT f.title, r.rental_id, r.rental_date
FROM film f
FULL OUTER JOIN inventory i ON f.film_id = i.film_id
FULL OUTER JOIN rental r    ON i.inventory_id = r.inventory_id
ORDER BY f.film_id DESC; -- Para ver más fácilmente todos los registros por película


-- ============================================================================
-- 34. Los 5 clientes que más dinero se han gastado.
-- ============================================================================
SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) AS total_gastado
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_gastado DESC
LIMIT 5;


-- ============================================================================
-- 35. Actores cuyo primer nombre es 'Johnny'.
-- ============================================================================
SELECT *
FROM actor
WHERE first_name = 'JOHNNY';


-- ============================================================================
-- 36. Renombra first_name como Nombre y last_name como Apellido.
-- ============================================================================
SELECT first_name AS "Nombre", last_name AS "Apellido" -- Entre comillas para que no se quede en minúscula
FROM actor;


-- ============================================================================
-- 37. ID del actor más bajo y más alto.
-- ============================================================================
SELECT MIN(actor_id) AS id_minimo, MAX(actor_id) AS id_maximo
FROM actor;


-- ============================================================================
-- 38. Cuántos actores hay en la tabla actor.
-- ============================================================================
SELECT COUNT(*) AS total_actores
FROM actor;


-- ============================================================================
-- 39. Actores ordenados por apellido de forma ascendente.
-- ============================================================================
SELECT *
FROM actor
ORDER BY last_name ASC;


-- ============================================================================
-- 40. Primeras 5 películas de la tabla film.
-- ============================================================================
SELECT *
FROM film
ORDER BY film_id
LIMIT 5;


-- ============================================================================
-- 41. Agrupa actores por nombre y cuenta. ¿Cuál es el más repetido?
--     Respuesta: hay un triple empate -> PENELOPE, KENNETH y JULIA (4 cada uno).
-- ============================================================================
SELECT first_name, COUNT(*) AS repeticiones
FROM actor
GROUP BY first_name
ORDER BY repeticiones DESC, first_name;


-- ============================================================================
-- 42. Todos los alquileres y los nombres de los clientes que los realizaron.
-- ============================================================================
SELECT r.rental_id, r.rental_date, c.first_name, c.last_name
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id;


-- ============================================================================
-- 43. Todos los clientes y sus alquileres, incluyendo los que no tienen.
-- ============================================================================
SELECT c.customer_id, c.first_name, c.last_name, r.rental_id
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id;


-- ============================================================================
-- 44. CROSS JOIN entre film y category. ¿Aporta valor? ¿Por qué?
-- ----------------------------------------------------------------------------
-- Respuesta: NO aporta valor. Un CROSS JOIN produce el producto cartesiano
-- (1000 películas x 16 categorías = 16.000 filas), emparejando cada película
-- con TODAS las categorías, incluidas las que no le corresponden. La relación
-- real película-categoría está modelada en la tabla puente 'film_category',
-- que es la que debe usarse (con INNER JOIN) para obtener datos con sentido.
-- ============================================================================
SELECT f.title, c.name
FROM film f
CROSS JOIN category c;


-- ============================================================================
-- 45. Actores que han participado en películas de la categoría 'Action'.
-- ============================================================================
SELECT DISTINCT a.actor_id, a.first_name, a.last_name
FROM actor a
JOIN film_actor fa    ON a.actor_id = fa.actor_id
JOIN film_category fc ON fa.film_id = fc.film_id
JOIN category c       ON fc.category_id = c.category_id
WHERE c.name = 'Action'
ORDER BY a.last_name;


-- ============================================================================
-- 46. Actores que NO han participado en ninguna película.
-- ============================================================================
SELECT a.actor_id, a.first_name, a.last_name
FROM actor a
WHERE a.actor_id NOT IN (SELECT actor_id FROM film_actor);


-- ============================================================================
-- 47. Nombre de los actores y cantidad de películas en que han participado.
-- ============================================================================
SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS num_peliculas
FROM actor a
LEFT JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id, a.first_name, a.last_name
ORDER BY num_peliculas DESC;


-- ============================================================================
-- 48. Vista 'actor_num_peliculas': nombres + nº de películas por actor.
-- ============================================================================
DROP VIEW IF EXISTS actor_num_peliculas;
CREATE VIEW actor_num_peliculas AS
SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS num_peliculas
FROM actor a
LEFT JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id, a.first_name, a.last_name;

-- Comprobación:
SELECT * FROM actor_num_peliculas ORDER BY num_peliculas DESC LIMIT 5;


-- ============================================================================
-- 49. Número total de alquileres realizados por cada cliente.
-- ============================================================================
SELECT customer_id, COUNT(*) AS total_alquileres
FROM rental
GROUP BY customer_id
ORDER BY total_alquileres DESC;


-- ============================================================================
-- 50. Duración total de las películas en la categoría 'Action'.
-- ============================================================================
SELECT SUM(f.length) AS duracion_total
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c       ON fc.category_id = c.category_id
WHERE c.name = 'Action';


-- ============================================================================
-- 51. Tabla temporal 'cliente_rentas_temporal': total de alquileres por cliente.
-- ============================================================================
DROP TABLE IF EXISTS cliente_rentas_temporal;
CREATE TEMP TABLE cliente_rentas_temporal AS
SELECT customer_id, COUNT(*) AS total_alquileres
FROM rental
GROUP BY customer_id;

SELECT * FROM cliente_rentas_temporal ORDER BY total_alquileres DESC LIMIT 5;


-- ============================================================================
-- 52. Tabla temporal 'peliculas_alquiladas': películas alquiladas >= 10 veces.
-- ============================================================================
DROP TABLE IF EXISTS peliculas_alquiladas;
CREATE TEMP TABLE peliculas_alquiladas AS
SELECT f.film_id, f.title, COUNT(r.rental_id) AS veces_alquilada
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r    ON i.inventory_id = r.inventory_id
GROUP BY f.film_id, f.title
HAVING COUNT(r.rental_id) >= 10;

SELECT * FROM peliculas_alquiladas ORDER BY veces_alquilada DESC LIMIT 5;


-- ============================================================================
-- 53. Películas alquiladas por 'Tammy Sanders' aún no devueltas (orden alfab.).
-- ============================================================================
SELECT DISTINCT f.title
FROM customer c
JOIN rental r    ON c.customer_id = r.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f      ON i.film_id = f.film_id
WHERE c.first_name = 'TAMMY' AND c.last_name = 'SANDERS'
  AND r.return_date IS NULL
ORDER BY f.title;


-- ============================================================================
-- 54. Actores en >=1 película de categoría 'Sci-Fi' (orden por apellido).
-- ============================================================================
SELECT DISTINCT a.first_name, a.last_name
FROM actor a
JOIN film_actor fa    ON a.actor_id = fa.actor_id
JOIN film_category fc ON fa.film_id = fc.film_id
JOIN category c       ON fc.category_id = c.category_id
WHERE c.name = 'Sci-Fi'
ORDER BY a.last_name;


-- ============================================================================
-- 55. Actores de películas alquiladas DESPUÉS del primer alquiler de
--     'Spartacus Cheaper' (orden por apellido).
-- ============================================================================
SELECT DISTINCT a.first_name, a.last_name
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN inventory i   ON fa.film_id = i.film_id
JOIN rental r      ON i.inventory_id = r.inventory_id
WHERE r.rental_date > (
        SELECT MIN(r2.rental_date)
        FROM rental r2
        JOIN inventory i2 ON r2.inventory_id = i2.inventory_id
        JOIN film f2      ON i2.film_id = f2.film_id
        WHERE f2.title = 'SPARTACUS CHEAPER'
)
ORDER BY a.last_name;


-- ============================================================================
-- 56. Actores que NO han actuado en ninguna película de categoría 'Music'.
-- ============================================================================
SELECT a.first_name, a.last_name
FROM actor a
WHERE a.actor_id NOT IN (
        SELECT fa.actor_id
        FROM film_actor fa
        JOIN film_category fc ON fa.film_id = fc.film_id
        JOIN category c       ON fc.category_id = c.category_id
        WHERE c.name = 'Music'
)
ORDER BY a.last_name;


-- ============================================================================
-- 57. Títulos alquilados por más de 8 días (return_date - rental_date > 8 días).
-- ============================================================================
SELECT DISTINCT f.title
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r    ON i.inventory_id = r.inventory_id
WHERE r.return_date - r.rental_date > INTERVAL '8 days'
ORDER BY f.title;


-- ============================================================================
-- 58. Títulos las pelúclas de la categoría 'Animation'.
-- ============================================================================
SELECT f.title
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c       ON fc.category_id = c.category_id
WHERE c.name = 'Animation'
ORDER BY f.title;


-- ============================================================================
-- 59. Películas con la misma duración que 'Dancing Fever' (orden por título).
-- ============================================================================
SELECT title, length
FROM film
WHERE length = (SELECT length FROM film WHERE title = 'DANCING FEVER')
  AND title <> 'DANCING FEVER'
ORDER BY title;


-- ============================================================================
-- 60. Clientes con al menos 7 películas distintas alquiladas (orden apellido).
-- ============================================================================
SELECT c.first_name, c.last_name, COUNT(DISTINCT i.film_id) AS peliculas_distintas
FROM customer c
JOIN rental r    ON c.customer_id = r.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(DISTINCT i.film_id) >= 7
ORDER BY c.last_name;


-- ============================================================================
-- 61. Cantidad total de películas alquiladas por categoría (recuento alquileres).
-- ============================================================================
SELECT c.name, COUNT(r.rental_id) AS total_alquileres
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN inventory i      ON fc.film_id = i.film_id
JOIN rental r         ON i.inventory_id = r.inventory_id
GROUP BY c.name
ORDER BY total_alquileres DESC;


-- ============================================================================
-- 62. Número de películas por categoría estrenadas en 2006.
-- ============================================================================
SELECT c.name, COUNT(*) AS num_peliculas
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c       ON fc.category_id = c.category_id
WHERE f.release_year = 2006
GROUP BY c.name
ORDER BY num_peliculas DESC;


-- ============================================================================
-- 63. Todas las combinaciones posibles de trabajadores con las tiendas.
-- ============================================================================
SELECT s.staff_id, s.first_name, s.last_name, st.store_id
FROM staff s
CROSS JOIN store st;


-- ============================================================================
-- 64. Cantidad total de películas alquiladas por cada cliente
--     (id, nombre, apellido, cantidad).
-- ============================================================================
SELECT c.customer_id, c.first_name, c.last_name, COUNT(r.rental_id) AS peliculas_alquiladas
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY peliculas_alquiladas DESC;

