# Pistes · Pas 04

Llegeix només la pista que necessitis.

## No sé a quina branca soc

```bash
git branch            # l'asterisc marca la branca actual
git status            # la primera línia diu "On branch ..."
```

## He fet el commit a `treball/pas-04` en lloc de `feature/rols`

El més senzill és tornar a començar el pas:

```bash
git switch -C treball/pas-04 pas-04
git branch -D feature/rols      # si ja l'havies creada
```

## El merge no ha dit `Fast-forward`

Si ha obert el Bloc de notes o diu `Merge made by the 'ort' strategy`,
s'ha creat un commit de merge. Passa quan `treball/pas-04` té commits que
no són a `feature/rols`, o si has fet servir `--no-ff`. Torna a començar el
pas (vegeu la pista anterior) i fes tots els commits a `feature/rols`.

## `verifica.py` diu que `treball/pas-04` i `feature/rols` no apunten al mateix commit

Compara on és cada branca:

```bash
git log --oneline --graph --all -4
```

Si `feature/rols` va per davant, et falta el merge:

```bash
git switch treball/pas-04
git merge feature/rols
```

## `python -c ...` diu `No module named rocinante`

Executa l'ordre des de l'arrel del projecte (la carpeta on hi ha
`verifica.py`).
