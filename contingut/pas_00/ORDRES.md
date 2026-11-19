# Xuleta d'ordres de Git

Totes les ordres que surten als reptes, agrupades per tema. La columna
**Pas** indica on apareixen per primera vegada. Els valors entre `< >` són
els que has de canviar (`<hash>`, `<fitxer>`, `<branca>`...).

## El flux de cada pas

```bash
git switch -c treball/pas-NN pas-NN   # crea la teva branca de treball
cat REPTE.md                          # llegeix l'enunciat
python verifica.py NN                 # comprova el resultat
git switch -C treball/pas-NN pas-NN   # torna a començar el pas des de zero
```

## Configurar i connectar

| Ordre | Què fa | Pas |
|---|---|---|
| `git config --global user.name "Nom Cognom"` | Defineix el nom que surt als commits | 00 |
| `git config --global user.email "correu@exemple.cat"` | Defineix el correu dels commits | 00 |
| `git config --global core.editor notepad` | Tria l'editor per als missatges (a macOS o Linux, `nano`) | 00 |
| `git config --global --list` | Mostra la configuració | 00 |
| `git clone git@github.com:<usuari>/git-rocinante.git` | Copia un repositori remot al teu ordinador | 00 |
| `git remote -v` | Llista els remots i les seves adreces | 00 |
| `git remote add upstream <url>` | Afegeix un remot nou | 00 |
| `git remote set-url origin <url>` | Canvia l'adreça d'un remot | 00 |
| `git tag` | Llista els tags (cada pas del curs és un tag) | 00 |
| `git fetch origin --tags` | Porta del remot els commits, les branques i els tags que no tens | 00 |

## Les tres zones: guardar canvis

```
directori de treball  --git add-->  staging  --git commit-->  repositori
```

| Ordre | Què fa | Pas |
|---|---|---|
| `git status` | Diu què hi ha a cada zona. Fes-la servir sovint | 01 |
| `git diff` | Mostra els canvis que encara no són al staging | 01 |
| `git add <fitxer>` | Passa un fitxer al staging (millor que `git add .`) | 01 |
| `git commit -m "feat: ..."` | Crea un commit amb el que hi ha al staging | 01 |
| `git rm -r --cached <carpeta>` | Deixa de versionar una carpeta sense esborrar-la del disc | 01 |

El fitxer `.gitignore` diu quins fitxers no s'han de versionar mai
(`__pycache__/`, `.idea/`...).

## Llegir la història

| Ordre | Què fa | Pas |
|---|---|---|
| `git log --oneline` | Un commit per línia: hash curt i missatge | 01 |
| `git log --oneline --graph --all` | La història de totes les branques, en forma d'arbre | 02 |
| `git log --format="%h %an: %s"` | Hash, autor i missatge de cada commit | 02 |
| `git log --oneline -- <fitxer>` | Només els commits que han tocat un fitxer | 02 |
| `git log --oneline -S <text> -- <fitxer>` | Els commits que han afegit o esborrat un text | 02 |
| `git show <hash>` | Què va canviar en un commit (`-` esborrat, `+` afegit) | 02 |
| `git diff <hash1> <hash2> -- <fitxer>` | Diferències entre dos commits | 02 |

Si la sortida no s'acaba, prem `q` per sortir del paginador.

## Moure's per la història

| Ordre | Què fa | Pas |
|---|---|---|
| `git switch --detach <hash>` | Ves a un commit antic (detached HEAD: per mirar, no per treballar) | 02 |
| `git switch -` | Torna a la branca d'abans | 02 |
| `git restore --source=<hash> <fitxer>` | Porta un fitxer tal com era en un commit | 02 |

## Desfer: què vull desfer → quina ordre

| Vull desfer... | Ordre | Pas |
|---|---|---|
| un canvi que encara no he afegit al staging | `git restore <fitxer>` | 03 |
| un fitxer que he afegit al staging per error | `git restore --staged <fitxer>` | 03 |
| el missatge (o el contingut) de l'**últim** commit, si **no l'he pujat** | `git commit --amend -m "..."` | 03 |
| un commit que **ja és compartit** (amb un commit nou que el desfà) | `git revert <hash>` | 03 |
| un merge amb conflictes que se m'ha complicat | `git merge --abort` | 05 |
| un revert amb conflictes | `git revert --abort` | 03 |
| un bisect començat | `git bisect reset` | 06 |

`git reset` i `git rebase` reescriuen la història: en aquest curs no
calen, i si els fas servir sobre commits compartits trenques la història
dels altres.

## Branques

| Ordre | Què fa | Pas |
|---|---|---|
| `git branch` | Llista les branques locals (l'asterisc és la teva) | 04 |
| `git branch -a` | També les remotes (`remotes/origin/...`) | 05 |
| `git branch -vv` | Branques amb la remota que segueixen | 07 |
| `git switch -c <branca>` | Crea una branca i s'hi posa | 04 |
| `git switch <branca>` | Canvia de branca | 04 |
| `git branch -d <branca>` | Esborra una branca ja integrada (`-D` la força) | 04 |
| `git merge <branca>` | Integra una branca a la branca actual | 04 |
| `git merge origin/<branca>` | Integra una branca remota | 05 |

**Fast-forward:** si la teva branca no s'ha mogut, el merge només l'avança.
**Conflicte:** si les dues branques han canviat les mateixes línies, Git
escriu les dues versions entre `<<<<<<<`, `=======` i `>>>>>>>`. Deixa el
fitxer com ha de quedar, sense marcadors, i després `git add <fitxer>` i
`git commit`.

## Buscar un error

| Ordre | Què fa | Pas |
|---|---|---|
| `git bisect start <dolent> <bo>` | Comença una cerca binària entre dos commits | 06 |
| `git bisect good` / `git bisect bad` | Marca el commit actual com a bo o dolent | 06 |
| `git bisect run python tests/test_x.py` | Ho fa sol: executa l'ordre a cada pas (0 = bo, 1 = dolent) | 06 |
| `git bisect reset` | Acaba la cerca i torna a la teva branca | 06 |

## Treballar amb el remot

| Ordre | Què fa | Pas |
|---|---|---|
| `git push -u origin <branca>` | Puja una branca i hi connecta la local (seguiment) | 07 |
| `git push -u origin --all` | Puja totes les branques, amb seguiment | 07 |
| `git push` | Puja els commits nous de la branca actual | 07 |
| `git pull` | Porta i integra els commits nous de la remota | 07 |
| `git fetch origin` | Porta les novetats del remot sense integrar-les | 05 |

## Missatges de commit (Conventional Commits)

```
<tipus>: <què fa el commit, en imperatiu>
```

`feat` (funcionalitat nova), `fix` (correcció), `docs` (documentació),
`refactor` (canvi sense canviar el comportament), `test` (tests), `chore`
(manteniment). Màxim 72 caràcters a la primera línia.
