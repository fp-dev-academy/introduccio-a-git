"""Pas 03 - Esborrar les proves.

Amos fa que la CLI imprimeixi "AMOS WAS HERE" i, uns quants commits després,
fa un commit amb el missatge "asdf", que és el que apunta el tag. Entremig,
cap commit no toca __main__.py, perquè el revert no tingui conflictes.
Després del tag, Naomi fa el revert a main (ESPECIFICACIO.md, 3).
"""

from git_utils import Repo
from passos import copia, modifica, verifica

CONSUM_EN_REPOS = '''

def consum_en_repos(massa_t):
    """Consum de massa de reacció amb els motors al ralentí, en tones per hora."""
    return massa_t * 0.01
'''

TEST_TRIPULACIO = '''\
"""Tests de rocinante/tripulacio.py. Ús: python tests/test_tripulacio.py"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rocinante.tripulacio import capita, noms  # noqa: E402


class TestTripulacio(unittest.TestCase):
    def test_el_capita_es_holden(self):
        self.assertEqual(capita()["nom"], "James Holden")

    def test_la_tripulacio_original_hi_es(self):
        for nom in ("James Holden", "Naomi Nagata", "Amos Burton", "Alex Kamal"):
            self.assertIn(nom, noms())


if __name__ == "__main__":
    unittest.main()
'''


def build(repo: Repo) -> None:
    modifica(repo, "rocinante/__main__.py",
             "def main(arguments):\n",
             'def main(arguments):\n    print("AMOS WAS HERE")\n')
    amos = repo.commit("feat: millora la sortida de la CLI", "amos")

    text = (repo.directori / "rocinante/combustible.py").read_text(encoding="utf-8")
    repo.escriu("rocinante/combustible.py", text + CONSUM_EN_REPOS)
    repo.commit("feat: calcula el consum en repòs", "naomi")

    repo.escriu("tests/test_tripulacio.py", TEST_TRIPULACIO)
    repo.commit("test: comprova la consulta del capità", "holden")

    copia(repo, "pas_03", "REPTE.md", "PISTES.md")
    repo.escriu("verifica.py", verifica("03"))
    repo.commit("feat: afegeix el repte i el verificador del pas 03", "naomi")

    modifica(repo, "rocinante/tripulacio.py",
             '{"nom": "Amos Burton", "rol": "mecànic"}',
             '{"nom": "Amos Burton", "rol": "mecànic en cap"}')
    repo.commit("asdf", "amos")
    repo.tag("pas-03", "Pas 03 - Esborrar les proves", "holden")

    repo.revert(amos, "naomi")
