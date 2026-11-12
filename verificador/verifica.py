"""Verificador del curs de Git de la Rocinante.

Ús (des de la carpeta del repositori):

    python verifica.py NN

Comprova l'estat del repositori per al pas NN i mostra cada criteri com a
[OK] o [FALLA]. No modifica mai el repositori: només el llegeix.

Codis de sortida: 0 si se superen tots els criteris, 1 si en falla algun,
2 si no es pot fer la verificació (no hi ha git, no és un repositori o el
pas no existeix).
"""

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPOSITORI_GUIA = "gitlab.com/fp-dev-academy/git-rocinante"
URL_GUIA_SSH = "git@gitlab.com:fp-dev-academy/git-rocinante.git"

# L'omple el generador amb tots els tags del curs.
TAGS_DEL_CURS: tuple[str, ...] = ()


class ErrorEntorn(Exception):
    """No es pot fer la verificació (codi de sortida 2)."""


@dataclass
class Resultat:
    ok: bool
    criteri: str
    pista: str = ""


def criteri(ok: bool, text: str, pista: str) -> Resultat:
    return Resultat(ok, text, "" if ok else pista)


# --- Accés a git (només lectura) ---------------------------------------

def git(*args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", "-c", "core.quotepath=off", *args],
            capture_output=True, encoding="utf-8",
        )
    except FileNotFoundError:
        raise ErrorEntorn("No es troba git. Comprova que Git for Windows està instal·lat.")


def sortida(*args: str) -> str:
    """Sortida d'una ordre de git, o "" si falla."""
    resultat = git(*args)
    return resultat.stdout.strip() if resultat.returncode == 0 else ""


def config(clau: str) -> str:
    return sortida("config", "--get", clau)


def normalitza_url(url: str) -> str:
    """Converteix una URL SSH o HTTPS en 'host/ruta', sense '.git' final."""
    url = url.strip().lower()
    coincidencia = (re.match(r"^(?:ssh://)?git@([^:/]+)[:/](.+)$", url)
                    or re.match(r"^https?://([^/]+)/(.+)$", url))
    if coincidencia is None:
        return url
    host, ruta = coincidencia.groups()
    ruta = ruta.rstrip("/")
    if ruta.endswith(".git"):
        ruta = ruta[:-4]
    return f"{host}/{ruta}"


def es_ssh(url: str) -> bool:
    return url.startswith(("git@", "ssh://"))


# --- Passos --------------------------------------------------------------

PASSOS = {}


def pas(numero: str, titol: str):
    def registra(funcio):
        PASSOS[numero] = (titol, funcio)
        return funcio
    return registra


@pas("00", "Embarcament")
def verifica_pas_00(repo: Path) -> list[Resultat]:
    nom = config("user.name")
    correu = config("user.email")
    origin = config("remote.origin.url")
    upstream = config("remote.upstream.url")
    tags = set(sortida("tag", "--list").splitlines())
    falten = [t for t in TAGS_DEL_CURS if t not in tags]
    return [
        criteri(bool(nom), "user.name definit",
                'git config --global user.name "El teu nom i cognom"'),
        criteri(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correu) is not None,
                "user.email definit amb format de correu",
                'git config --global user.email "el-teu-correu@exemple.cat"'),
        criteri(bool(config("core.editor")), "core.editor definit",
                "git config --global core.editor notepad"),
        criteri(bool(origin) and normalitza_url(origin) != REPOSITORI_GUIA,
                "origin apunta al teu fork, no al repositori guia",
                "Has clonat el repositori guia? Vegeu PISTES.md: git remote set-url origin ..."),
        criteri(es_ssh(origin), "origin fa servir SSH (git@...)",
                "git remote set-url origin git@gitlab.com:<usuari>/git-rocinante.git"),
        criteri(normalitza_url(upstream) == REPOSITORI_GUIA,
                "upstream apunta al repositori guia",
                f"git remote add upstream {URL_GUIA_SSH}"),
        criteri(not falten, "hi ha tots els tags del curs en local",
                f"Falten {', '.join(falten)}. Prova: git fetch origin --tags"),
        criteri(sys.version_info >= (3, 12),
                f"Python 3.12 o superior (tens {sys.version.split()[0]})",
                "Instal·la una versió de Python més recent."),
    ]


# --- Programa principal ----------------------------------------------------

def arrel_del_repositori() -> Path:
    resultat = git("rev-parse", "--show-toplevel")
    if resultat.returncode != 0:
        raise ErrorEntorn("Aquesta carpeta no és un repositori de Git. "
                          "Executa verifica.py des de la carpeta git-rocinante.")
    return Path(resultat.stdout.strip())


def main(arguments: list[str]) -> int:
    if len(arguments) != 1:
        raise ErrorEntorn("Ús: python verifica.py NN   (per exemple: python verifica.py 00)")
    numero = arguments[0].zfill(2)
    if numero not in PASSOS:
        disponibles = ", ".join(sorted(PASSOS))
        raise ErrorEntorn(f"El pas {arguments[0]} no existeix en aquesta versió de "
                          f"verifica.py. Passos disponibles: {disponibles}.")
    repo = arrel_del_repositori()
    titol, funcio = PASSOS[numero]
    print(f"Pas {numero} - {titol}\n")
    resultats = funcio(repo)
    for resultat in resultats:
        print(f"[{'OK' if resultat.ok else 'FALLA'}] {resultat.criteri}")
        if resultat.pista:
            print(f"        Pista: {resultat.pista}")
    superats = sum(r.ok for r in resultats)
    print(f"\n{superats} de {len(resultats)} criteris superats.")
    if superats == len(resultats):
        print("Pas superat. Bona feina, tripulant.")
        return 0
    print("Encara no. Revisa les pistes o llegeix PISTES.md.")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except ErrorEntorn as error:
        print(error)
        sys.exit(2)
