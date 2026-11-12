#!/usr/bin/env bash
# Pas 01 - canvia el rol d'un tripulant en lloc d'afegir-s'hi.
# espera: TRIPULACIO
set -euo pipefail
git switch --quiet -c treball/pas-01 pas-01
"$PYTHON" -m rocinante > /dev/null
perl -pi -e 's/"rol": "pilot"/"rol": "pilot de combat"/' rocinante/tripulacio.py
git add rocinante/tripulacio.py
git commit --quiet -m "fix: corregeix el rol de l'Alex"
printf '__pycache__/\n*.pyc\n.idea/\n' > .gitignore
git add .gitignore
git commit --quiet -m "chore: ignora els fitxers generats per Python i PyCharm"
