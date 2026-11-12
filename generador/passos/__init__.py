"""Passos del curs. Cada mòdul té una funció build(repo) que hi afegeix commits i tags."""

from pathlib import Path

from git_utils import Repo

ARREL = Path(__file__).resolve().parents[2]
CONTINGUT = ARREL / "contingut"
VERIFICADOR = ARREL / "verificador" / "verifica.py"

# Tots els tags del curs. En afegir un pas, cal afegir-hi el seu tag:
# test_generador comprova que coincideixen amb els del repositori generat.
TAGS_DEL_CURS = ("pas-00",)

_MARCA_TAGS = "TAGS_DEL_CURS: tuple[str, ...] = ()"


def llegeix(pas: str, nom: str) -> str:
    """Retorna el text d'un fitxer de contingut/<pas>/<nom>."""
    return (CONTINGUT / pas / nom).read_text(encoding="utf-8")


def copia(repo: Repo, pas: str, *rutes: str) -> None:
    """Escriu al repositori els fitxers de contingut/<pas>/ amb la mateixa ruta."""
    for ruta in rutes:
        repo.escriu(ruta, llegeix(pas, ruta))


def verifica() -> str:
    """Text de verifica.py per al repositori guia, amb els tags del curs."""
    text = VERIFICADOR.read_text(encoding="utf-8")
    if text.count(_MARCA_TAGS) != 1:
        raise ValueError(f"verifica.py ha de contenir exactament una vegada: {_MARCA_TAGS}")
    return text.replace(_MARCA_TAGS, f"TAGS_DEL_CURS: tuple[str, ...] = {TAGS_DEL_CURS!r}")
