"""
============================================================
PROYECTO LÓGICA: Katas de Python
============================================================
Soluciones a las katas del proyecto.

Estructura del archivo:
    - Cada ejercicio va encabezado por un comentario con su enunciado.
    - Primero se define la función / lambda / clase.
    - Al final del archivo (bloque if __name__ == "__main__") están las
      demostraciones (casos de uso) de cada ejercicio.
    - Los ejercicios que requieren input() del usuario se dejan definidos
      como funciones y su llamada aparece comentada en el bloque principal,
      para que el archivo pueda ejecutarse de principio a fin sin bloquearse
      esperando datos por teclado.

Nota: el enunciado numera los ejercicios del 1 al 41 pero salta el número 35
      (pasa del 34 al 36). Se respeta esa numeración para que coincida con el PDF.
"""

# ------------------------------------------------------------
# Módulos utilizados en todo el archivo (buena práctica: imports arriba)
# ------------------------------------------------------------
from functools import reduce   # Necesario para los ejercicios con reduce()
import math                    # Necesario para el área del círculo (pi)


# ============================================================
# EJERCICIO 1
# Escribe una función que reciba una cadena de texto como parámetro y
# devuelva un diccionario con las frecuencias de cada letra en la cadena.
# Los espacios no deben ser considerados.
# ============================================================
def frecuencia_letras(cadena):
    """
    Cuenta cuántas veces aparece cada letra en una cadena.

    Args:
        cadena (str): Texto a analizar.

    Returns:
        dict: Diccionario {letra: frecuencia} sin contar los espacios.
    """
    frecuencias = {}
    for letra in cadena:
        # Ignoramos los espacios en blanco
        if letra != " ":
            # get(letra, 0) devuelve el valor actual o 0 si la letra es nueva
            frecuencias[letra] = frecuencias.get(letra, 0) + 1
    return frecuencias


# ============================================================
# EJERCICIO 2
# Dada una lista de números, obtén una nueva lista con el doble de cada valor.
# Usa la función map().
# ============================================================
def doblar_valores(lista):
    """Devuelve una nueva lista con el doble de cada número usando map()."""
    return list(map(lambda x: x * 2, lista))


# ============================================================
# EJERCICIO 3
# Escribe una función que tome una lista de palabras y una palabra objetivo.
# Debe devolver una lista con todas las palabras que contengan la palabra objetivo.
# ============================================================
def palabras_que_contienen(lista_palabras, objetivo):
    """
    Filtra las palabras que contienen 'objetivo' como subcadena.

    Args:
        lista_palabras (list): Lista de palabras.
        objetivo (str): Texto que debe estar contenido en la palabra.

    Returns:
        list: Palabras que contienen el objetivo.
    """
    # 'in' comprueba si 'objetivo' aparece dentro de cada palabra
    return [palabra for palabra in lista_palabras if objetivo in palabra]


# ============================================================
# EJERCICIO 4
# Genera una función que calcule la diferencia entre los valores de dos listas.
# Usa la función map().
# ============================================================
def diferencia_listas(lista1, lista2):
    """
    Resta elemento a elemento dos listas.
    map() puede recibir varios iterables; la lambda recibe un elemento de cada uno.
    """
    return list(map(lambda x, y: x - y, lista1, lista2))


# ============================================================
# EJERCICIO 5
# Escribe una función que tome una lista de números y un valor opcional
# nota_aprobado (por defecto 5). Calcula la media y determina si es
# "aprobado" (media >= nota_aprobado) o "suspenso". Devuelve una tupla (media, estado).
# ============================================================
def evaluar_media(lista, nota_aprobado=5):
    """
    Calcula la media de una lista y determina el estado (aprobado/suspenso).

    Returns:
        tuple: (media, estado)
    """
    media = sum(lista) / len(lista)
    # Operador ternario: valor_si_verdadero if condicion else valor_si_falso
    estado = "aprobado" if media >= nota_aprobado else "suspenso"
    return (media, estado)


# ============================================================
# EJERCICIO 6
# Escribe una función que calcule el factorial de un número de manera recursiva.
# ============================================================
def factorial(n):
    """
    Calcula el factorial de n de forma recursiva.
    El caso base (n == 0 o n == 1) detiene la recursividad.
    """
    if n == 0 or n == 1:
        return 1
    # La función se llama a sí misma con un número menor hasta llegar al caso base
    return n * factorial(n - 1)


# ============================================================
# EJERCICIO 7
# Genera una función que convierta una lista de tuplas a una lista de strings.
# Usa la función map().
# ============================================================
def tuplas_a_strings(lista_tuplas):
    """
    Convierte cada tupla en un string uniendo sus elementos con un espacio.
    Ejemplo: [("Juan", "Garcia")] -> ["Juan Garcia"]
    """
    # map interno: convierte cada elemento de la tupla a str
    # join: los une en una sola cadena
    return list(map(lambda tupla: " ".join(map(str, tupla)), lista_tuplas))


# ============================================================
# EJERCICIO 8
# Escribe un programa que pida al usuario dos números e intente dividirlos.
# Maneja las excepciones (valor no numérico o división por cero) y muestra
# un mensaje indicando si la división fue exitosa o no.
# ============================================================
def dividir_dos_numeros():
    """Pide dos números por teclado y los divide gestionando errores."""
    try:
        num1 = float(input("Introduce el primer número: "))
        num2 = float(input("Introduce el segundo número: "))
        resultado = num1 / num2
    except ValueError:
        # Salta si el usuario no introduce un número
        print("Error: debes introducir valores numéricos. La división no fue exitosa.")
    except ZeroDivisionError:
        # Salta si el segundo número es 0
        print("Error: no se puede dividir entre cero. La división no fue exitosa.")
    else:
        # Solo se ejecuta si no hubo ninguna excepción
        print(f"La división fue exitosa. Resultado: {round(resultado, 2)}")


# ============================================================
# EJERCICIO 9
# Escribe una función que tome una lista de nombres de mascotas y devuelva
# una nueva lista excluyendo las mascotas prohibidas en España. Usa filter().
# ============================================================
def filtrar_mascotas(lista_mascotas):
    """Devuelve las mascotas que NO están en la lista de prohibidas."""
    prohibidas = ["Mapache", "Tigre", "Serpiente Pitón", "Cocodrilo", "Oso"]
    # filter conserva solo los elementos para los que la lambda devuelve True
    return list(filter(lambda mascota: mascota not in prohibidas, lista_mascotas))


# ============================================================
# EJERCICIO 10
# Escribe una función que reciba una lista de números y calcule su promedio.
# Si la lista está vacía, lanza una excepción personalizada y maneja el error.
# ============================================================
class ListaVaciaError(Exception):
    """Excepción personalizada que se lanza cuando la lista está vacía."""
    pass


def calcular_promedio_seguro(lista):
    """
    Calcula el promedio de una lista.
    Lanza ListaVaciaError si la lista no tiene elementos.
    """
    if len(lista) == 0:
        raise ListaVaciaError("La lista está vacía, no se puede calcular el promedio.")
    return sum(lista) / len(lista)


# ============================================================
# EJERCICIO 11
# Escribe un programa que pida al usuario su edad. Si introduce un valor no
# numérico o fuera de rango (menor que 0 o mayor que 120), maneja las excepciones.
# ============================================================
def pedir_edad():
    """Pide la edad por teclado y valida que sea un número dentro de rango."""
    try:
        edad = int(input("Introduce tu edad: "))
        # Si está fuera de rango, lanzamos manualmente un ValueError
        if edad < 0 or edad > 120:
            raise ValueError("la edad debe estar entre 0 y 120.")
    except ValueError as error:
        # Captura tanto el error de conversión como el que lanzamos nosotros
        print(f"Entrada no válida: {error}")
    else:
        print(f"Tu edad es: {edad} años.")


# ============================================================
# EJERCICIO 12
# Genera una función que al recibir una frase devuelva una lista con la
# longitud de cada palabra. Usa la función map().
# ============================================================
def longitud_palabras(frase):
    """Devuelve la longitud de cada palabra de la frase."""
    # split() separa la frase en palabras; len calcula la longitud de cada una
    return list(map(len, frase.split()))


# ============================================================
# EJERCICIO 13
# Genera una función que, para un conjunto de caracteres, devuelva una lista de
# tuplas con cada letra en mayúsculas y minúsculas. Sin letras repetidas. Usa map().
# ============================================================
def mayusculas_minusculas(caracteres):
    """
    Para cada letra única devuelve una tupla (MAYÚSCULA, minúscula).
    Usamos un set para eliminar las letras repetidas.
    """
    # Pasamos a minúsculas y convertimos a set para quitar duplicados
    letras_unicas = set(caracteres.lower())
    return list(map(lambda letra: (letra.upper(), letra.lower()), letras_unicas))


# ============================================================
# EJERCICIO 14
# Crea una función que retorne las palabras de una lista que comiencen con una
# letra específica. Usa la función filter().
# ============================================================
def palabras_con_letra(lista_palabras, letra):
    """Devuelve las palabras que empiezan por la letra indicada."""
    # startswith devuelve True si la palabra empieza por 'letra'
    return list(filter(lambda palabra: palabra.startswith(letra), lista_palabras))


# ============================================================
# EJERCICIO 15
# Crea una función lambda que sume 3 a cada número de una lista dada.
# ============================================================
# La lambda recibe la lista y aplica un map que suma 3 a cada elemento
sumar_tres = lambda lista: list(map(lambda x: x + 3, lista))


# ============================================================
# EJERCICIO 16
# Escribe una función que tome una cadena de texto y un número entero n y
# devuelva una lista con todas las palabras más largas que n. Usa filter().
# ============================================================
def palabras_mas_largas(texto, n):
    """Devuelve las palabras del texto cuya longitud es mayor que n."""
    return list(filter(lambda palabra: len(palabra) > n, texto.split()))


# ============================================================
# EJERCICIO 17
# Crea una función que tome una lista de dígitos y devuelva el número
# correspondiente. Por ejemplo [5,7,2] -> 572. Usa la función reduce().
# ============================================================
def digitos_a_numero(digitos):
    """
    Convierte una lista de dígitos en el número que representan.
    En cada paso: acumulado * 10 + nuevo_dígito
    [5,7,2] -> 5 -> 5*10+7=57 -> 57*10+2=572
    """
    return reduce(lambda acumulado, digito: acumulado * 10 + digito, digitos)


# ============================================================
# EJERCICIO 18
# Crea una lista de diccionarios con información de estudiantes (nombre, edad,
# calificación) y usa filter para extraer los que tengan calificación >= 90.
# ============================================================
def estudiantes_sobresalientes(estudiantes):
    """Filtra los estudiantes cuya calificación es mayor o igual a 90."""
    return list(filter(lambda est: est["calificacion"] >= 90, estudiantes))


# ============================================================
# EJERCICIO 19
# Crea una función lambda que filtre los números impares de una lista dada.
# ============================================================
# Un número es impar si el resto de dividir entre 2 es distinto de 0
filtrar_impares = lambda lista: list(filter(lambda x: x % 2 != 0, lista))


# ============================================================
# EJERCICIO 20
# Para una lista con elementos tipo integer y string, obtén una nueva lista
# solo con los valores int. Usa la función filter().
# ============================================================
def solo_enteros(lista):
    """Devuelve solo los elementos de tipo entero de la lista."""
    # type(x) == int evita que los booleanos (que también son int) cuelen
    return list(filter(lambda x: type(x) == int, lista))


# ============================================================
# EJERCICIO 21
# Crea una función que calcule el cubo de un número dado mediante una lambda.
# ============================================================
cubo = lambda x: x ** 3


# ============================================================
# EJERCICIO 22
# Dada una lista numérica, obtén el producto total de sus valores. Usa reduce().
# ============================================================
def producto_total(lista):
    """Multiplica todos los elementos de la lista entre sí."""
    return reduce(lambda x, y: x * y, lista)


# ============================================================
# EJERCICIO 23
# Concatena una lista de palabras. Usa la función reduce().
# ============================================================
def concatenar_palabras(lista):
    """Une todas las palabras de la lista separándolas por un espacio."""
    return reduce(lambda x, y: x + " " + y, lista)


# ============================================================
# EJERCICIO 24
# Calcula la diferencia total en los valores de una lista. Usa reduce().
# ============================================================
def diferencia_total(lista):
    """Va restando cada elemento al resultado acumulado: ((a-b)-c)-..."""
    return reduce(lambda x, y: x - y, lista)


# ============================================================
# EJERCICIO 25
# Crea una función que cuente el número de caracteres en una cadena de texto.
# ============================================================
def contar_caracteres(cadena):
    """Devuelve el número total de caracteres de la cadena."""
    return len(cadena)


# ============================================================
# EJERCICIO 26
# Crea una función lambda que calcule el resto de la división entre dos números.
# ============================================================
resto_division = lambda x, y: x % y


# ============================================================
# EJERCICIO 27
# Crea una función que calcule el promedio de una lista de números.
# ============================================================
def promedio(lista):
    """Calcula la media aritmética de una lista de números."""
    return sum(lista) / len(lista)


# ============================================================
# EJERCICIO 28
# Crea una función que busque y devuelva el primer elemento duplicado en una lista.
# ============================================================
def primer_duplicado(lista):
    """
    Devuelve el primer elemento que se repite recorriendo la lista de izquierda
    a derecha. Usamos un set para recordar los elementos ya vistos (búsqueda rápida).
    """
    vistos = set()
    for elemento in lista:
        # Si ya lo habíamos visto, es el primer duplicado
        if elemento in vistos:
            return elemento
        vistos.add(elemento)
    return None  # No hay duplicados


# ============================================================
# EJERCICIO 29
# Crea una función que convierta una variable en cadena de texto y enmascare
# todos los caracteres con '#', excepto los últimos cuatro.
# ============================================================
def enmascarar(variable):
    """
    Enmascara con '#' todos los caracteres menos los 4 últimos.
    Ejemplo: 1234567890 -> ######7890
    """
    texto = str(variable)
    # Si tiene 4 caracteres o menos, no hay nada que enmascarar
    if len(texto) <= 4:
        return texto
    # '#' repetido tantas veces como caracteres haya que ocultar + los 4 últimos
    return "#" * (len(texto) - 4) + texto[-4:]


# ============================================================
# EJERCICIO 30
# Crea una función que determine si dos palabras son anagramas (mismas letras
# en distinto orden).
# ============================================================
def son_anagramas(palabra1, palabra2):
    """
    Dos palabras son anagramas si, ordenando sus letras, coinciden.
    Pasamos a minúsculas para que la comparación no distinga mayúsculas.
    """
    return sorted(palabra1.lower()) == sorted(palabra2.lower())


# ============================================================
# EJERCICIO 31
# Crea una función que solicite al usuario ingresar una lista de nombres y luego
# un nombre para buscar. Si está, imprime un mensaje; si no, lanza una excepción.
# ============================================================
def buscar_nombre_en_lista():
    """Pide una lista de nombres y busca uno en ella."""
    entrada = input("Introduce varios nombres separados por comas: ")
    # Separamos por comas y quitamos espacios sobrantes de cada nombre
    nombres = [nombre.strip() for nombre in entrada.split(",")]
    buscado = input("¿Qué nombre quieres buscar? ").strip()

    if buscado in nombres:
        print(f"El nombre '{buscado}' fue encontrado en la lista.")
    else:
        # Lanzamos una excepción si no se encuentra
        raise ValueError(f"El nombre '{buscado}' no está en la lista.")


# ============================================================
# EJERCICIO 32
# Crea una función que tome un nombre completo y una lista de empleados, busque
# el nombre y devuelva el puesto; si no está, devuelve un mensaje.
# ============================================================
def buscar_puesto(nombre_completo, empleados):
    """
    Busca un empleado por su nombre y devuelve su puesto.

    Args:
        nombre_completo (str): Nombre a buscar.
        empleados (list): Lista de diccionarios con claves 'nombre' y 'puesto'.
    """
    for empleado in empleados:
        if empleado["nombre"] == nombre_completo:
            return empleado["puesto"]
    return "Esta persona no trabaja aquí."


# ============================================================
# EJERCICIO 33
# Crea una función lambda que sume elementos correspondientes de dos listas.
# ============================================================
# map con dos iterables: la lambda suma el elemento i de cada lista
sumar_listas = lambda lista1, lista2: list(map(lambda x, y: x + y, lista1, lista2))


# ============================================================
# EJERCICIO 34
# Crea la clase Arbol, con un tronco y ramas como atributos. Métodos:
# crecer_tronco, nueva_rama, crecer_ramas, quitar_rama e info_arbol.
# ============================================================
class Arbol:
    """Representa un árbol genérico con un tronco y una lista de ramas."""

    def __init__(self):
        """Inicializa el árbol con tronco de longitud 1 y sin ramas."""
        self.tronco = 1
        self.ramas = []  # Cada elemento representa la longitud de una rama

    def crecer_tronco(self):
        """Aumenta la longitud del tronco en una unidad."""
        self.tronco += 1

    def nueva_rama(self):
        """Añade una nueva rama de longitud 1."""
        self.ramas.append(1)

    def crecer_ramas(self):
        """Aumenta en una unidad la longitud de todas las ramas existentes."""
        # Recorremos la lista y sumamos 1 a cada longitud (list comprehension)
        self.ramas = [longitud + 1 for longitud in self.ramas]

    def quitar_rama(self, posicion):
        """Elimina la rama de la posición indicada (índice de la lista)."""
        # Comprobamos que la posición exista para no provocar un error
        if 0 <= posicion < len(self.ramas):
            self.ramas.pop(posicion)
        else:
            print(f"No existe ninguna rama en la posición {posicion}.")

    def info_arbol(self):
        """Devuelve un diccionario con la información del árbol."""
        return {
            "longitud_tronco": self.tronco,
            "numero_ramas": len(self.ramas),
            "longitudes_ramas": self.ramas
        }


# ============================================================
# EJERCICIO 36  (el enunciado no incluye un ejercicio 35)
# Crea la clase UsuarioBanco, que representa a un usuario con nombre, saldo y si
# tiene o no cuenta corriente. Métodos: retirar_dinero, transferir_dinero,
# agregar_dinero (los dos primeros lanzan error si no se pueden realizar).
# ============================================================
class UsuarioBanco:
    """Representa a un usuario de un banco."""

    def __init__(self, nombre, saldo, cuenta_corriente):
        """
        Args:
            nombre (str): Nombre del usuario.
            saldo (float): Saldo inicial.
            cuenta_corriente (bool): True si tiene cuenta corriente, False si no.
        """
        self.nombre = nombre
        self.saldo = saldo
        self.cuenta_corriente = cuenta_corriente

    def retirar_dinero(self, cantidad):
        """Retira dinero del saldo. Lanza un error si el saldo es insuficiente."""
        if cantidad > self.saldo:
            raise ValueError(
                f"{self.nombre} no tiene saldo suficiente para retirar {cantidad}."
            )
        self.saldo -= cantidad
        print(f"{self.nombre} ha retirado {cantidad}. Saldo actual: {self.saldo}")

    def transferir_dinero(self, otro_usuario, cantidad):
        """
        Transfiere dinero DESDE otro_usuario HACIA el usuario actual (self).
        Lanza un error si el otro usuario no tiene saldo suficiente.
        """
        if cantidad > otro_usuario.saldo:
            raise ValueError(
                f"{otro_usuario.nombre} no tiene saldo suficiente para transferir {cantidad}."
            )
        otro_usuario.saldo -= cantidad
        self.saldo += cantidad
        print(f"Transferencia de {cantidad} de {otro_usuario.nombre} a {self.nombre} realizada.")

    def agregar_dinero(self, cantidad):
        """Agrega dinero al saldo del usuario."""
        self.saldo += cantidad
        print(f"{self.nombre} ha ingresado {cantidad}. Saldo actual: {self.saldo}")


# ============================================================
# EJERCICIO 37
# Crea una función procesar_texto que procese un texto según la opción indicada:
# "contar", "reemplazar" o "eliminar". Cada opción es otra función auxiliar.
# ============================================================
def contar_palabras(texto):
    """Devuelve un diccionario con cuántas veces aparece cada palabra."""
    conteo = {}
    for palabra in texto.split():
        conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo


def reemplazar_palabras(texto, palabra_original, palabra_nueva):
    """Devuelve el texto reemplazando palabra_original por palabra_nueva."""
    return texto.replace(palabra_original, palabra_nueva)


def eliminar_palabra(texto, palabra):
    """Devuelve el texto sin la palabra indicada."""
    # Reemplazamos la palabra por vacío y limpiamos dobles espacios resultantes
    resultado = texto.replace(palabra, "")
    return " ".join(resultado.split())  # split()+join elimina espacios sobrantes


def procesar_texto(texto, opcion, *args):
    """
    Procesa un texto según la opción indicada.

    Args:
        texto (str): Texto a procesar.
        opcion (str): "contar", "reemplazar" o "eliminar".
        *args: Argumentos variables según la opción
               (reemplazar necesita 2, eliminar necesita 1, contar ninguno).
    """
    if opcion == "contar":
        return contar_palabras(texto)
    elif opcion == "reemplazar":
        # Desempaquetamos los args en (palabra_original, palabra_nueva)
        return reemplazar_palabras(texto, *args)
    elif opcion == "eliminar":
        return eliminar_palabra(texto, *args)
    else:
        return "Opción no válida. Usa 'contar', 'reemplazar' o 'eliminar'."


# ============================================================
# EJERCICIO 38
# Genera un programa que diga si es de noche, de día o de tarde según la hora.
# ============================================================
def momento_del_dia(hora):
    """
    Clasifica la hora (0-23) en día, tarde o noche.
    Rangos usados: día [6-14), tarde [14-21), noche el resto.
    """
    if 6 <= hora < 14:
        return "Es de día"
    elif 14 <= hora < 21:
        return "Es de tarde"
    else:
        return "Es de noche"


# ============================================================
# EJERCICIO 39
# Escribe un programa que determine la calificación en texto según la nota:
# 0-69 insuficiente, 70-79 bien, 80-89 muy bien, 90-100 excelente.
# ============================================================
def calificacion_texto(nota):
    """Convierte una nota numérica en su calificación en texto."""
    if nota < 70:
        return "insuficiente"
    elif nota < 80:
        return "bien"
    elif nota < 90:
        return "muy bien"
    else:
        return "excelente"


# ============================================================
# EJERCICIO 40
# Escribe una función que tome dos parámetros: figura ("rectangulo", "circulo"
# o "triangulo") y datos (tupla con los datos necesarios para calcular el área).
# ============================================================
def area_figura(figura, datos):
    """
    Calcula el área de una figura geométrica.

    Args:
        figura (str): "rectangulo", "circulo" o "triangulo".
        datos (tuple): Datos necesarios (base/altura, radio, etc.).
    """
    if figura == "rectangulo":
        base, altura = datos
        return base * altura
    elif figura == "circulo":
        radio = datos[0]
        return math.pi * radio ** 2
    elif figura == "triangulo":
        base, altura = datos
        return (base * altura) / 2
    else:
        return "Figura no reconocida."


# ============================================================
# EJERCICIO 41
# Programa que calcule el monto final de una compra tras aplicar un descuento,
# usando condicionales (if/elif/else).
# ============================================================
def calcular_compra():
    """Calcula el precio final de una compra aplicando un cupón si es válido."""
    precio = float(input("Introduce el precio original del artículo: "))
    tiene_cupon = input("¿Tienes un cupón de descuento? (sí/no): ").strip().lower()

    # Aceptamos "sí" y "si" como respuesta afirmativa
    if tiene_cupon in ("sí", "si"):
        descuento = float(input("Introduce el valor del cupón de descuento: "))
        # Solo aplicamos el descuento si el cupón es válido (mayor que 0)
        if descuento > 0:
            precio_final = precio - descuento
        else:
            precio_final = precio
    else:
        precio_final = precio

    print(f"El precio final de la compra es: {precio_final}€")


# ============================================================
# CASOS DE USO / DEMOSTRACIONES
# ============================================================
if __name__ == "__main__":

    print("EJERCICIO 1:", frecuencia_letras("hola mundo"))

    print("EJERCICIO 2:", doblar_valores([1, 2, 3, 4]))

    print("EJERCICIO 3:", palabras_que_contienen(["casa", "casona", "perro", "descasar"], "casa"))

    print("EJERCICIO 4:", diferencia_listas([10, 20, 30], [1, 2, 3]))

    print("EJERCICIO 5:", evaluar_media([4, 6, 8, 5]))

    print("EJERCICIO 6:", factorial(5))

    print("EJERCICIO 7:", tuplas_a_strings([("Juan", "Garcia"), ("Ana", "Lopez")]))

    # EJERCICIO 8 (requiere input) -> descomenta para probar:
    # dividir_dos_numeros()

    print("EJERCICIO 9:", filtrar_mascotas(["Perro", "Tigre", "Gato", "Oso", "Canario"]))

    # EJERCICIO 10 (usa try/except con la excepción personalizada):
    try:
        print("EJERCICIO 10:", calcular_promedio_seguro([]))
    except ListaVaciaError as error:
        print("EJERCICIO 10:", error)

    # EJERCICIO 11 (requiere input) -> descomenta para probar:
    # pedir_edad()

    print("EJERCICIO 12:", longitud_palabras("me encanta programar en python"))

    print("EJERCICIO 13:", mayusculas_minusculas("aAbBcC"))

    print("EJERCICIO 14:", palabras_con_letra(["manzana", "melon", "pera", "mango"], "m"))

    print("EJERCICIO 15:", sumar_tres([1, 2, 3, 10]))

    print("EJERCICIO 16:", palabras_mas_largas("el gato come pescado hoy", 3))

    print("EJERCICIO 17:", digitos_a_numero([5, 7, 2]))

    lista_estudiantes = [
        {"nombre": "Ana", "edad": 20, "calificacion": 95},
        {"nombre": "Luis", "edad": 22, "calificacion": 80},
        {"nombre": "Marta", "edad": 21, "calificacion": 92},
    ]
    print("EJERCICIO 18:", estudiantes_sobresalientes(lista_estudiantes))

    print("EJERCICIO 19:", filtrar_impares([1, 2, 3, 4, 5, 6, 7]))

    print("EJERCICIO 20:", solo_enteros([1, "hola", 2, "python", 3, True]))

    print("EJERCICIO 21:", cubo(3))

    print("EJERCICIO 22:", producto_total([1, 2, 3, 4]))

    print("EJERCICIO 23:", concatenar_palabras(["Python", "es", "genial"]))

    print("EJERCICIO 24:", diferencia_total([100, 20, 30, 5]))

    print("EJERCICIO 25:", contar_caracteres("Hola Mundo"))

    print("EJERCICIO 26:", resto_division(10, 3))

    print("EJERCICIO 27:", promedio([10, 20, 30]))

    print("EJERCICIO 28:", primer_duplicado([1, 2, 3, 2, 4, 3]))

    print("EJERCICIO 29:", enmascarar(1234567890))

    print("EJERCICIO 30:", son_anagramas("roma", "amor"))

    # EJERCICIO 31 (requiere input) -> descomenta para probar:
    # buscar_nombre_en_lista()

    empleados = [
        {"nombre": "Juan Garcia", "puesto": "Gerente"},
        {"nombre": "Ana Lopez", "puesto": "Analista"},
    ]
    print("EJERCICIO 32:", buscar_puesto("Ana Lopez", empleados))
    print("EJERCICIO 32:", buscar_puesto("Pedro Ruiz", empleados))

    print("EJERCICIO 33:", sumar_listas([1, 2, 3], [10, 20, 30]))

    # EJERCICIO 34: Caso de uso de la clase Arbol
    print("\n--- EJERCICIO 34: Clase Arbol ---")
    arbol = Arbol()          # 1. Crear un árbol
    arbol.crecer_tronco()    # 2. Hacer crecer el tronco
    arbol.nueva_rama()       # 3. Añadir una rama
    arbol.crecer_ramas()     # 4. Hacer crecer todas las ramas
    arbol.nueva_rama()       # 5. Añadir dos ramas nuevas
    arbol.nueva_rama()
    arbol.quitar_rama(2)     # 6. Retirar la rama de la posición 2 (índice 2)
    print("Info del árbol:", arbol.info_arbol())  # 7. Obtener información

    # EJERCICIO 36: Caso de uso de la clase UsuarioBanco
    print("\n--- EJERCICIO 36: Clase UsuarioBanco ---")
    alicia = UsuarioBanco("Alicia", 100, True)  # 1. Crear usuarios
    bob = UsuarioBanco("Bob", 50, True)
    bob.agregar_dinero(20)                       # 2. Agregar 20 a Bob -> 70
    try:
        # 3. Transferir 80 de Bob a Alicia. Bob solo tiene 70, así que dará error:
        alicia.transferir_dinero(bob, 80)
    except ValueError as error:
        print("Error controlado:", error)
    alicia.retirar_dinero(50)                    # 4. Retirar 50 a Alicia -> 50

    # EJERCICIO 37: Caso de uso de procesar_texto
    print("\n--- EJERCICIO 37: procesar_texto ---")
    texto_ejemplo = "hola mundo hola python mundo"
    print("Contar:", procesar_texto(texto_ejemplo, "contar"))
    print("Reemplazar:", procesar_texto(texto_ejemplo, "reemplazar", "mundo", "planeta"))
    print("Eliminar:", procesar_texto(texto_ejemplo, "eliminar", "hola"))

    print("\nEJERCICIO 38:", momento_del_dia(10), "/", momento_del_dia(17), "/", momento_del_dia(23))

    print("EJERCICIO 39:", calificacion_texto(65), "/", calificacion_texto(75),
          "/", calificacion_texto(85), "/", calificacion_texto(95))

    print("EJERCICIO 40:",
          "rectángulo:", area_figura("rectangulo", (4, 5)),
          "| círculo:", round(area_figura("circulo", (3,)), 2),
          "| triángulo:", area_figura("triangulo", (6, 4)))

    # EJERCICIO 41 (requiere input) -> descomenta para probar:
    # calcular_compra()
