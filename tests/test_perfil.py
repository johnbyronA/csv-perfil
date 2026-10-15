import json
from pathlib import Path

import pytest

from csv_perfil import perfilar_csv, perfilar_filas
from csv_perfil.cli import main
from csv_perfil.perfil import _a_numero, es_nulo

EJEMPLO = Path(__file__).resolve().parent.parent / "examples" / "ventas.csv"


@pytest.mark.parametrize("valor", ["", "  ", "NA", "null", "None", "nan", "-"])
def test_es_nulo(valor):
    assert es_nulo(valor)


def test_no_es_nulo():
    assert not es_nulo("0")


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("10", 10.0), ("3,5", 3.5), ("1.25", 1.25), ("abc", None)],
)
def test_a_numero(texto, esperado):
    assert _a_numero(texto) == esperado


def test_perfilar_filas_numerico_y_texto():
    filas = [{"a": "1", "b": "x"}, {"a": "3", "b": ""}, {"a": "", "b": "x"}]
    a, b = perfilar_filas(filas, ["a", "b"])
    assert a.tipo == "numérico"
    assert a.nulos == 1
    assert a.a_dict()["media"] == 2.0
    assert b.tipo == "texto"
    assert b.unicos == 1
    assert b.porcentaje_nulos == pytest.approx(33.33)


def test_columna_vacia():
    (c,) = perfilar_filas([{"c": ""}], ["c"])
    assert c.tipo == "vacío"


def test_perfilar_csv_ejemplo():
    perfiles = {p.nombre: p for p in perfilar_csv(EJEMPLO)}
    assert perfiles["cantidad"].tipo == "numérico"
    assert perfiles["producto"].tipo == "texto"


def test_detecta_punto_y_coma(tmp_path):
    archivo = tmp_path / "datos.csv"
    archivo.write_text("x;y\n1;a\n2;b\n", encoding="utf-8")
    perfiles = perfilar_csv(archivo)
    assert [p.nombre for p in perfiles] == ["x", "y"]


def test_cli_json(capsys):
    assert main([str(EJEMPLO), "--json"]) == 0
    salida = json.loads(capsys.readouterr().out)
    assert salida[0]["columna"] == "fecha"


def test_cli_archivo_inexistente(capsys):
    assert main(["no_existe.csv"]) == 1
    assert "no se encontró" in capsys.readouterr().err
