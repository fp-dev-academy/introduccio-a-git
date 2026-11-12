"""Passos del curs. Cada mòdul té una funció build(repo) que hi afegeix commits i tags."""

from pathlib import Path

CONTINGUT = Path(__file__).resolve().parents[2] / "contingut"


def llegeix(pas: str, nom: str) -> str:
    """Retorna el text d'un fitxer de contingut/<pas>/<nom>."""
    return (CONTINGUT / pas / nom).read_text(encoding="utf-8")
