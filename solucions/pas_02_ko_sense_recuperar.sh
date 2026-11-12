#!/usr/bin/env bash
# Pas 02 - respon les preguntes però no recupera la funció.
# espera: rumb_emergencia
set -euo pipefail
git switch --quiet -c treball/pas-02 pas-02
# Els dos commits que mencionen rumb_emergencia, del més antic al més nou.
AFEGIT=$(git log --reverse --format=%h -S rumb_emergencia -- rocinante/navegacio.py | sed -n 1p)
ESBORRAT=$(git log --format=%h -S rumb_emergencia -- rocinante/navegacio.py | sed -n 1p)
AUTOR=$(git log -1 --format=%an "$ESBORRAT")
mkdir -p respostes
printf "autor_esborrat=%s\nhash_afegit=%s\n" "$AUTOR" "$AFEGIT" > respostes/pas-02.txt
git add respostes/pas-02.txt
git commit --quiet -m "docs: respon les preguntes del pas 02"
