#!/usr/bin/env bash
# Pas 04 - fa la feina a feature/rols però no la integra a treball/pas-04.
# espera: git merge feature/rols
set -euo pipefail
git switch --quiet -c treball/pas-04 pas-04
git switch --quiet -c feature/rols
cat >> rocinante/tripulacio.py <<'PY'


def per_rol(rol):
    """Retorna els tripulants que tenen el rol indicat."""
    return [tripulant for tripulant in TRIPULACIO if tripulant["rol"] == rol]
PY
git add rocinante/tripulacio.py
git commit --quiet -m "feat: llista la tripulació per rol"
git switch --quiet treball/pas-04
