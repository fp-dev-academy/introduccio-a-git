#!/usr/bin/env bash
# Pas 03 - aprofita l'--amend per afegir-hi un canvi.
# espera: mateix contingut
set -euo pipefail
git switch --quiet -c treball/pas-03 pas-03
AMOS=$(git log --format=%H -S "AMOS WAS HERE" -- rocinante/__main__.py | sed -n 1p)
echo '# Revisat per Naomi' >> rocinante/tripulacio.py
git add rocinante/tripulacio.py
git commit --quiet --amend -m "feat: ascendeix l'Amos a mecànic en cap"
git revert --no-edit "$AMOS" > /dev/null
