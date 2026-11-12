#!/usr/bin/env bash
# Pas 03 - fa el revert però no corregeix el missatge asdf.
# espera: --amend
set -euo pipefail
git switch --quiet -c treball/pas-03 pas-03
AMOS=$(git log --format=%H -S "AMOS WAS HERE" -- rocinante/__main__.py | sed -n 1p)
git revert --no-edit "$AMOS" > /dev/null
