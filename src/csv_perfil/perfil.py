"""Lógica principal para perfilar archivos CSV.

Todo el procesamiento usa solo la biblioteca estándar de Python, por lo
que el proyecto no tiene dependencias externas en tiempo de ejecución.
"""

from __future__ import annotations

import csv
import statistics
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

VALORES_NULOS = frozenset({"", "na", "n/a", "null", "none", "nan", "-"})


@dataclass
class PerfilColumna:
    """Resumen estadístico de una columna."""

    nombre: str
    total: int = 0
    nulos: int = 0
    valores: list[str] = field(default_factory=list, repr=False)

    @property
    def no_nulos(self) -> int:
        return self.total - self.nulos

    @property
    def porcentaje_nulos(self) -> float:
        return round(100 * self.nulos / self.total, 2) if self.total else 0.0

    @property
    def unicos(self) -> int:
        return len(set(self.valores))

    @property
    def numericos(self) -> list[float]:
        return [n for n in (_a_numero(v) for v in self.valores) if n is not None]

    @property
    def tipo(self) -> str:
        """Infiere el tipo dominante: 'vacío', 'numérico' o 'texto'."""
        if not self.valores:
            return "vacío"
        if len(self.numericos) == len(self.valores):
            return "numérico"
        return "texto"

    def a_dict(self) -> dict:
        """Devuelve el perfil como diccionario serializable a JSON."""
        datos: dict = {
            "columna": self.nombre,
            "tipo": self.tipo,
            "total": self.total,
            "nulos": self.nulos,
            "porcentaje_nulos": self.porcentaje_nulos,
            "unicos": self.unicos,
        }
        if self.tipo == "numérico":
            nums = self.numericos
            datos.update(
                {
                    "minimo": min(nums),
                    "maximo": max(nums),
                    "media": round(statistics.fmean(nums), 4),
                    "mediana": statistics.median(nums),
                }
            )
        return datos


def _a_numero(valor: str) -> float | None:
    """Convierte un texto a número aceptando coma o punto decimal."""
    limpio = valor.strip().replace(" ", "")
    if "," in limpio and "." not in limpio:
        limpio = limpio.replace(",", ".")
    try:
        return float(limpio)
    except ValueError:
        return None


def es_nulo(valor: str | None) -> bool:
    """Indica si un valor debe considerarse nulo."""
    return valor is None or valor.strip().lower() in VALORES_NULOS


def perfilar_filas(filas: Iterable[dict[str, str]], columnas: list[str]) -> list[PerfilColumna]:
    """Calcula el perfil de cada columna a partir de filas ya leídas."""
    perfiles = {c: PerfilColumna(nombre=c) for c in columnas}
    for fila in filas:
        for columna in columnas:
            perfil = perfiles[columna]
            perfil.total += 1
            valor = fila.get(columna)
            if es_nulo(valor):
                perfil.nulos += 1
            else:
                perfil.valores.append(valor.strip())
    return list(perfiles.values())


def perfilar_csv(ruta: str | Path, separador: str | None = None, codificacion: str = "utf-8") -> list[PerfilColumna]:
    """Lee un archivo CSV y devuelve el perfil de sus columnas.

    Si no se indica ``separador``, se intenta detectar automáticamente.
    """
    ruta = Path(ruta)
    with ruta.open(newline="", encoding=codificacion) as archivo:
        muestra = archivo.read(4096)
        archivo.seek(0)
        if separador is None:
            try:
                separador = csv.Sniffer().sniff(muestra, delimiters=",;\t|").delimiter
            except csv.Error:
                separador = ","
        lector = csv.DictReader(archivo, delimiter=separador)
        columnas = list(lector.fieldnames or [])
        return perfilar_filas(lector, columnas)
