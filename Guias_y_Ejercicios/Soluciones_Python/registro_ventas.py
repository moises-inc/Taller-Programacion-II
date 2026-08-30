'''
Generar código que sirva para registrar ventas en un archivo de texto llamado "registro_ventas.txt".

Usar funciones, validaciones, diccionarios y persistencia de datos.

Se debe registrar un mínimo de 3 ventas. Se debe registrar: 
• Nombre del cliente. 
• Producto comprado. 
• Valor unitario en pesos chilenos. 
• Cantidad de unidades. 
• Total de la venta. 
• Fecha de la venta

'''

# Librerias para manejo de fechas y existencia de archivos

import os
from datetime import datetime

archivo_ventas = "registro_ventas.txt"

# Función 0: Validación de entradas

def validar_entrada(prompt, tipo):
    while True:
        entrada = input(prompt)
        if tipo == "str":
            if entrada.strip() != "":
                return entrada.strip()
            else:
                print("Entrada inválida. Por favor, ingrese un valor válido.")
        elif tipo == "float":
            try:
                valor = float(entrada)
                if valor > 0:
                    return valor
                else:
                    print("El valor debe ser mayor a 0.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido.")
        elif tipo == "int":
            try:
                valor = int(entrada)
                if valor > 0:
                    return valor
                else:
                    print("El valor debe ser mayor a 0.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número entero válido.")
                
# Función 1: Registrar venta

def solicitar_venta():
    print("\n--- Registro de Venta ---")
    
    nombre_cliente = validar_entrada("Ingrese el nombre del cliente: ", "str")
    producto_comprado = validar_entrada("Ingrese el producto comprado: ", "str")
    valor_unitario = validar_entrada("Ingrese el valor unitario en pesos chilenos: ", "float")
    cantidad_unidades = validar_entrada("Ingrese la cantidad de unidades: ", "int")
    total_venta = valor_unitario * cantidad_unidades
    fecha_venta = datetime.now().strftime("%Y-%m-%d")
    
    venta = {
        "nombre_cliente": nombre_cliente,
        "producto_comprado": producto_comprado,
        "valor_unitario": valor_unitario,
        "cantidad_unidades": cantidad_unidades,
        "total_venta": total_venta,
        "fecha_venta": fecha_venta
    }
    
    return venta

# Función 2: Calcular total

def calcular_total(valor, cantidad):
    total = valor * cantidad
    print(f"Venta registrada. Total de la venta: {total}")
    return total

# Función 3: Guardar venta en archivo

def guardar_venta(venta):
    contenido = {
        "nombre_cliente": venta["nombre_cliente"],
        "producto_comprado": venta["producto_comprado"],
        "valor_unitario": venta["valor_unitario"],
        "cantidad_unidades": venta["cantidad_unidades"],
        "total_venta": venta["total_venta"],
        "fecha_venta": venta["fecha_venta"]
    }
    
    with open(archivo_ventas, "a") as archivo:
        archivo.write(f"{contenido}\n")
        
    print("Venta guardada exitosamente en el archivo.")
    
# Función 4: Leer ventas

def leer_ventas():
    if not os.path.exists(archivo_ventas):
        print("No hay ventas registradas.")
        return
    
    print("\n--- Ventas Registradas ---")
    with open(archivo_ventas, "r") as archivo:
        for linea in archivo:
            print(linea.strip()) 
