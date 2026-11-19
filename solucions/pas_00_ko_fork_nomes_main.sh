#!/usr/bin/env bash
# Pas 00 - ha fet el fork amb «Copy the main branch only»: no té cap tag.
# espera: hi ha tots els tags del curs
set -euo pipefail
git tag --list | xargs git tag --delete > /dev/null
git remote set-url origin git@github.com:alumne/git-rocinante.git
git remote add upstream git@github.com:fp-dev-academy/git-rocinante.git
git config --global user.name "Camina Drummer"
git config --global user.email "camina.drummer@exemple.cat"
git config --global core.editor notepad
