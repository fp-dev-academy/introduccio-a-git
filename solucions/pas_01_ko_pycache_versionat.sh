#!/usr/bin/env bash
# Pas 01 - fa `git add -A` abans de crear el .gitignore i versiona __pycache__.
# espera: cap fitxer de __pycache__/ ni .idea/
set -euo pipefail
git switch --quiet -c treball/pas-01 pas-01
"$PYTHON" -m rocinante > /dev/null
perl -pi -e 's/^]$/    {"nom": "Camina Drummer", "rol": "cadet"},\n]/' rocinante/tripulacio.py
git add -A
git commit --quiet -m "feat: afegeix Camina Drummer a la tripulació"
printf '__pycache__/\n*.pyc\n.idea/\n' > .gitignore
git add .gitignore
git commit --quiet -m "chore: ignora els fitxers generats per Python i PyCharm"
