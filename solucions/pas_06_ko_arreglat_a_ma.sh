#!/usr/bin/env bash
# Pas 06 - troba el culpable, però corregeix la línia a mà en lloc de fer revert.
# espera: revert
set -euo pipefail
git switch --quiet -c treball/pas-06 pas-06
git bisect start pas-06 v1.0 > /dev/null
git bisect run "$PYTHON" tests/test_navegacio.py > /dev/null 2>&1
CULPABLE=$(git rev-parse --short=7 refs/bisect/bad)
git bisect reset > /dev/null 2>&1
mkdir -p respostes
printf "culpable=%s\n" "$CULPABLE" > respostes/pas-06.txt
perl -pi -e 's|/ 360$|/ 3600|' rocinante/navegacio.py
git add rocinante/navegacio.py respostes/pas-06.txt
git commit --quiet -m "fix: corregeix la conversió a hores"
