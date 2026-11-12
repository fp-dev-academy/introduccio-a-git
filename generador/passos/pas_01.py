"""Pas 01 - Primera entrada al diari.

A pas-01 no hi ha .gitignore: els fitxers a ignorar els genera l'alumne.
Després del tag, Amos afegeix el .gitignore a main (ESPECIFICACIO.md, 3).
"""

from git_utils import Repo
from passos import copia, verifica

GITIGNORE_AMOS = """\
# Python
__pycache__/
*.pyc
.venv/

# PyCharm
.idea/
"""


def build(repo: Repo) -> None:
    copia(repo, "pas_01", "REPTE.md", "PISTES.md")
    repo.escriu("verifica.py", verifica("01"))
    repo.commit("feat: afegeix el repte i el verificador del pas 01", "naomi")
    repo.tag("pas-01", "Pas 01 - Primera entrada al diari", "holden")

    repo.escriu(".gitignore", GITIGNORE_AMOS)
    repo.commit("chore: ignora la brossa", "amos")
