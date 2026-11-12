#!/usr/bin/env bash
# Pas 02 - fa --amend sobre el commit del tag en lloc d'un commit nou.
# espera: parteix de pas-02
set -euo pipefail
git switch --quiet -c treball/pas-02 pas-02
AFEGIT=$(git log --reverse --format=%h -S rumb_emergencia -- rocinante/navegacio.py | sed -n 1p)
ESBORRAT=$(git log --format=%h -S rumb_emergencia -- rocinante/navegacio.py | sed -n 1p)
AUTOR=$(git log -1 --format=%an "$ESBORRAT")
git restore --source="$AFEGIT" rocinante/navegacio.py
git add rocinante/navegacio.py
git commit --quiet --amend --no-edit
mkdir -p respostes
printf "autor_esborrat=%s\nhash_afegit=%s\n" "$AUTOR" "$AFEGIT" > respostes/pas-02.txt
git add respostes/pas-02.txt
git commit --quiet -m "docs: respon les preguntes del pas 02"
