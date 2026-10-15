"""Interfaz de línea de comandos de csv-perfil."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .perfil import PerfilColumna, perfilar_csv


def _tabla(perfiles: list[PerfilColumna]) -> str:
    encabezados = ["columna", "tipo", "total", "nulos", "% nulos", "únicos", "mín", "máx", "media"]
    filas = []
    for p in perfiles:
        d = p.a_dict()
        filas.append(
            [
                d["columna"],
                d["tipo"],
                str(d["total"]),
                str(d["nulos"]),
                f'{d["porcentaje_nulos"]}%',
                str(d["unicos"]),
                str(d.get("minimo", "")),
                str(d.get("maximo", "")),
                str(d.get("media", "")),
            ]
        )
    anchos = [max(len(x) for x in col) for col in zip(encabezados, *filas)]
    linea = lambda celdas: "  ".join(c.ljust(a) for c, a in zip(celdas, anchos))  # noqa: E731
    separador = "  ".join("-" * a for a in anchos)
    return "\n".join([linea(encabezados), separador, *(linea(f) for f in filas)])


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv-perfil",
        description="Genera un perfil rápido (tipos, nulos, únicos y estadísticas) de un archivo CSV.",
    )
    parser.add_argument("archivo", help="Ruta al archivo CSV")
    parser.add_argument("-s", "--separador", help="Separador de columnas (por defecto se detecta)")
    parser.add_argument("-e", "--codificacion", default="utf-8", help="Codificación del archivo (por defecto utf-8)")
    parser.add_argument("--json", action="store_true", help="Imprime el resultado en formato JSON")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    try:
        perfiles = perfilar_csv(args.archivo, separador=args.separador, codificacion=args.codificacion)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{args.archivo}'.", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print("Error: no se pudo leer el archivo. Prueba con --codificacion latin-1.", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps([p.a_dict() for p in perfiles], ensure_ascii=False, indent=2))
    else:
        print(_tabla(perfiles))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
