#!/usr/bin/env bash
# Pas 05 - fa commit amb els marcadors de conflicte.
# espera: <<<<<<<
set -euo pipefail
git switch --quiet -c treball/pas-05 pas-05
NAOMI=origin/tripulacio/naomi-eficiencia
AMOS=origin/tripulacio/amos-potencia
git merge --quiet "$NAOMI"                  # fast-forward
git merge "$AMOS" > /dev/null || true         # conflicte esperat
git add rocinante/combustible.py
git commit --quiet --no-edit
