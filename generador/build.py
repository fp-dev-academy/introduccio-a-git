"""Genera el repositori guia git-rocinante.

Ús: python generador/build.py --out <directori>

El directori de sortida s'esborra i es torna a crear (idempotent). El
generador no fa push: la publicació la fa el docent (ESPECIFICACIO.md, 6).
"""

import argparse
import shutil
from pathlib import Path

from git_utils import Repo
from passos import pas_00, pas_01

PASSOS = [pas_00, pas_01]


def genera(sortida: Path) -> None:
    if sortida.exists():
        shutil.rmtree(sortida)
    with Repo.crea(sortida) as repo:
        for pas in PASSOS:
            pas.build(repo)


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera el repositori guia git-rocinante.")
    parser.add_argument("--out", type=Path, required=True, help="directori de sortida")
    arguments = parser.parse_args()
    genera(arguments.out)
    print(f"Repositori generat a {arguments.out}")


if __name__ == "__main__":
    main()
