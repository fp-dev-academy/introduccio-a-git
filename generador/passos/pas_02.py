"""Pas 02 - La caixa negra.

Alex afegeix rumb_emergencia() i, tres commits després, Amos l'esborra.
Entremig, cap commit no toca navegacio.py (així `restore --source` no desfà
res més). Després del tag, Alex la recupera a main (ESPECIFICACIO.md, 3).
"""

from git_utils import Repo
from passos import copia, llegeix, modifica, registra_resposta, verifica

NAVEGACIO = "rocinante/navegacio.py"

# S'afegeix al final de navegacio.py, separada per dues línies en blanc.
RUMB_EMERGENCIA = (
    "\n\n"
    "def rumb_emergencia(rumb_perill):\n"
    '    """Rumb d\'emergència (en graus): el sentit contrari al del perill."""\n'
    "    return (rumb_perill + 180) % 360\n"
)


def build(repo: Repo) -> None:
    navegacio_sense_rumb = llegeix("pas_00", NAVEGACIO)
    navegacio_amb_rumb = navegacio_sense_rumb + RUMB_EMERGENCIA

    repo.escriu(NAVEGACIO, navegacio_amb_rumb)
    afegit = repo.commit("feat: afegeix el rumb d'emergència", "alex")

    modifica(repo, "rocinante/combustible.py",
             '    """Consum de massa de reacció, en tones per hora."""\n',
             '    """Consum de massa de reacció, en tones per hora.\n\n'
             '    0.8 és el factor de rendiment del motor Epstein de la Rocinante.\n'
             '    """\n')
    repo.commit("docs: explica el factor del motor Epstein", "naomi")

    modifica(repo, "rocinante/tripulacio.py", '''def alta(nom, rol):''', '''def capita():
    """Retorna el tripulant que té el rol de capità."""
    return next(t for t in TRIPULACIO if t["rol"] == "capità")


def alta(nom, rol):''')
    repo.commit("feat: afegeix la consulta del capità", "holden")

    repo.escriu(NAVEGACIO, navegacio_sense_rumb)
    repo.commit("refactor: neteja codi mort", "amos")

    registra_resposta("02", "autor_esborrat", "amos burton", "amos")
    registra_resposta("02", "hash_afegit", afegit[:7])
    copia(repo, "pas_02", "REPTE.md", "PISTES.md")
    repo.escriu("verifica.py", verifica("02"))
    repo.commit("feat: afegeix el repte i el verificador del pas 02", "naomi")
    repo.tag("pas-02", "Pas 02 - La caixa negra", "holden")

    repo.escriu(NAVEGACIO, navegacio_amb_rumb)
    repo.commit("fix: torna a afegir el rumb d'emergència", "alex")
