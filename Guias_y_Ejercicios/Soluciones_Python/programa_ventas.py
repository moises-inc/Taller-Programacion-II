# ==============================================================================
# PROGRAMA DE REGISTRO DE VENTAS EN PYTHON (CON ARCHIVOS Y DICCIONARIOS)
# Taller de Programación II — Universidad San Sebastián
# ==============================================================================
# Este script implementa la solución completa a la Guía Práctica de Ventas.
# Aplica diccionarios, funciones modulares, validaciones (GIGO), persistencia
# en el archivo "ventas.txt" (modo 'a' y encoding 'utf-8'), y cálculo de resúmenes.
# ==============================================================================

import os
from datetime import date

# Nombre del archivo de almacenamiento persistente
NOMBRE_ARCHIVO = "ventas.txt"


# ------------------------------------------------------------------------------
# FUNCIÓN 1: calcular_total
# ------------------------------------------------------------------------------
def calcular_total(valor_unitario: int, cantidad: int) -> int:
    """
    Recibe el valor unitario y la cantidad (ambos enteros) y retorna
    el total calculado (valor_unitario * cantidad).
    """
    # El total no se solicita al usuario: se calcula internamente
    return valor_unitario * cantidad


# ------------------------------------------------------------------------------
# FUNCIÓN 2: solicitar_venta
# ------------------------------------------------------------------------------
def solicitar_venta() -> dict:
    """
    Solicita los datos de la venta al usuario por consola, aplicando
    validaciones estrictas (GIGO). Retorna un diccionario con 6 claves.
    """
    print("\n--- REGISTRAR NUEVA VENTA ---")

    # 1. Validación del nombre del cliente (No puede quedar vacío)
    while True:
        cliente = input("Ingrese nombre del cliente: ").strip()
        if cliente:
            break
        print("❌ Error: El nombre del cliente no puede estar vacío.")

    # 2. Validación del producto (No puede quedar vacío)
    while True:
        producto = input("Ingrese producto comprado: ").strip()
        if producto:
            break
        print("❌ Error: El nombre del producto no puede estar vacío.")

    # 3. Validación del valor unitario (Debe ser entero mayor a cero)
    while True:
        try:
            valor_unitario = int(input("Ingrese valor unitario ($CLP): "))
            if valor_unitario > 0:
                break
            print("❌ Error: El valor unitario debe ser un entero mayor a cero.")
        except ValueError:
            print("❌ Error: Debe ingresar un número entero válido.")

    # 4. Validación de la cantidad (Debe ser entero mayor a cero)
    while True:
        try:
            cantidad = int(input("Ingrese cantidad de unidades: "))
            if cantidad > 0:
                break
            print("❌ Error: La cantidad debe ser un entero mayor a cero.")
        except ValueError:
            print("❌ Error: Debe ingresar un número entero válido.")

    # 5. Cálculo automático del total de la venta
    total = calcular_total(valor_unitario, cantidad)

    # 6. Obtención de la fecha actual en formato YYYY-MM-DD
    fecha_actual = date.today().strftime("%Y-%m-%d")

    # Construcción y retorno del diccionario con las 6 claves especificadas
    venta = {
        "nombre_cliente": cliente,
        "producto": producto,
        "valor_unitario": valor_unitario,
        "cantidad": cantidad,
        "total": total,
        "fecha": fecha_actual
    }

    print(f"✅ Venta registrada exitosamente. Total calculado: ${total:,.0f} CLP")
    return venta


# ------------------------------------------------------------------------------
# FUNCIÓN 3: guardar_venta
# ------------------------------------------------------------------------------
def guardar_venta(venta: dict, ruta_archivo: str = NOMBRE_ARCHIVO) -> None:
    """
    Recibe un diccionario 'venta' y escribe sus 6 campos en una línea
    del archivo 'ventas.txt' separando cada campo por punto y coma (;).
    Usa el modo 'a' (append) para conservar los registros anteriores.
    """
    # Formatear la cadena delimitada por punto y coma (;)
    # Orden de campos: cliente;producto;valor_unitario;cantidad;total;fecha
    linea = (
        f"{venta['nombre_cliente']};"
        f"{venta['producto']};"
        f"{venta['valor_unitario']};"
        f"{venta['cantidad']};"
        f"{venta['total']};"
        f"{venta['fecha']}\n"
    )

    # Administrador de contexto with open en modo 'a' y encoding 'utf-8'
    with open(ruta_archivo, "a", encoding="utf-8") as archivo:
        archivo.write(linea)
    
    print(f"💾 Registro guardado correctamente en '{ruta_archivo}'.")


# ------------------------------------------------------------------------------
# FUNCIÓN 4: leer_ventas
# ------------------------------------------------------------------------------
def leer_ventas(ruta_archivo: str = NOMBRE_ARCHIVO) -> list:
    """
    Abre el archivo 'ventas.txt' en modo lectura ('r'), recorre cada línea,
    limpia saltos de línea con strip(), separa los campos con split(';'),
    convierte valores numéricos a entero y reconstruye una lista de diccionarios.
    """
    ventas = []

    # Verificar existencia previa antes de intentar abrir
    if not os.path.exists(ruta_archivo):
        print(f"⚠️ El archivo '{ruta_archivo}' aún no existe.")
        return ventas

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                linea_limpia = linea.strip()
                if not linea_limpia:
                    continue  # Ignorar líneas vacías

                partes = linea_limpia.split(";")
                if len(partes) == 6:
                    registro = {
                        "nombre_cliente": partes[0],
                        "producto": partes[1],
                        "valor_unitario": int(partes[2]),
                        "cantidad": int(partes[3]),
                        "total": int(partes[4]),
                        "fecha": partes[5]
                    }
                    ventas.append(registro)
                else:
                    print(f"⚠️ Advertencia: Línea {numero_linea} con formato incorrecto.")
    except Exception as e:
        print(f"❌ Error al leer el archivo '{ruta_archivo}': {e}")

    return ventas


# ------------------------------------------------------------------------------
# FUNCIÓN 5: mostrar_ventas
# ------------------------------------------------------------------------------
def mostrar_ventas(ventas: list) -> None:
    """
    Recibe una lista de diccionarios de ventas y los muestra por pantalla
    en una tabla formateada y legible.
    """
    print("\n" + "=" * 80)
    print(f"{'N°':<3} | {'CLIENTE':<20} | {'PRODUCTO':<18} | {'UNITARIO':<9} | {'CANT':<4} | {'TOTAL':<9} | {'FECHA':<10}")
    print("=" * 80)

    if not ventas:
        print(" No hay registros de ventas para mostrar.")
        print("=" * 80)
        return

    for idx, v in enumerate(ventas, start=1):
        print(
            f"{idx:<3} | "
            f"{v['nombre_cliente']:<20} | "
            f"{v['producto']:<18} | "
            f"${v['valor_unitario']:<8,d} | "
            f"{v['cantidad']:<4} | "
            f"${v['total']:<8,d} | "
            f"{v['fecha']:<10}"
        )
    print("=" * 80)


# ------------------------------------------------------------------------------
# FUNCIÓN 6: calcular_resumen
# ------------------------------------------------------------------------------
def calcular_resumen(ventas: list) -> dict:
    """
    Recibe la lista de diccionarios de ventas y aplica el patrón acumulador
    para calcular la cantidad total de ventas registradas y el monto acumulado general.
    """
    cantidad_ventas = len(ventas)
    total_general = 0

    for venta in ventas:
        total_general += venta["total"]

    print("\n=== RESUMEN EJECUTIVO DE VENTAS ===")
    print(f" Total de transacciones registradas : {cantidad_ventas}")
    print(f" Recaudación total acumulada        : ${total_general:,.0f} CLP")
    print("====================================")

    return {
        "cantidad_ventas": cantidad_ventas,
        "total_general": total_general
    }


# ------------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------------------------
def main():
    print("==========================================================================")
    print("   SISTEMA DE REGISTRO DE VENTAS CON ARCHIVOS (TP2 - USS SEDE PATAGONIA)   ")
    print("==========================================================================")

    # Petición de 3 ventas de prueba al usuario
    NUM_VENTAS = 3
    print(f"\nSe procederá a registrar {NUM_VENTAS} ventas de prueba.")

    for i in range(1, NUM_VENTAS + 1):
        print(f"\n--- Registro {i} de {NUM_VENTAS} ---")
        v = solicitar_venta()
        guardar_venta(v)

    # Recuperación desde el archivo en disco
    print("\n📖 Leyendo todas las ventas almacenadas en 'ventas.txt'...")
    ventas_recuperadas = leer_ventas()

    # Mostrar la tabla formateada
    mostrar_ventas(ventas_recuperadas)

    # Calcular y mostrar el resumen
    calcular_resumen(ventas_recuperadas)


if __name__ == "__main__":
    main()
