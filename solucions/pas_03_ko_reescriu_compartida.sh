#!/usr/bin/env bash
# Pas 03 - elimina el commit de l'Amos de la història amb rebase.
# espera: parteix de pas-03~1
set -euo pipefail
git switch --quiet -c treball/pas-03 pas-03
AMOS=$(git log --format=%H -S "AMOS WAS HERE" -- rocinante/__main__.py | sed -n 1p)
git rebase --quiet --onto "$AMOS~1" "$AMOS"
