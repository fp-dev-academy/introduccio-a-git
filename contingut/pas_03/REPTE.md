# Pas 03 · Esborrar les proves

L'Amos ha estat provant coses al diari de bord. Ha deixat dos regals:

- l'últim commit té el missatge `asdf`, que no explica res;
- uns quants commits abans, un commit que diu `feat: millora la sortida de
  la CLI` fa, en realitat, que l'aplicació escrigui `AMOS WAS HERE` cada
  vegada que s'executa.

```bash
git switch -c treball/pas-03 pas-03
python -m rocinante
git log --oneline -6
```

## Què aprendràs

- Treure un canvi del *staging* (`git restore --staged`) i descartar-lo
  (`git restore`).
- Corregir l'últim commit amb `git commit --amend`.
- Desfer un commit antic amb `git revert`.
- Quan s'ha de fer servir cadascun, i per què `git reset` no és l'eina per
  desfer coses compartides.

## Desfer: quina eina, i quan

| Situació | Eina | Què fa amb la història |
|---|---|---|
| Canvi al directori de treball que no vols | `git restore <fitxer>` | Res: el canvi no ha arribat mai a la història |
| Fitxer al *staging* que no volies afegir | `git restore --staged <fitxer>` | Res |
| L'**últim** commit està malament i **no l'has compartit** | `git commit --amend` | **Substitueix** l'últim commit per un de nou |
| Un commit (antic o recent) **ja compartit** està malament | `git revert <hash>` | **Afegeix** un commit nou que en desfà els canvis |

`git reset` mou la branca enrere i fa desaparèixer commits. És útil en
local, però si aquells commits ja els tenen els companys, els trenca la
història. Ho veuràs a l'ampliació (pas 10).

> **Una ficció necessària.** El commit `asdf` ja és al repositori de la
> flota, és a dir, tècnicament ja està compartit. Per practicar, fes com si
> l'Amos encara no l'hagués pujat. A la vida real, un commit que ja has pujat
> **no es modifica** amb `--amend`: es corregeix amb un commit nou. Per això,
> a `main`, la tripulació l'ha deixat tal com està.

## El repte

L'**ordre** dels apartats 2 i 3 és important: `--amend` només pot modificar
l'**últim** commit. Si primer fas el revert, l'últim commit ja no serà el
d'`asdf`.

### 1. Practica: staging i descartar (no es verifica)

Fes un canvi qualsevol a `README.md` i observa'l a cada zona:

```bash
echo "nota de prova" >> README.md
git status
git add README.md
git status                      # és al staging
git restore --staged README.md
git status                      # torna a ser només al directori de treball
git restore README.md
git status                      # el canvi ha desaparegut
```

### 2. Corregeix el missatge `asdf`

Mira què va canviar realment l'últim commit:

```bash
git show HEAD
```

Corregeix-ne el missatge (en format Conventional Commits) sense canviar-ne
el contingut:

```bash
git commit --amend -m "feat: ascendeix l'Amos a mecànic en cap"
git log --oneline -3
```

Fixa't que el hash de l'últim commit ha canviat: no és el mateix commit
modificat, sinó un commit **nou** que el substitueix.

### 3. Desfés l'"AMOS WAS HERE"

Busca el commit que el va introduir:

```bash
git log --oneline -- rocinante/__main__.py
git show <hash>
```

Desfés-lo amb un revert:

```bash
git revert <hash>
```

Git obrirà el Bloc de notes amb un missatge ja escrit
(`Revert "feat: millora la sortida de la CLI"`). És vàlid tal com està:
desa i tanca la finestra.

```bash
python -m rocinante
git log --oneline -4
```

El commit de l'Amos **continua a la història**, i al damunt hi ha un commit
nou que en desfà els canvis. Qualsevol company veurà què va passar i quan.

### 4. Comprova-ho

```bash
python verifica.py 03
```
