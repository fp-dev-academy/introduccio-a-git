#!/usr/bin/env bash
# Pas 03 - corregeix el missatge, però sense format Conventional Commits.
# espera: Conventional Commits
set -euo pipefail
git switch --quiet -c treball/pas-03 pas-03
AMOS=$(git log --format=%H -S "AMOS WAS HERE" -- rocinante/__main__.py | sed -n 1p)
git commit --quiet --amend -m "arreglat"
git revert --no-edit "$AMOS" > /dev/null
