#!/usr/bin/env bash
# Pas 06 - correcta, amb bisect manual (good/bad a cada pas).
set -euo pipefail
git switch --quiet -c treball/pas-06 pas-06
git bisect start pas-06 v1.0 > /dev/null
while true; do
    if "$PYTHON" tests/test_navegacio.py > /dev/null 2>&1; then veredicte=good; else veredicte=bad; fi
    resultat=$(git bisect "$veredicte")
    case "$resultat" in *"is the first bad commit"*) break ;; esac
done
CULPABLE=$(git rev-parse --short=7 refs/bisect/bad)
git bisect reset > /dev/null 2>&1
mkdir -p respostes
printf "culpable=%s\n" "$CULPABLE" > respostes/pas-06.txt
git revert --no-edit "$CULPABLE" > /dev/null
git add respostes/pas-06.txt
git commit --quiet -m "docs: respon la pregunta del pas 06"
