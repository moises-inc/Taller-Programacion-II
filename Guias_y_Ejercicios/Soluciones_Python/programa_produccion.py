"""Sistema de control de productos y ordenes de produccion.

El programa utiliza un archivo de texto delimitado por punto y coma como
almacenamiento persistente. Cada linea representa una orden con el formato:

    id;producto;area;cantidad;valor_unitario;estado

La implementacion mantiene separadas las responsabilidades de preparacion,
serializacion, lectura, presentacion y modificacion de los registros.
"""

from pathlib import Path
from typing import Final, TypedDict


class Producto(TypedDict):
    """Estructura tipada para una orden de produccion."""

    id: int
    producto: str
    area: str
    cantidad: int
    valor_unitario: int
    estado: str


CARPETA_DATOS: Final[Path] = Path("datos")
ARCHIVO_PRODUCCION: Final[Path] = CARPETA_DATOS / "produccion.txt"
CANTIDAD_CAMPOS: Final[int] = 6
ESTADO_INICIAL: Final[str] = "Pendiente"
ESTADOS_PERMITIDOS: Final[tuple[str, ...]] = (
    "Pendiente",
    "En Proceso",
    "Completada",
    "Cancelada",
)


def preparar_archivo() -> None:
    """Crea la carpeta de datos y asegura la existencia del archivo TXT.

    El modo ``a`` crea el archivo si no existe y, al mismo tiempo, conserva
    cualquier contenido que ya estuviera almacenado.
    """

    try:
        CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
        with ARCHIVO_PRODUCCION.open("a", encoding="utf-8"):
            pass
    except OSError as error:
        raise OSError(
            f"No fue posible preparar '{ARCHIVO_PRODUCCION}': {error}"
        ) from error


def convertir_linea_a_diccionario(linea: str) -> Producto:
    """Convierte una linea delimitada en un diccionario tipado.

    Se eliminan los espacios externos de la linea y de cada campo. Los
    campos ``id``, ``cantidad`` y ``valor_unitario`` se convierten a ``int``
    para permitir comparaciones y operaciones aritmeticas posteriores.

    Args:
        linea: Registro de texto sin formato o con salto de linea final.

    Returns:
        Un diccionario con las seis claves del modelo de produccion.

    Raises:
        ValueError: Si la linea no tiene seis campos o contiene datos
            invalidos.
    """

    linea_limpia = linea.strip()
    if not linea_limpia:
        raise ValueError("La linea esta vacia.")

    campos = [campo.strip() for campo in linea_limpia.split(";")]
    if len(campos) != CANTIDAD_CAMPOS:
        raise ValueError(
            "El registro debe contener exactamente "
            f"{CANTIDAD_CAMPOS} campos separados por ';'."
        )

    try:
        identificador = int(campos[0])
        cantidad = int(campos[3])
        valor_unitario = int(campos[4])
    except ValueError as error:
        raise ValueError(
            "Los campos id, cantidad y valor_unitario deben ser enteros."
        ) from error

    if identificador <= 0:
        raise ValueError("El id debe ser un entero mayor que cero.")
    if not campos[1] or not campos[2] or not campos[5]:
        raise ValueError("Producto, area y estado no pueden estar vacios.")
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")
    if valor_unitario < 0:
        raise ValueError("El valor_unitario no puede ser negativo.")

    return {
        "id": identificador,
        "producto": campos[1],
        "area": campos[2],
        "cantidad": cantidad,
        "valor_unitario": valor_unitario,
        "estado": campos[5],
    }


def convertir_diccionario_a_linea(producto: Producto) -> str:
    """Serializa un diccionario de produccion en una linea delimitada.

    La funcion no agrega ``\n``. Esto permite que el llamador decida cuando
    terminar la linea al escribirla en el archivo.

    Args:
        producto: Diccionario que cumple el modelo de seis campos.

    Returns:
        Texto plano con los campos separados por punto y coma.

    Raises:
        ValueError: Si un campo textual contiene el delimitador o si los
            valores numericos no cumplen las reglas del modelo.
    """

    campos_texto = (producto["producto"], producto["area"], producto["estado"])
    if any(";" in campo for campo in campos_texto):
        raise ValueError("Los campos textuales no pueden contener ';'.")
    if producto["id"] <= 0:
        raise ValueError("El id debe ser mayor que cero.")
    if not all(campo.strip() for campo in campos_texto):
        raise ValueError("Los campos textuales no pueden estar vacios.")
    if producto["cantidad"] <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")
    if producto["valor_unitario"] < 0:
        raise ValueError("El valor_unitario no puede ser negativo.")

    return ";".join(
        (
            str(producto["id"]),
            producto["producto"].strip(),
            producto["area"].strip(),
            str(producto["cantidad"]),
            str(producto["valor_unitario"]),
            producto["estado"].strip(),
        )
    )


def leer_productos() -> list[Producto]:
    """Lee el archivo completo y reconstruye una lista de diccionarios.

    Las lineas vacias o con formato invalido se omiten con una advertencia,
    de modo que un registro defectuoso no impida recuperar los demas.
    ``FileNotFoundError`` se trata defensivamente como un archivo sin datos.
    """

    productos: list[Producto] = []

    try:
        with ARCHIVO_PRODUCCION.open("r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                if not linea.strip():
                    continue
                try:
                    productos.append(convertir_linea_a_diccionario(linea))
                except (ValueError, TypeError) as error:
                    print(f"Advertencia: linea {numero_linea} omitida: {error}")
    except FileNotFoundError:
        return productos
    except (OSError, UnicodeError) as error:
        print(f"Error al leer '{ARCHIVO_PRODUCCION}': {error}")

    return productos


def _reescribir_archivo(productos: list[Producto]) -> None:
    """Reemplaza el contenido del archivo con la lista recibida."""

    preparar_archivo()
    lineas = [convertir_diccionario_a_linea(producto) + "\n" for producto in productos]
    try:
        with ARCHIVO_PRODUCCION.open("w", encoding="utf-8") as archivo:
            archivo.writelines(lineas)
    except OSError as error:
        raise OSError(
            f"No fue posible reescribir '{ARCHIVO_PRODUCCION}': {error}"
        ) from error


def _ajustar_texto(texto: str, ancho: int) -> str:
    """Recorta textos extensos para conservar la alineacion de la tabla."""

    if len(texto) <= ancho:
        return texto
    return texto[: max(0, ancho - 3)] + "..."


def mostrar_productos(productos: list[Producto]) -> None:
    """Presenta las ordenes en una tabla de consola alineada."""

    anchos = {
        "id": 4,
        "producto": 24,
        "area": 16,
        "cantidad": 10,
        "valor_unitario": 15,
        "estado": 14,
    }
    separador = "-+-".join("-" * ancho for ancho in anchos.values())

    print("\nORDENES DE PRODUCCION")
    print(separador)
    print(
        f"{'ID':>{anchos['id']}} | "
        f"{'PRODUCTO':<{anchos['producto']}} | "
        f"{'AREA':<{anchos['area']}} | "
        f"{'CANTIDAD':>{anchos['cantidad']}} | "
        f"{'VALOR UNITARIO':>{anchos['valor_unitario']}} | "
        f"{'ESTADO':<{anchos['estado']}}"
    )
    print(separador)

    if not productos:
        print("No hay ordenes registradas.")
        print(separador)
        return

    for producto in productos:
        producto_texto = _ajustar_texto(producto["producto"], anchos["producto"])
        area_texto = _ajustar_texto(producto["area"], anchos["area"])
        estado_texto = _ajustar_texto(producto["estado"], anchos["estado"])
        cantidad_texto = f"{producto['cantidad']:,}"
        valor_texto = f"${producto['valor_unitario']:,}"
        print(
            f"{producto['id']:>{anchos['id']}} | "
            f"{producto_texto:<{anchos['producto']}} | "
            f"{area_texto:<{anchos['area']}} | "
            f"{cantidad_texto:>{anchos['cantidad']}} | "
            f"{valor_texto:>{anchos['valor_unitario']}} | "
            f"{estado_texto:<{anchos['estado']}}"
        )
    print(separador)


def _solicitar_texto(mensaje: str, nombre_campo: str) -> str:
    """Solicita texto no vacio y sin el delimitador del archivo."""

    while True:
        valor = input(mensaje).strip()
        if not valor:
            print(f"Error: {nombre_campo} no puede estar vacio.")
        elif ";" in valor:
            print(f"Error: {nombre_campo} no puede contener ';'.")
        else:
            return valor


def _solicitar_entero(mensaje: str, minimo: int, nombre_campo: str) -> int:
    """Solicita un entero que sea mayor o igual al minimo indicado."""

    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor < minimo:
                print(
                    f"Error: {nombre_campo} debe ser un entero mayor o igual "
                    f"que {minimo}."
                )
            else:
                return valor
        except ValueError:
            print(f"Error: {nombre_campo} debe ser un entero valido.")


def _obtener_siguiente_id(productos: list[Producto]) -> int:
    """Calcula un identificador positivo que no se repita con los existentes."""

    return max((producto["id"] for producto in productos), default=0) + 1


def agregar_producto() -> None:
    """Solicita una orden y la agrega al final del archivo en modo ``a``."""

    preparar_archivo()
    productos = leer_productos()
    identificador = _obtener_siguiente_id(productos)

    print("\nREGISTRAR NUEVA ORDEN")
    nombre = _solicitar_texto("Producto: ", "El nombre del producto")
    area = _solicitar_texto("Area: ", "El area")
    cantidad = _solicitar_entero("Cantidad de unidades: ", 1, "La cantidad")
    valor_unitario = _solicitar_entero(
        "Valor unitario (entero >= 0): ",
        0,
        "El valor unitario",
    )

    producto: Producto = {
        "id": identificador,
        "producto": nombre,
        "area": area,
        "cantidad": cantidad,
        "valor_unitario": valor_unitario,
        "estado": ESTADO_INICIAL,
    }

    try:
        with ARCHIVO_PRODUCCION.open("a", encoding="utf-8") as archivo:
            archivo.write(convertir_diccionario_a_linea(producto) + "\n")
    except OSError as error:
        print(f"Error al guardar la orden: {error}")
        return

    print(f"Orden {identificador} agregada correctamente.")


def calcular_costos_produccion(productos: list[Producto]) -> None:
    """Calcula y muestra el subtotal de cada orden y el total de la planta."""

    print("\nDESGLOSE DE COSTOS DE PRODUCCION")
    print("-" * 72)
    if not productos:
        print("No hay ordenes disponibles para calcular costos.")
        print("-" * 72)
        return

    total_produccion = 0
    for producto in productos:
        subtotal = producto["cantidad"] * producto["valor_unitario"]
        total_produccion += subtotal
        print(
            f"ID {producto['id']:>4} | "
            f"{_ajustar_texto(producto['producto'], 28):<28} | "
            f"{producto['cantidad']:>8,} unidades x "
            f"${producto['valor_unitario']:>12,} = ${subtotal:>14,}"
        )

    print("-" * 72)
    print(f"Costo total estimado de produccion: ${total_produccion:,}")


def buscar_productos(productos: list[Producto]) -> None:
    """Filtra las ordenes por area o estado sin distinguir mayusculas."""

    if not productos:
        print("No hay ordenes disponibles para buscar.")
        return

    print("\nCRITERIOS DE BUSQUEDA: area / estado")
    criterio = input("Seleccione el criterio: ").strip().lower()
    if criterio not in {"area", "estado"}:
        print("Error: el criterio debe ser 'area' o 'estado'.")
        return

    valor_buscado = input(f"Ingrese {criterio}: ").strip().lower()
    if not valor_buscado:
        print("Error: el valor de busqueda no puede estar vacio.")
        return

    resultados = [
        producto
        for producto in productos
        if producto[criterio].lower() == valor_buscado
    ]
    if resultados:
        mostrar_productos(resultados)
    else:
        print("No se encontraron ordenes coincidentes.")


def _solicitar_id_existente(productos: list[Producto]) -> int:
    """Solicita repetidamente un id hasta encontrarlo en la lista."""

    ids_existentes = {producto["id"] for producto in productos}
    while True:
        identificador = _solicitar_entero("Ingrese el id de la orden: ", 1, "El id")
        if identificador in ids_existentes:
            return identificador
        print("Error: no existe una orden con ese id.")


def _solicitar_nuevo_estado(estado_actual: str) -> str:
    """Solicita un estado valido y evita cambios redundantes."""

    print(f"Estado actual: {estado_actual}")
    print("Estados validos: " + ", ".join(ESTADOS_PERMITIDOS))
    estados_por_clave = {estado.lower(): estado for estado in ESTADOS_PERMITIDOS}

    while True:
        nuevo_estado = input("Nuevo estado: ").strip().lower()
        if nuevo_estado in estados_por_clave:
            estado_normalizado = estados_por_clave[nuevo_estado]
            if estado_normalizado == estado_actual:
                print("El estado no presenta cambios.")
            return estado_normalizado
        print("Error: seleccione uno de los estados indicados.")


def actualizar_estado(productos: list[Producto]) -> None:
    """Actualiza un estado en memoria y sincroniza la lista completa en disco."""

    if not productos:
        print("No hay ordenes disponibles para actualizar.")
        return

    mostrar_productos(productos)
    identificador = _solicitar_id_existente(productos)
    producto = next(
        producto for producto in productos if producto["id"] == identificador
    )
    estado_anterior = producto["estado"]
    producto["estado"] = _solicitar_nuevo_estado(estado_anterior)

    try:
        _reescribir_archivo(productos)
    except OSError:
        producto["estado"] = estado_anterior
        raise

    print(f"Estado de la orden {identificador} actualizado correctamente.")


def _solicitar_confirmacion(mensaje: str) -> bool:
    """Solicita una confirmacion explicita y devuelve un valor booleano."""

    while True:
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()
        if respuesta in {"s", "si"}:
            return True
        if respuesta in {"n", "no"}:
            return False
        print("Respuesta invalida. Escriba 's' para confirmar o 'n' para cancelar.")


def eliminar_producto(productos: list[Producto]) -> None:
    """Elimina una orden confirmada y reescribe el archivo completo."""

    if not productos:
        print("No hay ordenes disponibles para eliminar.")
        return

    mostrar_productos(productos)
    identificador = _solicitar_id_existente(productos)
    posicion = next(
        indice
        for indice, producto in enumerate(productos)
        if producto["id"] == identificador
    )
    producto_eliminado = productos[posicion]

    if not _solicitar_confirmacion(
        f"Confirma la eliminacion de la orden {identificador}"
    ):
        print("Operacion cancelada.")
        return

    productos.pop(posicion)
    try:
        _reescribir_archivo(productos)
    except OSError:
        productos.insert(posicion, producto_eliminado)
        raise

    print(f"Orden {identificador} eliminada correctamente.")


def programa_principal() -> None:
    """Coordina el menu interactivo y mantiene el programa en ejecucion."""

    try:
        preparar_archivo()
        print("=" * 72)
        print("CONTROL DE PRODUCTOS Y ORDENES DE PRODUCCION")
        print("Universidad San Sebastian - Taller de Programacion II")
        print("=" * 72)

        while True:
            productos = leer_productos()
            print("\nMENU PRINCIPAL")
            print("1. Preparar archivo")
            print("2. Agregar orden")
            print("3. Listar ordenes")
            print("4. Calcular costos de produccion")
            print("5. Buscar por area o estado")
            print("6. Actualizar estado")
            print("7. Eliminar orden")
            print("8. Salir")

            opcion = input("Seleccione una opcion: ").strip()
            if opcion == "1":
                preparar_archivo()
                print("El archivo esta preparado.")
            elif opcion == "2":
                agregar_producto()
            elif opcion == "3":
                mostrar_productos(productos)
            elif opcion == "4":
                calcular_costos_produccion(productos)
            elif opcion == "5":
                buscar_productos(productos)
            elif opcion == "6":
                actualizar_estado(productos)
            elif opcion == "7":
                eliminar_producto(productos)
            elif opcion == "8":
                print("Programa finalizado.")
                break
            else:
                print("Opcion invalida. Seleccione un numero del 1 al 8.")
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma finalizado por el usuario.")
    except Exception as error:
        print(f"\nError inesperado: {error}")


if __name__ == "__main__":
    programa_principal()
