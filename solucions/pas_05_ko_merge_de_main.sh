#!/usr/bin/env bash
# Pas 05 - copia la resolució de la tripulació fent merge de main.
# espera: v1.0
set -euo pipefail
git switch --quiet -c treball/pas-05 pas-05
NAOMI=origin/tripulacio/naomi-eficiencia
AMOS=origin/tripulacio/amos-potencia
git merge --quiet --no-edit origin/main
