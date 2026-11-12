# Pas 01 · Primera entrada al diari

Ja ets a bord, però el diari encara no ho sap: el teu nom no surt a la llista
de la tripulació. I, de passada, l'Amos s'ha queixat que el diari s'omple de
brossa cada vegada que algú obre l'ordinador de bord.

## Què aprendràs

- Les **tres zones** de Git: directori de treball, *staging* (índex) i
  repositori.
- `git status`, `git diff`, `git add` i `git commit`.
- Escriure **missatges de commit** amb el format Conventional Commits.
- Fer que Git **ignori** fitxers amb `.gitignore`.

## Les tres zones

```
directori de treball  --git add-->  staging  --git commit-->  repositori
  (els teus fitxers)                (el que                   (la història)
                                     anirà al commit)
```

`git status` et diu, en tot moment, què hi ha a cada zona. Executa'l sovint.

## El repte

Comença des de la teva branca de treball:

```bash
git switch -c treball/pas-01 pas-01
```

### 1. Genera brossa

Executa l'aplicació i assegura't que tens el projecte obert a PyCharm:

```bash
python -m rocinante tripulacio
git status
```

Fixa't en les línies `Untracked files`: hi ha `rocinante/__pycache__/`
(fitxers que crea Python en executar el codi) i `.idea/` (la configuració de
PyCharm). No formen part del diari i **no s'han de versionar mai**.

> Si PyCharm et pregunta si vols afegir fitxers a Git, respon que **no**.

### 2. Afegeix-te a la tripulació

Obre `rocinante/tripulacio.py` i afegeix una línia a la llista `TRIPULACIO`,
just abans del `]` final, amb el teu nom:

```python
    {"nom": "El teu nom", "rol": "cadet"},
```

Mira què ha canviat i què hi ha a cada zona:

```bash
git status
git diff
```

Passa el canvi al *staging*, torna a mirar l'estat i fes el commit:

```bash
git add rocinante/tripulacio.py
git status
git commit -m "feat: afegeix el teu nom a la tripulació"
```

> Fes `git add` **del fitxer concret**. Un `git add .` ara afegiria també
> `__pycache__/` i `.idea/` al commit.

### 3. Ignora la brossa

Crea el fitxer `.gitignore` a l'arrel del projecte (amb PyCharm o des del
terminal) amb aquest contingut:

```
__pycache__/
*.pyc
.idea/
```

Des de Git Bash, ho pots fer amb:

```bash
printf '__pycache__/\n*.pyc\n.idea/\n' > .gitignore
```

Torna a mirar l'estat: `__pycache__/` i `.idea/` han desaparegut, i ara
només hi surt `.gitignore`. Fes-ne commit:

```bash
git status
git add .gitignore
git commit -m "chore: ignora els fitxers generats per Python i PyCharm"
```

### 4. Mira el resultat i comprova-ho

```bash
git log --oneline -3
python verifica.py 01
```

## Missatges de commit: Conventional Commits

El diari de la Rocinante segueix un format fix per als missatges:

```
<tipus>: <què fa el commit, en imperatiu>
```

| Tipus | Quan |
|---|---|
| `feat` | funcionalitat nova |
| `fix` | correcció d'un error |
| `docs` | documentació |
| `refactor` | canvi de codi que no canvia el comportament |
| `test` | tests |
| `chore` | manteniment (configuració, fitxers auxiliars...) |

La primera línia té 72 caràcters com a màxim. Exemples: `feat: afegeix la
Bobbie a la tripulació`, `fix: corregeix el càlcul del consum`.
