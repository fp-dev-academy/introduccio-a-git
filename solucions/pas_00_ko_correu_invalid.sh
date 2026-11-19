#!/usr/bin/env bash
# Pas 00 - ha posat el nom d'usuari com a correu.
# espera: user.email
set -euo pipefail
git remote set-url origin git@github.com:alumne/git-rocinante.git
git remote add upstream git@github.com:fp-dev-academy/git-rocinante.git
git config --global user.name "Camina Drummer"
git config --global user.email "cdrummer"
git config --global core.editor notepad
