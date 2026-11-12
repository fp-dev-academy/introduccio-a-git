#!/usr/bin/env bash
# Pas 00 - no ha configurat l'editor.
# espera: core.editor
set -euo pipefail
git remote set-url origin git@gitlab.com:alumne/git-rocinante.git
git remote add upstream git@gitlab.com:fp-dev-academy/git-rocinante.git
git config --global user.name "Camina Drummer"
git config --global user.email "camina.drummer@exemple.cat"
