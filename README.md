# Taller de Programación II — Universidad San Sebastián

> **Asignatura de Programación en Python Orientada a la Gestión y Persistencia de Archivos: TXT, CSV y JSON**  
> Repositorio público oficial de material docente, apuntes maestros teóricos, cuadernos Jupyter interactivos y módulos de referencia resueltos — *Universidad San Sebastián · Sede Patagonia*.

[![Python 3.13](https://img.shields.io/badge/Python-3.13-4B8BBE?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter Notebooks](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-D4AF37?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Universidad San Sebastián](https://img.shields.io/badge/USS-Sede%20Patagonia-00205B)](https://www.uss.cl/)
[![moises-inc](https://img.shields.io/badge/moises--inc-Taller--Programacion--II-00205B)](https://github.com/moises-inc/Taller-Programacion-II)

---

## Descripción General

La asignatura **Taller de Programación II** profundiza en los mecanismos de **persistencia de datos** mediante el manejo estructurado de archivos en lenguaje Python. Permite la transición desde modelos en memoria volátil RAM hacia sistemas de información duraderos mediante entrada/salida (I/O) en disco físico.

Este repositorio consolida la versión pública sanitizada de los recursos académicos del curso:
* **Apuntes Teóricos Maestros:** Síntesis rigurosa con trazabilidad de fuentes (Cátedra USS, Texto Guía y Referencias de Estándares).
* **Guías Docentes Originales:** Enunciados formales provistos en formatos PDF y DOCX.
* **Módulos Python de Referencia (.py):** Soluciones modulares tipadas con arquitectura defensiva (`try-except`, `pathlib`, `csv.writer`).
* **Cuadernos Jupyter Interactivos (.ipynb):** Pautas ejecutadas con celdas pre-renderizadas y esquemas v4 validados.

### Estructura Curricular por Unidades

| Unidad | Áreas de Dominio Técnico |
| :--- | :--- |
| **Unidad 0 — Repaso y Fundamentos** | Consolidación de estructuras de datos en memoria: variables, condicionales, ciclos, listas, diccionarios, funciones y modularización. |
| **Unidad 1 — Persistencia de Archivos (TXT / CSV / JSON)** | Flujos de entrada/salida (*I/O Buffering*), administradores de contexto (`with open`), modos de apertura (`r`, `w`, `a`), punteros (`seek`/`tell`), operaciones CRUD atómicas, estándar IETF RFC 4180, serialización de datos y patrones de procesamiento masivo (corte de control y apareo). |

---

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Organización del Repositorio](#organización-del-repositorio)
- [Apuntes Teóricos Maestros](#apuntes-teóricos-maestros)
- [Guías Docentes Originales](#guías-docentes-originales)
- [Módulos y Soluciones en Python (.py)](#módulos-y-soluciones-en-python-py)
- [Índice de Cuadernos Jupyter (.ipynb)](#índice-de-cuadernos-jupyter-ipynb)
- [Datos de Ejemplo e Infraestructura](#datos-de-ejemplo-e-infraestructura)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Licencia](#licencia)

---

## Organización del Repositorio

```
Taller-Programacion-II/
├── LICENSE                            # Licencia Abierta MIT
├── README.md                          # Portal Principal de Documentación
├── .gitignore                         # Exclusión de artefactos locales y cachés
├── Apuntes/                           # Notas Maestras Teóricas (Markdown Sanitizado)
│   ├── Repaso_Programacion_I.md       #    • Unidad 0: Fundamentos y Estructuras Base
│   ├── Manejo_Archivos_Python.md      #    • Unidad 1A: Archivos TXT, Buffer y CRUD Atómico
│   └── Archivos_CSV_Python.md         #    • Unidad 1B: Persistencia CSV (RFC 4180) y DictWriter
├── Guias_y_Ejercicios/                # Enunciados Oficiales y Módulos de Código
│   ├── Guias_Docente/                 #    • Enunciados en PDF y DOCX
│   ├── Soluciones_Python/             #    • Módulos Python (.py) resueltos y tipados
│   └── datos/                         #    • Conjuntos de datos de prueba
└── Entrenamiento_Laboratorio/        # Cuadernos Jupyter Interactivos (.ipynb)
    ├── datos/                         #    • Archivos de entrada/salida de práctica
    ├── Solucion_Guia_Basica_Paso_a_Paso_Archivos_TXT.ipynb
    ├── Solucion_Guia_Practica_Ejercicios_Archivos_TXT.ipynb
    ├── Solucion_Guia_Integral_Ejercicios_Unidad1.ipynb
    ├── Solucion_Guia_CSV_Maquinas_Industriales.ipynb
    ├── Solucion_Ejercicios_Extra_CSV.ipynb
    ├── Solucion_Guia_Manejo_Archivos_Produccion.ipynb
    ├── Solucion_Actividad_Registro_Ventas_Archivos.ipynb
    ├── Solucion_Simulacro_Control1_Laboratorio.ipynb
    └── Cuaderno_Entrenamiento_Solemnes_TallerII.ipynb
```

---

## Apuntes Teóricos Maestros

Notas de estudio integrales desarrolladas bajo el estándar de trazabilidad de fuentes:

| Apunte Maestro | Descripción Técnica |
| :--- | :--- |
| [Repaso_Programacion_I.md](Apuntes/Repaso_Programacion_I.md) | Repaso estructural de variables, condicionales, ciclos `while`/`for`, funciones con retornos explícitos y preparación para persistencia. |
| [Manejo_Archivos_Python.md](Apuntes/Manejo_Archivos_Python.md) | Gestión exhaustiva de archivos TXT, jerarquía de memoria, descriptores de archivo, protocolos Context Manager, modos de apertura, corte de control y serialización JSON. |
| [Archivos_CSV_Python.md](Apuntes/Archivos_CSV_Python.md) | Guía maestra de persistencia en CSV: análisis léxico con `split()`, módulo `csv` (`reader`, `writer`), abstracción nominal con `DictReader`/`DictWriter`, estándar RFC 4180 y prevención de CSV Injection. |

---

## Guías Docentes Originales

Enunciados académicos oficiales disponibles en `Guias_y_Ejercicios/Guias_Docente/`:

- `Guia_Basica_paso_a_paso_Manejo_Archivos_TXT_Python` (Formatos PDF y DOCX)
- `Guia_Practica_Ejercicios_Archivos_TXT_Python` (Formatos PDF y DOCX)
- `Guia Integral Ejercicios_Unidad1` (Formato PDF)
- `Guia_Ejercicio_Integral_CSV_Maquinas_Industriales` (Formatos PDF y DOCX)
- `2. Ejercicios Extra CSV` (Ejercicios 2.6 Productos, 2.7 Sensores y 2.8 Mantenciones - PDF)
- `Guia_Ejercicios_Manejo_Archivos_Produccion_Python` (Formatos PDF y DOCX)
- `Actividad_Registro_Ventas_Archivos_Python` (Formato PDF)

---

## Módulos y Soluciones en Python (.py)

Módulos de referencia implementados con tipado explícito e ingeniería defensiva en `Guias_y_Ejercicios/Soluciones_Python/`:

- `guia_maquinas_industriales_csv.py` — Registro de condiciones operacionales de máquinas industriales en CSV con evaluación automática de estado.
- `ejercicios_extra_csv.py` — Resolución unificada de ejercicios de productos, sensores (con rangos físicos) y mantenciones con marca temporal (`datetime`).
- `guia_integral_unidad1.py` — Sistema modular de gestión de clientes en CSV con validaciones de integridad de negocio.
- `programa_produccion.py` — Sistema CRUD persistente de órdenes de producción industrial (TXT delimitado).
- `practica_archivos_basica.py` — Funciones fundamentales de lectura, escritura y anexión en archivos planos TXT.
- `practica_intensiva_io_txt_csv.py` — Práctica intensiva de flujos de entrada/salida y parsing en TXT y CSV.
- `practica_serializacion_json.py` — Módulo de serialización y deserialización estructurada con formato JSON.
- `simulacro_control1_laboratorio.py` — Módulo resuelto del simulacro de evaluación práctica de laboratorio.

---

## Índice de Cuadernos Jupyter (.ipynb)

Cuadernos interactivos formateados formalmente en `Entrenamiento_Laboratorio/`:

| Cuaderno Jupyter | Tema y Descripción Técnica |
| :--- | :--- |
| [Solucion_Guia_Basica_Paso_a_Paso_Archivos_TXT.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_Basica_Paso_a_Paso_Archivos_TXT.ipynb) | Guía básica de 11 ejercicios paso a paso para manipulación de archivos TXT. |
| [Solucion_Guia_Practica_Ejercicios_Archivos_TXT.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_Practica_Ejercicios_Archivos_TXT.ipynb) | Guía práctica de 15 ejercicios sobre persistencia en texto plano. |
| [Solucion_Guia_Integral_Ejercicios_Unidad1.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_Integral_Ejercicios_Unidad1.ipynb) | Sistema integral de clientes con lectura/escritura en CSV. |
| [Solucion_Guia_CSV_Maquinas_Industriales.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_CSV_Maquinas_Industriales.ipynb) | Evaluación automática y resumen estadístico de máquinas industriales. |
| [Solucion_Ejercicios_Extra_CSV.ipynb](Entrenamiento_Laboratorio/Solucion_Ejercicios_Extra_CSV.ipynb) | Resolución de ejercicios docentes 2.6 (Productos), 2.7 (Sensores) y 2.8 (Mantenciones). |
| [Solucion_Guia_Manejo_Archivos_Produccion.ipynb](Entrenamiento_Laboratorio/Solucion_Guia_Manejo_Archivos_Produccion.ipynb) | Sistema de control de producción con archivo TXT delimitado por punto y coma. |
| [Solucion_Actividad_Registro_Ventas_Archivos.ipynb](Entrenamiento_Laboratorio/Solucion_Actividad_Registro_Ventas_Archivos.ipynb) | Registro de ventas por lotes fijos y resumen acumulado. |
| [Solucion_Simulacro_Control1_Laboratorio.ipynb](Entrenamiento_Laboratorio/Solucion_Simulacro_Control1_Laboratorio.ipynb) | Pauta oficial del simulacro de evaluación de laboratorio. |
| [Cuaderno_Entrenamiento_Solemnes_TallerII.ipynb](Entrenamiento_Laboratorio/Cuaderno_Entrenamiento_Solemnes_TallerII.ipynb) | Cuaderno de entrenamiento con 12 ejercicios de rastreo de código (*Code Tracing*) para evaluaciones escritas. |

---

## Datos de Ejemplo e Infraestructura

En las carpetas `datos/` de cada directorio de soluciones se incluyen los archivos de prueba requeridos (`produccion.txt`, `registro.txt`, `ventas.txt`, `registro_ventas.txt`).  
Cada script y cuaderno verifica la presencia de su archivo de datos y lo genera automáticamente en caso de no existir, asegurando que el repositorio sea **100% ejecutable e independiente**.

---

## Instalación y Ejecución

### 1. Clonar el Repositorio

```bash
git clone https://github.com/moises-inc/Taller-Programacion-II.git
cd Taller-Programacion-II
```

### 2. Ejecutar Módulos Python

```bash
cd Guias_y_Ejercicios/Soluciones_Python
python3 programa_produccion.py
python3 guia_maquinas_industriales_csv.py
```

### 3. Ejecutar Cuadernos Jupyter

```bash
cd Entrenamiento_Laboratorio
jupyter notebook Solucion_Guia_CSV_Maquinas_Industriales.ipynb
```

---

## Licencia

Este proyecto y sus materiales educativos se distribuyen bajo la **Licencia MIT** — © 2026 Moisés Vera / moises-inc. Consulte el archivo [LICENSE](LICENSE) para mayores detalles.
