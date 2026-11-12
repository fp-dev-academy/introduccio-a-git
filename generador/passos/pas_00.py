"""Pas 00 - Embarcament."""

from git_utils import Repo
from passos import llegeix

# Al primer commit perquè l'alumnat treballa a Windows 11 (vegeu CLAUDE.md).
GITATTRIBUTES = "* text=auto eol=lf\n"


def build(repo: Repo) -> None:
    repo.escriu(".gitattributes", GITATTRIBUTES)
    repo.escriu("LICENSE", llegeix("pas_00", "LICENSE"))
    repo.escriu("LICENSE-docs", llegeix("pas_00", "LICENSE-docs"))
    repo.commit("chore: inicia el diari de bord de la Rocinante", "holden")
