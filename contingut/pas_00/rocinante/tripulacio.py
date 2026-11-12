"""Tripulació de la Rocinante."""

TRIPULACIO = [
    {"nom": "James Holden", "rol": "capità"},
    {"nom": "Naomi Nagata", "rol": "enginyera"},
    {"nom": "Amos Burton", "rol": "mecànic"},
    {"nom": "Alex Kamal", "rol": "pilot"},
]


def noms():
    """Retorna els noms de tota la tripulació."""
    return [tripulant["nom"] for tripulant in TRIPULACIO]


def alta(nom, rol):
    """Dona d'alta un tripulant nou (només durant l'execució)."""
    tripulant = {"nom": nom, "rol": rol}
    TRIPULACIO.append(tripulant)
    return tripulant
