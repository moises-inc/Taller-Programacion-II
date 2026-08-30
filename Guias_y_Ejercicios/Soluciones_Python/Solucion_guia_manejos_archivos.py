# Manejo de archivos para una tienda

''' Ejercicio 1. Preparar la ruta y crear el archivo 

Instrucciones: Crea una constante para la carpeta datos y otra para el archivo 
produccion.txt. Usa pathlib.Path. Luego crea la carpeta con mkdir(...) y el archivo con 
modo a
'''

from pathlib import Path

# Constantes para la carpeta y el archivo
CARPETA_DATOS = Path("datos")
ARCHIVO_PRODUCCION = CARPETA_DATOS / "produccion.txt"

# Crear la carpeta y el archivo
CARPETA_DATOS.mkdir(exist_ok=True)
ARCHIVO_PRODUCCION.touch(exist_ok=True)

'''Ejercicio 2. Agregar el primer registro

Instrucciones: Solicita al usuario el nombre de un producto y una cantidad. Guarda 
ambos datos en una línea. Por ahora puedes utilizar un formato sencillo, por ejemplo: 
producto;cantidad.
'''

# Solicitar al usuario el nombre del producto y la cantidad

# Validación de entrada

while True:
    try:
        nombre_producto = input("Ingrese el nombre del producto: ")
        cantidad_producto = int(input("Ingrese la cantidad del producto: "))
        if cantidad_producto < 0:
            print("La cantidad no puede ser negativa. Intente nuevamente.")
            continue
        if nombre_producto.strip() == "":
            print("El nombre del producto no puede estar vacío. Intente nuevamente.")
            continue
        break
    except ValueError:
        print("Por favor, ingrese un número válido para la cantidad.")


# Escribir el registro en el archivo
with open(ARCHIVO_PRODUCCION, "a") as f:
    f.write(f"{nombre_producto};{cantidad_producto}\n")