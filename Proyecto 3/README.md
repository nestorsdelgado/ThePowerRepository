# PROYECTO LÓGICA: Katas de Python

Resolución de las katas. El objetivo es demostrar el manejo de los conceptos fundamentales resolviendo 41 ejercicios.

## Estructura del repositorio

| Archivo | Descripción |
|---------|-------------|
| `katas_python.py` | Todas las katas resueltas. Cada ejercicio va encabezado por un comentario con su enunciado, seguido de la solución y, al final del archivo, su caso de uso. |
| `katas.ipynb` | Todas las katas resueltas pero usando el Notebook como en clase. |
| `README.md` | Este documento, con la descripción del proyecto y los pasos seguidos. |

> Nota sobre la numeración: el enunciado numera los ejercicios del 1 al 41 pero
> **no incluye un ejercicio 35** (pasa directamente del 34 al 36). En el código se
> respeta esa numeración para que coincida exactamente con el PDF del enunciado.

## Cómo ejecutarlo

```bash
python3 katas_python.py
```

Al ejecutarse, el archivo imprime por terminal el resultado (caso de uso) de
cada kata. El código está organizado en dos partes:

1. **Definiciones**: todas las funciones, lambdas y clases.
2. **Casos de uso**: dentro del bloque `if __name__ == "__main__":`, donde se
   llama a cada solución con datos de ejemplo.

### Por qué los casos de uso van al final, en un bloque `if __name__ == "__main__":`

Conviene separar el código que **define** la lógica (funciones, lambdas y
clases) del código que la **ejecuta** (las llamadas de ejemplo). El motivo es la
reutilización: si otro archivo quisiera importar una función de aquí, Python ejecutaría de golpe todos
los `print` y demostraciones durante la importación, lo cual no es deseable.

El bloque `if __name__ == "__main__":` evita eso. `__name__` es una variable que
Python rellena automáticamente: vale `"__main__"` **solo cuando el archivo se
ejecuta directamente** (`python3 katas_python.py`), y vale el nombre del módulo
(`"katas_python"`) cuando el archivo se importa desde otro sitio.

### Por qué las funciones con `input()` aparecen comentadas

Los ejercicios que piden datos por teclado con `input()` (los números **8, 11,
31 y 41**) están definidos como funciones y su **llamada** aparece **comentada**
en el bloque principal.

La razón es que `input()` pausa el programa y espera a que el usuario escriba
algo y pulse Enter. Como el bloque de casos de uso se ejecuta entero de arriba a
abajo, si esas llamadas estuvieran activas, el programa se **congelaría** en cada
una esperando datos, y no se verían los demás resultados hasta responder a mano.
Dejándolas comentadas, el archivo se ejecuta completo de una sola vez y muestra
limpiamente todas las katas que no necesitan interacción.

## Pasos seguidos durante el proyecto

1. **Lectura y análisis del enunciado**: se identificó qué concepto pone a
   prueba cada kata (tipos de datos, estructuras, condicionales, iteración,
   funciones, clases, módulos o manejo de errores).
2. **Elección del enfoque**: aunque muchas katas pueden resolverse de varias
   formas, se eligió en cada caso la herramienta que el propio enunciado sugería
   (`map()`, `filter()`, `reduce()`, `lambda`) o la más legible.
3. **Implementación**: cada solución se escribió como una función, lambda o
   clase y con comentarios en los pasos más complejos.
4. **Verificación**: se ejecutó el archivo completo comprobando que la salida de
   cada caso de uso coincide con lo esperado.
5. **Documentación**: redacción de este README.

## Conceptos demostrados

- **Tipos de datos básicos y funciones incorporadas**: uso de `len()`, `sum()`,
  `sorted()`, `str()`, `type()`, `round()`, indexación y *slicing*.

- **Estructuras de datos y sus métodos**: listas, diccionarios (`.get()`,
  `.items()`), conjuntos (`set` para eliminar duplicados) y tuplas.

- **Condicionales**: `if` / `elif` / `else` y el operador ternario.

- **Estructuras de iteración**: bucles `for`, *list comprehensions* y funciones
  de orden superior (`map`, `filter`, `reduce`).

- **Funciones**: parámetros por defecto (kata 5), argumentos variables `*args`
  (kata 37), recursividad (kata 6) y funciones `lambda`.
  
- **Clases y POO**: definición de clases, constructor `__init__`, atributos y
  métodos.

- **Uso de módulos**: `functools.reduce` y `math`.

- **Manejo de errores**: bloques `try` / `except` / `else` / `finally` y una
  excepción personalizada (`ListaVaciaError`).
  

## Buenas prácticas aplicadas

- `import` de módulos agrupados al principio del archivo.
- Nombres de variables y funciones descriptivos y en español, coherentes en
  todo el proyecto.
- Docstrings en las funciones y comentarios explicativos en los pasos menos
  evidentes.
- Separación entre la **definición** de la lógica y su **demostración** mediante
  el bloque `if __name__ == "__main__":`.
- Validaciones defensivas (por ejemplo, comprobar que una posición existe antes
  de eliminar una rama, o que la lista no está vacía antes de calcular la media).
