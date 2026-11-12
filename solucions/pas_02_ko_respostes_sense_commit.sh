#!/usr/bin/env bash
# Pas 02 - escriu les respostes però no en fa commit.
# espera: respostes/pas-02.txt versionat
set -euo pipefail
git switch --quiet -c treball/pas-02 pas-02
# Els dos commits que mencionen rumb_emergencia, del més antic al més nou.
AFEGIT=$(git log --reverse --format=%h -S rumb_emergencia -- rocinante/navegacio.py | sed -n 1p)
ESBORRAT=$(git log --format=%h -S rumb_emergencia -- rocinante/navegacio.py | sed -n 1p)
AUTOR=$(git log -1 --format=%an "$ESBORRAT")
git switch --quiet --detach "$AFEGIT"
grep -q "def rumb_emergencia" rocinante/navegacio.py
git switch --quiet -
git restore --source="$AFEGIT" rocinante/navegacio.py
git add rocinante/navegacio.py
git commit --quiet -m "fix: recupera el rumb d'emergència"
mkdir -p respostes
printf "autor_esborrat=%s\nhash_afegit=%s\n" "$AUTOR" "$AFEGIT" > respostes/pas-02.txt
