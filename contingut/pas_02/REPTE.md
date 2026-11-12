# Pas 02 · La caixa negra

L'Alex vol provar la maniobra d'evasió i la funció `rumb_emergencia()` ha
desaparegut de `rocinante/navegacio.py`. Ningú no recorda haver-la tocat.
Per sort, la nau té una caixa negra que ho recorda tot: **la història de
Git**.

## Què aprendràs

- Llegir la història: `git log`, `git show` i `git diff`.
- Viatjar a un commit antic en **detached HEAD** i tornar.
- Recuperar un fitxer tal com era en un commit antic: `git restore --source`.

## El repte

```bash
git switch -c treball/pas-02 pas-02
```

### 1. Llegeix la caixa negra

```bash
git log --oneline --graph
git log --format="%h %an: %s"
```

Cada línia és un commit: el **hash curt** (7 caràcters), l'autor i el
missatge. Per veure només els commits que han tocat un fitxer:

```bash
git log --oneline -- rocinante/navegacio.py
```

Per veure què va canviar en un commit concret (canvia `<hash>` per un dels
hashos de la llista):

```bash
git show <hash>
```

Les línies que comencen amb `-` es van esborrar i les que comencen amb `+`
es van afegir. Per comparar dos commits qualssevol:

```bash
git diff <hash_antic> <hash_nou> -- rocinante/navegacio.py
```

### 2. Respon les preguntes

Investiga quin commit va **afegir** `rumb_emergencia()` i quin la va
**esborrar**. Després crea el fitxer `respostes/pas-02.txt`:

```bash
mkdir -p respostes
notepad respostes/pas-02.txt
```

(El Bloc de notes et preguntarà si vols crear el fitxer: respon que sí.)
Escriu-hi aquestes dues línies, amb els teus valors:

```
autor_esborrat=<nom de qui va esborrar la funció>
hash_afegit=<hash curt del commit que la va afegir>
```

### 3. Viatja al passat

Pots moure't a qualsevol commit de la història. Ves al commit que va
afegir la funció:

```bash
git switch --detach <hash_afegit>
git status
grep -n "def rumb_emergencia" rocinante/navegacio.py
```

`git status` diu `HEAD detached at ...`: no ets a cap branca, sinó
directament sobre un commit. Serveix per mirar, no per treballar-hi. Torna
a la teva branca:

```bash
git switch -
git status
```

### 4. Recupera la funció

Porta el fitxer, tal com era en aquell commit, al teu directori de treball.
Revisa què canvia i fes-ne commit:

```bash
git restore --source=<hash_afegit> rocinante/navegacio.py
git diff
git add rocinante/navegacio.py
git commit -m "fix: recupera el rumb d'emergència"
```

I fes commit de les respostes:

```bash
git add respostes/pas-02.txt
git commit -m "docs: respon les preguntes del pas 02"
```

### 5. Comprova-ho

```bash
git log --oneline -3
python verifica.py 02
```

Fixa't que no has esborrat res de la història: el commit que va eliminar
la funció hi continua sent. Simplement n'has afegit un de nou que la torna
a portar.
