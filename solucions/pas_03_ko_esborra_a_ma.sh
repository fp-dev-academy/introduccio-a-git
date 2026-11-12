#!/usr/bin/env bash
# Pas 03 - treu el print a mà en lloc de fer revert.
# espera: revert
set -euo pipefail
git switch --quiet -c treball/pas-03 pas-03
AMOS=$(git log --format=%H -S "AMOS WAS HERE" -- rocinante/__main__.py | sed -n 1p)
git commit --quiet --amend -m "feat: ascendeix l'Amos a mecànic en cap"
perl -ni -e 'print unless /AMOS WAS HERE/' rocinante/__main__.py
git add rocinante/__main__.py
git commit --quiet -m "fix: treu el missatge de l'Amos"
