#!/usr/bin/env bash
# Pas 01 - resolució correcta.
set -euo pipefail
git switch --quiet -c treball/pas-01 pas-01
"$PYTHON" -m rocinante > /dev/null           # crea __pycache__/
mkdir -p .idea && echo "<project/>" > .idea/workspace.xml   # com PyCharm
perl -pi -e 's/^]$/    {"nom": "Camina Drummer", "rol": "cadet"},\n]/' rocinante/tripulacio.py
git add rocinante/tripulacio.py
git commit --quiet -m "feat: afegeix Camina Drummer a la tripulació"
printf '__pycache__/\n*.pyc\n.idea/\n' > .gitignore
git add .gitignore
git commit --quiet -m "chore: ignora els fitxers generats per Python i PyCharm"
