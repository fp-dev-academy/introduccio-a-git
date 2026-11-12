#!/usr/bin/env bash
# Pas 03 - resolució correcta.
set -euo pipefail
git switch --quiet -c treball/pas-03 pas-03
AMOS=$(git log --format=%H -S "AMOS WAS HERE" -- rocinante/__main__.py | sed -n 1p)
# Pràctica sense verificació: staging i descartar canvis.
echo "nota de prova" >> README.md
git add README.md
git restore --staged README.md
git restore README.md
git commit --quiet --amend -m "feat: ascendeix l'Amos a mecànic en cap"
git revert --no-edit "$AMOS" > /dev/null
