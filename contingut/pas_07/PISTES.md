# Pistes · Pas 07

Llegeix només la pista que necessitis.

## `verifica.py` diu que el pas 07 no existeix

Ets en una branca d'un pas anterior, on `verifica.py` encara no coneix
aquest pas:

```bash
git switch -c treball/pas-07 pas-07
python verifica.py 07
```

## `git push` diu `Permission denied (publickey)` o no es pot connectar

```bash
ssh -T git@gitlab.com
```

Ha de respondre `Welcome to GitLab`. Si no, revisa la clau SSH (vegeu les
pistes del pas 00).

## `git push` diu `rejected` o `fetch first`

La branca remota té commits que tu no tens. No hauria de passar en aquest
curs, si cadascú treballa al seu fork. Mira què hi ha:

```bash
git fetch origin
git log --oneline --graph --all -8
```

## `verifica.py` diu que una branca no està al dia

Has fet commits després del push. Puja'ls:

```bash
git switch <branca>
git status
git push
```

## `verifica.py` diu que `treball/pas-05` no té upstream

L'has pujada sense `-u`. Torna-la a pujar amb seguiment:

```bash
git push -u origin treball/pas-05
```

## La merge request apunta al repositori de la flota

A *Target branch*, canvia el projecte per `<usuari>/git-rocinante`. Si ja
l'has creada, tanca-la (*Close merge request*) i obre'n una de nova.

## L'altra persona no pot comentar la merge request

El teu fork ha de ser visible per a aquesta persona. Comprova-ho a
*Settings → General → Visibility*, o afegeix-la com a membre del projecte
amb el rol *Reporter*.
