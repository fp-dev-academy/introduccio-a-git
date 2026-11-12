"""Pas 04 - Nova secció de tripulació.

L'alumne crea la branca feature/rols i hi afegeix per_rol(). Abans del tag,
Alex afegeix l'ordre `rumb` a la línia d'ordres (commit de farciment).
"""

from git_utils import Repo
from passos import copia, modifica, verifica


def build(repo: Repo) -> None:
    main = "rocinante/__main__.py"
    modifica(repo, main,
             "from rocinante.navegacio import temps_trajecte\n",
             "from rocinante.navegacio import rumb_emergencia, temps_trajecte\n")
    modifica(repo, main,
             "  trajecte DISTANCIA_KM VELOCITAT_KMS   temps de trajecte\"\"\"",
             "  trajecte DISTANCIA_KM VELOCITAT_KMS   temps de trajecte\n"
             "  rumb GRAUS_PERILL                     rumb d'emergència\"\"\"")
    modifica(repo, main,
             "        else:\n            print(US)\n            return 2\n",
             "        elif ordre == \"rumb\":\n"
             "            (rumb_perill,) = map(float, valors)\n"
             "            print(f\"Rumb d'emergència: {rumb_emergencia(rumb_perill):.0f} graus\")\n"
             "        else:\n            print(US)\n            return 2\n")
    repo.commit("feat: afegeix l'ordre rumb a la línia d'ordres", "alex")

    copia(repo, "pas_04", "REPTE.md", "PISTES.md")
    repo.escriu("verifica.py", verifica("04"))
    repo.commit("feat: afegeix el repte i el verificador del pas 04", "naomi")
    repo.tag("pas-04", "Pas 04 - Nova secció de tripulació", "holden")
