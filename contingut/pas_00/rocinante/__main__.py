"""Línia d'ordres del diari de bord: python -m rocinante."""

import sys

from rocinante.combustible import calcula_consum
from rocinante.navegacio import temps_trajecte
from rocinante.tripulacio import TRIPULACIO

US = """Ús: python -m rocinante <ordre>

Ordres:
  tripulacio                            llista la tripulació
  consum MASSA_T ACCELERACIO_G          consum de massa de reacció
  trajecte DISTANCIA_KM VELOCITAT_KMS   temps de trajecte"""


def main(arguments):
    if not arguments:
        print("Diari de bord de la Rocinante.\n")
        print(US)
        return 0
    ordre, *valors = arguments
    try:
        if ordre == "tripulacio" and not valors:
            for tripulant in TRIPULACIO:
                print(f"{tripulant['nom']} ({tripulant['rol']})")
        elif ordre == "consum":
            massa_t, acceleracio_g = map(float, valors)
            print(f"Consum: {calcula_consum(massa_t, acceleracio_g):.2f} t/h")
        elif ordre == "trajecte":
            distancia_km, velocitat_kms = map(float, valors)
            print(f"Temps de trajecte: {temps_trajecte(distancia_km, velocitat_kms):.2f} h")
        else:
            print(US)
            return 2
    except ValueError:
        print(US)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
