#!/usr/bin/env bash
# Pas 05 - només integra la branca de la Naomi.
# espera: amos-potencia
set -euo pipefail
git switch --quiet -c treball/pas-05 pas-05
NAOMI=origin/tripulacio/naomi-eficiencia
AMOS=origin/tripulacio/amos-potencia
git merge --quiet "$NAOMI"
