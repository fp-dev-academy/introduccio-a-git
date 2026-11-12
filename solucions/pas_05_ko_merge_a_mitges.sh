#!/usr/bin/env bash
# Pas 05 - resol el conflicte però no acaba el merge amb un commit.
# espera: amos-potencia
set -euo pipefail
git switch --quiet -c treball/pas-05 pas-05
NAOMI=origin/tripulacio/naomi-eficiencia
AMOS=origin/tripulacio/amos-potencia
git merge --quiet "$NAOMI"                  # fast-forward
git merge "$AMOS" > /dev/null || true         # conflicte esperat
# Resol els dos blocs en conflicte amb la solució de referència.
"$PYTHON" - <<'PY'
import re
from pathlib import Path
fitxer = Path("rocinante/combustible.py")
text = fitxer.read_text(encoding="utf-8")
blocs = iter([
    "def calcula_consum(massa_t, acceleracio_g, eficiencia=1.0, mode_combat=False):\n",
    "    factor = 1.5 if mode_combat else 1.0\n"
    "    return massa_t * acceleracio_g * 0.8 * factor / eficiencia\n",
])
text = re.sub(r"<<<<<<< .*?\n.*?=======\n.*?>>>>>>> .*?\n", lambda m: next(blocs), text, flags=re.S)
fitxer.write_text(text, encoding="utf-8", newline="\n")
PY
git add rocinante/combustible.py
