"""Módulo de Práctica Intensiva: Serialización JSON en Python.

Universidad San Sebastián · Sede Patagonia
Taller de Programación II · Sprint de Entrenamiento Solemnes 2026

Diseñado para dominar la gestión de estructuras jerárquicas y persisitencia JSON:
- json.dump() / json.load() para archivos
- json.dumps() / json.loads() para cadenas de texto
- Formateo con indent=4 y ensure_ascii=False
- Captura de json.JSONDecodeError y FileNotFoundError
- Modificación y sincronización de objetos anidados en disco
"""

import json
from pathlib import Path
from typing import Any, Final

# Rutas de trabajo
CARPETA_DATOS: Final[Path] = Path("datos")
ARCHIVO_JSON: Final[Path] = CARPETA_DATOS / "configuraciones_laboratorio.json"
ENCODING: Final[str] = "utf-8"


def preparar_directorio() -> None:
    """Asegura la existencia de la carpeta de trabajo."""
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)


# ============================================================================
# OPERACIONES FUNDAMENTALES DE LECTURA Y ESCRITURA JSON
# ============================================================================

def guardar_json(datos: Any, ruta: Path = ARCHIVO_JSON) -> bool:
    """Serializa y escribe una estructura de datos Python en un archivo JSON."""
    preparar_directorio()
    try:
        with ruta.open("w", encoding=ENCODING) as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        print(f"✅ Estructura serializada exitosamente en '{ruta.name}'.")
        return True
    except Exception as error:
        print(f"❌ Error al guardar JSON en '{ruta}': {error}")
        return False


def cargar_json(ruta: Path = ARCHIVO_JSON) -> Any:
    """Lee y deserializa un archivo JSON. Retorna None en caso de fallo o ausencia."""
    if not ruta.exists():
        print(f"⚠️ El archivo '{ruta.name}' no existe.")
        return None

    try:
        with ruta.open("r", encoding=ENCODING) as archivo:
            return json.load(archivo)
    except json.JSONDecodeError as error:
        print(f"❌ Error sintáctico en JSON ('{ruta.name}'): El archivo está corrompido o vacío. Detalle: {error}")
        return None
    except PermissionError:
        print(f"❌ Permisos insuficientes para acceder a '{ruta.name}'.")
        return None


# ============================================================================
# PRÁCTICA CON CADENAS JSON (dumps / loads)
# ============================================================================

def demostrar_conversion_strings() -> None:
    """Demuestra el uso de json.dumps() y json.loads()."""
    print("\n--- DEMOSTRACIÓN DE json.dumps() Y json.loads() ---")

    # Objeto Python (Diccionario con varios tipos de datos)
    equipo_python = {
        "id_laboratorio": "A306",
        "docente_cargo": "Profesor Taller II",
        "estaciones_activas": 15,
        "software_instalado": ["Python 3.13", "VS Code", "Jupyter", "Git"],
        "requiere_mantenimiento": False,
        "parametros_red": {
            "ip_gateway": "192.168.1.1",
            "mascara": "255.255.255.0",
        },
    }

    # 1. Python dict -> JSON string (json.dumps)
    cadena_json = json.dumps(equipo_python, indent=2, ensure_ascii=False)
    print("1. Objeto Python convertido a Cadena JSON (json.dumps):")
    print(cadena_json)

    # 2. JSON string -> Python dict (json.loads)
    objeto_reconstruido = json.loads(cadena_json)
    print("\n2. Cadena JSON reconstruida a Diccionario Python (json.loads):")
    print(f"Tipo resultante: {type(objeto_reconstruido).__name__}")
    print(f"Docente a cargo: {objeto_reconstruido['docente_cargo']}")
    print(f"Primer software: {objeto_reconstruido['software_instalado'][0]}")


# ============================================================================
# SISTEMA DE GESTIÓN DE CONFIGURACIONES ANIDADAS
# ============================================================================

def inicializar_configuracion_default() -> None:
    """Crea una estructura inicial de configuración de laboratorio si no existe."""
    if not ARCHIVO_JSON.exists():
        config_inicial = {
            "curso": "Taller de Programación II",
            "periodo": "II° Semestre 2026",
            "laboratorios": [
                {
                    "codigo": "A306",
                    "capacidad": 30,
                    "equipos_disponibles": 25,
                    "guias_completadas": ["Guia 1 TXT", "Guia 2 CSV"],
                },
                {
                    "codigo": "A308",
                    "capacidad": 25,
                    "equipos_disponibles": 20,
                    "guias_completadas": ["Guia 1 TXT"],
                },
            ],
            "contador_sesiones": 1,
        }
        guardar_json(config_inicial, ARCHIVO_JSON)


def agregar_guia_completada(codigo_lab: str, nombre_guia: str) -> bool:
    """Busca un laboratorio en la estructura JSON y anexa una guía completada."""
    config = cargar_json(ARCHIVO_JSON)
    if config is None:
        print("❌ No se pudo cargar la configuración.")
        return False

    laboratorio_encontrado = False
    for lab in config.get("laboratorios", []):
        if lab["codigo"].upper() == codigo_lab.upper():
            if nombre_guia not in lab["guias_completadas"]:
                lab["guias_completadas"].append(nombre_guia)
                laboratorio_encontrado = True
                print(f"✅ Guía '{nombre_guia}' agregada al Lab {codigo_lab}.")
            else:
                print(f"ℹ️ La guía '{nombre_guia}' ya estaba registrada en el Lab {codigo_lab}.")
                return True
            break

    if not laboratorio_encontrado:
        print(f"❌ Laboratorio {codigo_lab} no encontrado.")
        return False

    # Incrementar contador global de sesiones
    config["contador_sesiones"] = config.get("contador_sesiones", 0) + 1

    # Sincronizar cambios en disco
    return guardar_json(config, ARCHIVO_JSON)


def ejecutar_practica_json() -> None:
    """Ejecuta la suite de verificación de JSON."""
    print("🚀 INICIANDO PRÁCTICA DE SERIALIZACIÓN JSON...\n")

    # 1. Probar conversiones en memoria
    demostrar_conversion_strings()

    # 2. Inicializar y modificar JSON en disco
    print("\n--- PRÁCTICA DE MANIPULACIÓN EN DISCO ---")
    inicializar_configuracion_default()
    agregar_guia_completada("A306", "Guia 3 JSON & Excepciones")

    # 3. Leer estado final
    config_final = cargar_json(ARCHIVO_JSON)
    print("\n📋 Estado Final del Archivo JSON en Disco:")
    print(json.dumps(config_final, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    ejecutar_practica_json()
