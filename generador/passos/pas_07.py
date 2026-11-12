"""Pas 07 - Informe a la flota.

Només afegeix el repte i el verificador. Les branques de treball les puja
l'alumne; la merge request i la revisió les comprova el docent a GitLab.
"""

from git_utils import Repo
from passos import copia, verifica


def build(repo: Repo) -> None:
    copia(repo, "pas_07", "REPTE.md", "PISTES.md")
    repo.escriu("verifica.py", verifica("07"))
    repo.commit("feat: afegeix el repte i el verificador del pas 07", "naomi")
    repo.tag("pas-07", "Pas 07 - Informe a la flota", "holden")
