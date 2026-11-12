#!/usr/bin/env bash
# Pas 01 - ho fa tot en un sol commit.
# espera: almenys 2 commits nous
set -euo pipefail
git switch --quiet -c treball/pas-01 pas-01
"$PYTHON" -m rocinante > /dev/null
perl -pi -e 's/^]$/    {"nom": "Camina Drummer", "rol": "cadet"},\n]/' rocinante/tripulacio.py
printf '__pycache__/\n*.pyc\n.idea/\n' > .gitignore
git add rocinante/tripulacio.py .gitignore
git commit --quiet -m "feat: afegeix Camina Drummer i el .gitignore"
