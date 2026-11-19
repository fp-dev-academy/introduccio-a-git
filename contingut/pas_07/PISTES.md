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
ssh -T git@github.com
```

Ha de respondre `Hi <usuari>! You've successfully authenticated`. Si no, revisa la clau SSH (vegeu les
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

## La pull request apunta al repositori de la flota

A *base repository*, tria `<usuari>/git-rocinante`. Si ja l'has creada,
tanca-la (*Close pull request*) i obre'n una de nova. No passa res: la flota
no la fusionarà.

## L'altra persona no pot comentar la pull request

El fork d'un repositori públic és públic: qualsevol persona amb un compte de
GitHub hi pot comentar. Comprova que ha iniciat sessió i que li has passat
l'enllaç de la PR del teu fork, no el de la flota.
