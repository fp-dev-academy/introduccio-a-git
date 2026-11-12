#!/usr/bin/env bash
# Pas 01 - missatge de commit sense format Conventional Commits.
# espera: Conventional Commits
set -euo pipefail
git switch --quiet -c treball/pas-01 pas-01
"$PYTHON" -m rocinante > /dev/null
perl -pi -e 's/^]$/    {"nom": "Camina Drummer", "rol": "cadet"},\n]/' rocinante/tripulacio.py
git add rocinante/tripulacio.py
git commit --quiet -m "he afegit la Camina"
printf '__pycache__/\n*.pyc\n.idea/\n' > .gitignore
git add .gitignore
git commit --quiet -m "chore: ignora els fitxers generats per Python i PyCharm"
