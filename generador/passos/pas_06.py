"""Pas 06 - Algú ha trencat la navegació.

Després de v1.0, 16 commits lineals de farciment. El 9è (de Naomi) canvia
`/ 3600` per `/ 360` a temps_trajecte(). Cap commit posterior no toca
navegacio.py, i tests/test_navegacio.py no canvia en tot el rang. Després
del tag, Alex fa el revert del culpable a main (ESPECIFICACIO.md, 3).
"""

from git_utils import Repo
from passos import copia, modifica, registra_resposta, verifica

MAIN = "rocinante/__main__.py"
TRIPULACIO = "rocinante/tripulacio.py"
COMBUSTIBLE = "rocinante/combustible.py"
NAVEGACIO = "rocinante/navegacio.py"
TEST_TRIPULACIO = "tests/test_tripulacio.py"
TEST_COMBUSTIBLE = "tests/test_combustible.py"

# Cada commit: (tripulant, missatge, [(fitxer, fragment, substitució), ...]).
# El 9è és el culpable. Els canvis a navegacio.py només van abans del 9è.
FARCIMENT = [
    ("alex", "feat: afegeix la velocitat de la llum", [
        (NAVEGACIO, '"""Càlculs de navegació."""\n',
         '"""Càlculs de navegació."""\n\nVELOCITAT_LLUM_KMS = 299_792.458\n'),
    ]),
    ("holden", "feat: comprova si algú és a bord", [
        (TRIPULACIO, "def capita():\n",
         'def es_a_bord(nom):\n    """Diu si hi ha algú amb aquest nom a la tripulació."""\n'
         "    return nom in noms()\n\n\ndef capita():\n"),
    ]),
    ("naomi", "docs: aclareix les unitats del consum en repòs", [
        (COMBUSTIBLE,
         '    """Consum de massa de reacció amb els motors al ralentí, en tones per hora."""\n',
         '    """Consum de massa de reacció amb els motors al ralentí.\n\n'
         "    La massa és en tones i el resultat, en tones per hora.\n    \"\"\"\n"),
    ]),
    ("amos", "feat: mostra quants tripulants hi ha", [
        (MAIN, "                print(f\"{tripulant['nom']} ({tripulant['rol']})\")\n",
         "                print(f\"{tripulant['nom']} ({tripulant['rol']})\")\n"
         '            print(f"Total: {len(TRIPULACIO)} tripulants")\n'),
    ]),
    ("alex", "feat: calcula la distància recorreguda", [
        (NAVEGACIO, "    return (rumb_perill + 180) % 360\n",
         "    return (rumb_perill + 180) % 360\n\n\n"
         "def distancia_recorreguda(velocitat_kms, segons):\n"
         '    """Distància recorreguda, en km."""\n'
         "    return velocitat_kms * segons\n"),
    ]),
    ("holden", "test: comprova qui és a bord", [
        (TEST_TRIPULACIO, "from rocinante.tripulacio import capita, noms  # noqa: E402\n",
         "from rocinante.tripulacio import capita, es_a_bord, noms  # noqa: E402\n"),
        (TEST_TRIPULACIO, "            self.assertIn(nom, noms())\n",
         "            self.assertIn(nom, noms())\n\n"
         "    def test_es_a_bord(self):\n"
         '        self.assertTrue(es_a_bord("Amos Burton"))\n'
         '        self.assertFalse(es_a_bord("Joe Miller"))\n'),
    ]),
    ("naomi", "feat: calcula l'autonomia", [
        (COMBUSTIBLE, "    return massa_t * 0.01\n",
         "    return massa_t * 0.01\n\n\n"
         "def autonomia(massa_reaccio_t, consum_t_h):\n"
         '    """Hores que es pot mantenir un consum amb la massa de reacció disponible."""\n'
         "    return massa_reaccio_t / consum_t_h\n"),
    ]),
    ("amos", "fix: treu els espais dels noms nous", [
        (TRIPULACIO, '    tripulant = {"nom": nom, "rol": rol}\n',
         '    tripulant = {"nom": nom.strip(), "rol": rol.strip()}\n'),
    ]),
    ("naomi", "refactor: unifica conversions d'unitats", [
        (NAVEGACIO, "    return distancia_km / velocitat_kms / 3600\n",
         "    return distancia_km / velocitat_kms / 360\n"),
    ]),
    ("alex", "test: comprova l'autonomia", [
        (TEST_COMBUSTIBLE, "from rocinante.combustible import calcula_consum  # noqa: E402\n",
         "from rocinante.combustible import autonomia, calcula_consum  # noqa: E402\n"),
        (TEST_COMBUSTIBLE,
         "            calcula_consum(100, 1, eficiencia=2.0, mode_combat=True), 60.0)\n",
         "            calcula_consum(100, 1, eficiencia=2.0, mode_combat=True), 60.0)\n\n"
         "    def test_autonomia(self):\n"
         "        self.assertAlmostEqual(autonomia(100, 20), 5.0)\n"),
    ]),
    ("holden", "feat: afegeix l'ordre autonomia", [
        (MAIN, "from rocinante.combustible import calcula_consum\n",
         "from rocinante.combustible import autonomia, calcula_consum\n"),
        (MAIN, "  rumb GRAUS_PERILL                     rumb d'emergència\"\"\"",
         "  rumb GRAUS_PERILL                     rumb d'emergència\n"
         "  autonomia MASSA_T CONSUM_T_H          hores d'autonomia\"\"\""),
        (MAIN, "        else:\n            print(US)\n            return 2\n",
         '        elif ordre == "autonomia":\n'
         "            massa_t, consum_t_h = map(float, valors)\n"
         '            print(f"Autonomia: {autonomia(massa_t, consum_t_h):.1f} h")\n'
         "        else:\n            print(US)\n            return 2\n"),
    ]),
    ("amos", "fix: ajusta el consum en repòs", [
        (COMBUSTIBLE, "    return massa_t * 0.01\n", "    return massa_t * 0.012\n"),
    ]),
    ("naomi", "docs: documenta el format de TRIPULACIO", [
        (TRIPULACIO, '"""Tripulació de la Rocinante."""\n',
         '"""Tripulació de la Rocinante.\n\n'
         'Cada tripulant és un diccionari amb les claus "nom" i "rol".\n"""\n'),
    ]),
    ("alex", "docs: millora l'ajuda de la línia d'ordres", [
        (MAIN, 'US = """Ús: python -m rocinante <ordre>\n',
         'US = """Ús: python -m rocinante <ordre> [valors...]\n'),
    ]),
    ("holden", "test: comprova l'alta de tripulants", [
        (TEST_TRIPULACIO, "from rocinante.tripulacio import capita, es_a_bord, noms  # noqa: E402\n",
         "from rocinante.tripulacio import alta, capita, es_a_bord, noms  # noqa: E402\n"),
        (TEST_TRIPULACIO, '        self.assertFalse(es_a_bord("Joe Miller"))\n',
         '        self.assertFalse(es_a_bord("Joe Miller"))\n\n'
         "    def test_alta_treu_els_espais(self):\n"
         '        tripulant = alta("  Bobbie Draper ", "marine")\n'
         '        self.assertEqual(tripulant["nom"], "Bobbie Draper")\n'),
    ]),
    ("amos", "fix: avisa si el consum no és positiu", [
        (COMBUSTIBLE, "    return massa_reaccio_t / consum_t_h\n",
         "    if consum_t_h <= 0:\n"
         '        raise ValueError("el consum ha de ser positiu")\n'
         "    return massa_reaccio_t / consum_t_h\n"),
    ]),
]

assert len(FARCIMENT) == 16
assert FARCIMENT[8][1] == "refactor: unifica conversions d'unitats"


def build(repo: Repo) -> None:
    hashos = []
    for tripulant, missatge, canvis in FARCIMENT:
        for fitxer, vell, nou in canvis:
            modifica(repo, fitxer, vell, nou)
        hashos.append(repo.commit(missatge, tripulant))
    culpable = hashos[8]

    registra_resposta("06", "culpable", culpable[:7])
    copia(repo, "pas_06", "REPTE.md", "PISTES.md")
    repo.escriu("verifica.py", verifica("06"))
    repo.commit("feat: afegeix el repte i el verificador del pas 06", "naomi")
    repo.tag("pas-06", "Pas 06 - Algú ha trencat la navegació", "holden")

    repo.revert(culpable, "alex")
