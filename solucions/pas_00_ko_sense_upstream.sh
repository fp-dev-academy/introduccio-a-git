#!/usr/bin/env bash
# Pas 00 - no ha afegit el remot upstream.
# espera: upstream apunta al repositori guia
set -euo pipefail
git remote set-url origin git@github.com:alumne/git-rocinante.git
git config --global user.name "Camina Drummer"
git config --global user.email "camina.drummer@exemple.cat"
git config --global core.editor notepad
