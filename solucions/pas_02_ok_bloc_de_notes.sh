#!/usr/bin/env bash
# Pas 02 - correcta, amb respostes escrites al Bloc de notes: BOM, CRLF, espais, nom de pila i hash llarg en majúscules.
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
HASH_LLARG=$(git rev-parse --short=8 "$AFEGIT" | tr a-f A-F)
printf '\xef\xbb\xbf# Respostes del pas 02\r\n\r\n  autor_esborrat = amos \r\nhash_afegit= %s\r\n' "$HASH_LLARG" > respostes/pas-02.txt
git add respostes/pas-02.txt
git commit --quiet -m "docs: respon les preguntes del pas 02"
