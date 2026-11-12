"""Pas 00 - Embarcament.

Construeix l'estat inicial del diari de bord: llicències, aplicació,
README, el repte del pas 00 i verifica.py.
"""

from git_utils import Repo
from passos import copia, llegeix, verifica

# Al primer commit perquè l'alumnat treballa a Windows 11 (vegeu CLAUDE.md).
GITATTRIBUTES = "* text=auto eol=lf\n"


def build(repo: Repo) -> None:
    repo.escriu(".gitattributes", GITATTRIBUTES)
    repo.escriu("LICENSE", llegeix("pas_00", "LICENSE"))
    repo.escriu("LICENSE-docs", llegeix("pas_00", "LICENSE-docs"))
    repo.commit("chore: inicia el diari de bord de la Rocinante", "holden")

    copia(repo, "pas_00", "rocinante/__init__.py", "rocinante/combustible.py",
          "tests/test_combustible.py")
    repo.commit("feat: calcula el consum de massa de reacció", "naomi")

    copia(repo, "pas_00", "rocinante/navegacio.py", "tests/test_navegacio.py")
    repo.commit("feat: calcula el temps de trajecte", "alex")

    copia(repo, "pas_00", "rocinante/tripulacio.py", "rocinante/__main__.py")
    repo.commit("feat: afegeix la tripulació i la línia d'ordres", "holden")

    copia(repo, "pas_00", "README.md")
    repo.commit("docs: explica com funciona el diari de bord", "holden")

    copia(repo, "pas_00", "REPTE.md", "PISTES.md")
    repo.escriu("verifica.py", verifica("00"))
    repo.commit("feat: afegeix el repte i el verificador del pas 00", "naomi")
    repo.tag("pas-00", "Pas 00 - Embarcament", "holden")
