#!/usr/bin/env bash
# Pas 00 - ha clonat el repositori guia en lloc del seu fork.
# espera: origin apunta al teu fork
set -euo pipefail
git remote set-url origin git@github.com:fp-dev-academy/git-rocinante.git
git remote add upstream git@github.com:fp-dev-academy/git-rocinante.git
git config --global user.name "Camina Drummer"
git config --global user.email "camina.drummer@exemple.cat"
git config --global core.editor notepad
