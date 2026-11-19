#!/usr/bin/env bash
# Pas 00 - resolució correcta.
# El test ja ha fet el clon; aquí se simula que era el fork de l'alumne.
set -euo pipefail
git remote set-url origin git@github.com:alumne/git-rocinante.git
git remote add upstream git@github.com:fp-dev-academy/git-rocinante.git
git config --global user.name "Camina Drummer"
git config --global user.email "camina.drummer@exemple.cat"
git config --global core.editor notepad
