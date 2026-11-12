# Pistes · Pas 03

Llegeix només la pista que necessitis.

## He fet el revert abans de l'`--amend`

L'`--amend` ha modificat el commit del revert, no el d'`asdf`. Torna a
començar el pas des de zero i fes-ho en ordre: primer l'`--amend` i
després el revert.

```bash
git switch -C treball/pas-03 pas-03
```

## No sé quin commit va introduir l'"AMOS WAS HERE"

```bash
git log --oneline -S "AMOS WAS HERE" -- rocinante/__main__.py
```

## El revert ha obert el Bloc de notes i no sé què fer

El missatge ja està escrit. Desa (Ctrl+S) i tanca la finestra. Fins que no
la tanquis, el terminal es queda esperant.

## He fet l'`--amend` sense `-m` i s'ha obert el Bloc de notes

Hi veuràs el missatge actual (`asdf`). Substitueix-lo pel nou, desa i tanca.

## `verifica.py` diu que HEAD~1 no té el mateix contingut que `asdf`

Abans de l'`--amend` tenies algun canvi al staging, i l'`--amend` l'ha
afegit al commit. Torna a començar el pas i, abans de l'`--amend`,
comprova amb `git status` que no hi ha res al staging.

## He esborrat la línia de l'"AMOS WAS HERE" a mà

Funciona, però el repte és fer-ho amb `git revert`: queda constància de
quin commit es desfà. Torna a començar el pas.

## `verifica.py` diu que la branca no parteix de `pas-03~1`

Has eliminat commits de la història (per exemple, amb `git reset` o
`git rebase`). Torna a començar el pas.

## `git revert` diu que hi ha un conflicte

No n'hi hauria d'haver cap, si no has tocat `rocinante/__main__.py`.
Cancel·la el revert i torna a començar el pas:

```bash
git revert --abort
git switch -C treball/pas-03 pas-03
```
