#!/usr/bin/env bash
# Pas 03 - fa el revert abans de l'--amend, i l'--amend modifica el revert.
# espera: revert abans
set -euo pipefail
git switch --quiet -c treball/pas-03 pas-03
AMOS=$(git log --format=%H -S "AMOS WAS HERE" -- rocinante/__main__.py | sed -n 1p)
git revert --no-edit "$AMOS" > /dev/null
git commit --quiet --amend -m "feat: ascendeix l'Amos a mecànic en cap"
