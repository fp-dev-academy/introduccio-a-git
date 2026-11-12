"""Pas 05 - Conflicte a la sala de màquines.

Holden escriu els tests que tothom ha acordat (eficiència, mode de combat i
la combinació): a pas-05 fallen a propòsit. Des de pas-05 surten dues
branques, d'un commit cadascuna, que modifiquen la signatura i el return de
calcula_consum(). Després del tag, Naomi les integra a main i resol el
conflicte: aquest merge és v1.0 (ESPECIFICACIO.md, 3).
"""

from git_utils import Repo
from passos import copia, modifica, verifica

COMBUSTIBLE = "rocinante/combustible.py"
SIGNATURA = "def calcula_consum(massa_t, acceleracio_g):\n"
RETURN = "    return massa_t * acceleracio_g * 0.8\n"

TESTS_NOUS = '''
    def test_eficiencia(self):
        self.assertAlmostEqual(calcula_consum(100, 1, eficiencia=2.0), 40.0)

    def test_mode_combat(self):
        self.assertAlmostEqual(calcula_consum(100, 1, mode_combat=True), 120.0)

    def test_eficiencia_i_mode_combat(self):
        self.assertAlmostEqual(
            calcula_consum(100, 1, eficiencia=2.0, mode_combat=True), 60.0)
'''


def build(repo: Repo) -> None:
    modifica(repo, "tests/test_combustible.py",
             "        self.assertAlmostEqual(calcula_consum(100, 3), 3 * calcula_consum(100, 1))\n",
             "        self.assertAlmostEqual(calcula_consum(100, 3), 3 * calcula_consum(100, 1))\n"
             + TESTS_NOUS)
    repo.commit("test: comprova l'eficiència i el mode de combat", "holden")

    copia(repo, "pas_05", "REPTE.md", "PISTES.md")
    repo.escriu("verifica.py", verifica("05"))
    repo.commit("feat: afegeix el repte i el verificador del pas 05", "naomi")
    repo.tag("pas-05", "Pas 05 - Conflicte a la sala de màquines", "holden")
    base = (repo.directori / COMBUSTIBLE).read_text(encoding="utf-8")

    repo.git("switch", "--quiet", "-c", "tripulacio/naomi-eficiencia", "pas-05")
    repo.escriu(COMBUSTIBLE, base
                .replace(SIGNATURA, "def calcula_consum(massa_t, acceleracio_g, eficiencia=1.0):\n")
                .replace(RETURN, "    return massa_t * acceleracio_g * 0.8 / eficiencia\n"))
    repo.commit("feat: té en compte l'eficiència del motor", "naomi")

    repo.git("switch", "--quiet", "-c", "tripulacio/amos-potencia", "pas-05")
    repo.escriu(COMBUSTIBLE, base
                .replace(SIGNATURA, "def calcula_consum(massa_t, acceleracio_g, mode_combat=False):\n")
                .replace(RETURN, "    factor = 1.5 if mode_combat else 1.0\n"
                                 "    return massa_t * acceleracio_g * 0.8 * factor\n"))
    repo.commit("feat: mode de combat", "amos")

    repo.git("switch", "--quiet", "main")
    repo.git("merge", "--quiet", "--ff-only", "tripulacio/naomi-eficiencia")
    resolt = (base
              .replace(SIGNATURA, "def calcula_consum(massa_t, acceleracio_g, eficiencia=1.0,\n"
                                  "                   mode_combat=False):\n")
              .replace(RETURN, "    factor = 1.5 if mode_combat else 1.0\n"
                               "    return massa_t * acceleracio_g * 0.8 * factor / eficiencia\n"))
    repo.merge("tripulacio/amos-potencia", "naomi", resolucio={COMBUSTIBLE: resolt})
    repo.tag("v1.0", "Versió 1.0 - Eficiència i mode de combat", "holden")
