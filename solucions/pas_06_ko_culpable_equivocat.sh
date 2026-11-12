#!/usr/bin/env bash
# Pas 06 - respon amb l'últim commit dolent en lloc del primer.
# espera: culpable
set -euo pipefail
git switch --quiet -c treball/pas-06 pas-06
git bisect start pas-06 v1.0 > /dev/null
git bisect run "$PYTHON" tests/test_navegacio.py > /dev/null 2>&1
CULPABLE=$(git rev-parse --short=7 refs/bisect/bad)
git bisect reset > /dev/null 2>&1
mkdir -p respostes
printf "culpable=%s\n" "$CULPABLE" > respostes/pas-06.txt
git revert --no-edit "$CULPABLE" > /dev/null
git add respostes/pas-06.txt
git commit --quiet -m "docs: respon la pregunta del pas 06"
git rev-parse --short=7 pas-06~1 | sed 's/^/culpable=/' > respostes/pas-06.txt
git add respostes/pas-06.txt
git commit --quiet -m "docs: corregeix la resposta del pas 06"
