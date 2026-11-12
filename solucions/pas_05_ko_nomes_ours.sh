#!/usr/bin/env bash
# Pas 05 - resol el conflicte quedant-se només la versió de la Naomi.
# espera: test_combustible
set -euo pipefail
git switch --quiet -c treball/pas-05 pas-05
NAOMI=origin/tripulacio/naomi-eficiencia
AMOS=origin/tripulacio/amos-potencia
git merge --quiet "$NAOMI"                  # fast-forward
git merge "$AMOS" > /dev/null || true         # conflicte esperat
git checkout --ours rocinante/combustible.py
git add rocinante/combustible.py
git commit --quiet --no-edit
