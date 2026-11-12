#!/usr/bin/env bash
# Pas 07 - resolució correcta: puja totes les branques amb seguiment.
set -euo pipefail
# Simula el fork de GitLab amb un repositori bare local, que fa d'origin.
FORK="$(pwd)/../fork.git"
git clone --quiet --bare "$(git remote get-url origin)" "$FORK"
git remote set-url origin "$FORK"
# Branques de treball de passos anteriors (amb algun commit propi).
git switch --quiet -c treball/pas-01 pas-01
git switch --quiet -c treball/pas-05 pas-05
git commit --quiet --allow-empty -m "chore: resol el conflicte de la sala de màquines"
git switch --quiet -c treball/pas-07 pas-07
git push --quiet -u origin treball/pas-05
git push --quiet -u origin --all
