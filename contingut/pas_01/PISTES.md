# Pistes · Pas 01

Llegeix només la pista que necessitis.

## `git status` no mostra `__pycache__/`

Python només el crea quan executa el codi. Executa abans
`python -m rocinante tripulacio`. Si tampoc no surt `.idea/`, obre la carpeta
del projecte amb PyCharm.

## He fet commit de `__pycache__/` o de `.idea/`

Treu-los de l'índex sense esborrar-los del disc, i fes un commit nou:

```bash
git rm -r --cached rocinante/__pycache__ .idea
git commit -m "chore: deixa de versionar els fitxers generats"
```

Si ja tens el `.gitignore`, no tornaran a aparèixer.

## Vull tornar a començar el pas

```bash
git switch -C treball/pas-01 pas-01
```

La branca torna a l'estat inicial del pas. Els fitxers ignorats o sense
seguiment (`__pycache__/`, `.idea/`, `.gitignore`) es queden on són.

## `verifica.py` diu que `tripulacio.py` té un error de sintaxi

Cada element de la llista acaba amb una coma i va entre `{` i `}`:

```python
    {"nom": "Alex Kamal", "rol": "pilot"},
    {"nom": "El teu nom", "rol": "cadet"},
]
```

Comprova-ho executant `python -m rocinante tripulacio`.

## El missatge d'un commit no té el format correcte

Si és **l'últim** commit i encara no l'has pujat enlloc, en pots canviar el
missatge:

```bash
git commit --amend -m "feat: afegeix el teu nom a la tripulació"
```

Ho veuràs amb detall al pas 03.

## `git commit` ha obert el Bloc de notes

Has fet `git commit` sense `-m`. Escriu el missatge a la primera línia,
desa i tanca la finestra. Si la tanques sense escriure res, Git cancel·la el
commit.

## `verifica.py` diu que el directori de treball no està net

Tens canvis sense commit. `git status` et diu quins són: fes-ne commit o
descarta'ls amb `git restore <fitxer>`.
