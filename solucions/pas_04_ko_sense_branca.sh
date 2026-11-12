#!/usr/bin/env bash
# Pas 04 - fa el commit directament a treball/pas-04.
# espera: feature/rols
set -euo pipefail
git switch --quiet -c treball/pas-04 pas-04
cat >> rocinante/tripulacio.py <<'PY'


def per_rol(rol):
    """Retorna els tripulants que tenen el rol indicat."""
    return [tripulant for tripulant in TRIPULACIO if tripulant["rol"] == rol]
PY
git add rocinante/tripulacio.py
git commit --quiet -m "feat: llista la tripulació per rol"
