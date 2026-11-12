"""Passos del curs. Cada mòdul té una funció build(repo) que hi afegeix commits i tags."""

import hashlib
import re
from pathlib import Path

from git_utils import Repo

ARREL = Path(__file__).resolve().parents[2]
CONTINGUT = ARREL / "contingut"
VERIFICADOR = ARREL / "verificador" / "verifica.py"

# Tots els tags del curs. En afegir un pas, cal afegir-hi el seu tag:
# test_generador comprova que coincideixen amb els del repositori generat.
TAGS_DEL_CURS = ("pas-00", "pas-01", "pas-02", "pas-03", "pas-04", "pas-05", "v1.0", "pas-06")

# Respostes esperades de cada pas ("NN.clau" -> SHA-256 dels valors acceptats,
# ja normalitzats). Les registren els passos durant la generació.
RESPOSTES: dict[str, tuple[str, ...]] = {}

_MARCA_TAGS = "TAGS_DEL_CURS: tuple[str, ...] = ()"
_MARCA_RESPOSTES = "RESPOSTES: dict[str, tuple[str, ...]] = {}"


def llegeix(pas: str, nom: str) -> str:
    """Retorna el text d'un fitxer de contingut/<pas>/<nom>."""
    return (CONTINGUT / pas / nom).read_text(encoding="utf-8")


def copia(repo: Repo, pas: str, *rutes: str) -> None:
    """Escriu al repositori els fitxers de contingut/<pas>/ amb la mateixa ruta."""
    for ruta in rutes:
        repo.escriu(ruta, llegeix(pas, ruta))


_BLOC = re.compile(r"^# >>> pas (\d\d)\n.*?^# <<< pas \1\n", re.M | re.S)


def modifica(repo: Repo, ruta: str, vell: str, nou: str) -> None:
    """Substitueix un fragment que ha d'aparèixer exactament una vegada al fitxer."""
    text = (repo.directori / ruta).read_text(encoding="utf-8")
    if text.count(vell) != 1:
        raise ValueError(f"{ruta}: el fragment ha d'aparèixer exactament una vegada: {vell!r}")
    repo.escriu(ruta, text.replace(vell, nou))


def registra_resposta(pas: str, clau: str, *valors_normalitzats: str) -> None:
    """Desa el SHA-256 dels valors acceptats per a una pregunta d'un pas."""
    RESPOSTES[f"{pas}.{clau}"] = tuple(
        hashlib.sha256(v.encode("utf-8")).hexdigest() for v in valors_normalitzats)


def verifica(fins_a: str) -> str:
    """Text de verifica.py per al repositori guia, amb els passos fins a fins_a.

    Els passos posteriors (blocs `# >>> pas NN` ... `# <<< pas NN`)
    s'esborren, i s'hi escriu la llista de tags del curs.
    """
    text = VERIFICADOR.read_text(encoding="utf-8")
    for marca in (_MARCA_TAGS, _MARCA_RESPOSTES):
        if text.count(marca) != 1:
            raise ValueError(f"verifica.py ha de contenir exactament una vegada: {marca}")
    if len(re.findall(r"^# >>> pas ", text, re.M)) != len(_BLOC.findall(text)):
        raise ValueError("verifica.py té un bloc de pas sense tancar")
    text = _BLOC.sub(lambda m: m.group(0) if m.group(1) <= fins_a else "", text)
    text = text.replace(_MARCA_RESPOSTES,
                        f"RESPOSTES: dict[str, tuple[str, ...]] = {dict(sorted(RESPOSTES.items()))!r}")
    return text.replace(_MARCA_TAGS, f"TAGS_DEL_CURS: tuple[str, ...] = {TAGS_DEL_CURS!r}")
