# csv-perfil

[![CI](https://github.com/johnbyronA/csv-perfil/actions/workflows/ci.yml/badge.svg)](https://github.com/johnbyronA/csv-perfil/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-green.svg)](LICENSE)

Herramienta de línea de comandos, **sin dependencias externas**, que genera en segundos un perfil de cualquier archivo CSV: tipo de dato inferido, valores nulos, valores únicos y estadísticas básicas de las columnas numéricas.

> *English:* A zero-dependency Python CLI that profiles CSV files (inferred types, nulls, unique values and basic stats).

## ¿Por qué?

Antes de analizar un archivo es útil saber qué contiene: ¿cuántos vacíos tiene cada columna?, ¿cuáles son numéricas?, ¿hay valores fuera de rango? `csv-perfil` responde eso sin abrir Excel ni escribir código.

## Características

- Detección automática del separador (`,` `;` `|` o tabulación).
- Reconoce nulos comunes: vacío, `NA`, `N/A`, `null`, `None`, `NaN`, `-`.
- Acepta decimales con coma (`3,5`) o punto (`3.5`).
- Salida en tabla legible o en JSON (`--json`) para integrarla con otras herramientas.
- Solo usa la biblioteca estándar de Python.

## Instalación

Requiere Python 3.9 o superior.

```bash
git clone https://github.com/johnbyronA/csv-perfil.git
cd csv-perfil
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -e .
```

## Uso

```bash
csv-perfil examples/ventas.csv
```

```text
columna          tipo      total  nulos  % nulos  únicos  mín     máx      media
---------------  --------  -----  -----  -------  ------  ------  -------  -------
fecha            texto     8      0      0.0%     7
producto         texto     8      0      0.0%     4
cantidad         numérico  8      1      12.5%    7       2.0     10.0     5.4286
precio_unitario  numérico  8      1      12.5%    4       1800.0  12500.0  6200.0
ciudad           texto     8      1      12.5%    4
```

Otras opciones:

```bash
csv-perfil datos.csv --json                 # salida en JSON
csv-perfil datos.csv -s ";"                 # forzar separador
csv-perfil datos.csv -e latin-1             # otra codificación
python -m csv_perfil datos.csv              # sin instalar el comando
```

También puede usarse como librería:

```python
from csv_perfil import perfilar_csv

for columna in perfilar_csv("examples/ventas.csv"):
    print(columna.a_dict())
```

## Estructura del proyecto

```text
csv-perfil/
├── src/csv_perfil/      # Código fuente del paquete
│   ├── perfil.py        # Lógica de perfilado
│   └── cli.py           # Interfaz de línea de comandos
├── tests/               # Pruebas con pytest
├── examples/            # Datos de ejemplo (ficticios)
└── .github/             # CI y plantillas de issues / PR
```

## Desarrollo

```bash
pip install -e ".[dev]"
pytest          # ejecutar pruebas
ruff check .    # revisar estilo
```

## Contribuir

¡Las contribuciones son bienvenidas! Revisa [CONTRIBUTING.md](CONTRIBUTING.md) y el [Código de Conducta](CODE_OF_CONDUCT.md).

## Seguridad

Para reportar una vulnerabilidad consulta [SECURITY.md](SECURITY.md).

## Licencia

Distribuido bajo la licencia MIT. Ver [LICENSE](LICENSE).
