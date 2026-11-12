#!/usr/bin/env bash
# Pas 00 - ha clonat el fork per HTTPS en lloc d'SSH.
# espera: origin fa servir SSH
set -euo pipefail
git remote set-url origin https://gitlab.com/alumne/git-rocinante.git
git remote add upstream git@gitlab.com:fp-dev-academy/git-rocinante.git
git config --global user.name "Camina Drummer"
git config --global user.email "camina.drummer@exemple.cat"
git config --global core.editor notepad
