# Pistes · Pas 00

Llegeix només la pista que necessitis.

## `git clone` diu `Permission denied (publickey)`

GitLab no reconeix la teva clau SSH. Comprova-ho:

```bash
ssh -T git@gitlab.com
```

Si no respon `Welcome to GitLab`, la clau no està configurada. Revisa
*Preferences → SSH Keys* al teu compte de GitLab i que la clau pública que
hi has posat és la del fitxer `~/.ssh/id_ed25519.pub` d'aquest ordinador.

## `verifica.py` diu que `origin` apunta al repositori guia

Has clonat el repositori de la flota en lloc del teu fork. No cal tornar a
clonar: canvia l'adreça d'`origin` per la del teu fork.

```bash
git remote set-url origin git@gitlab.com:<usuari>/git-rocinante.git
```

## `verifica.py` diu que `origin` no fa servir SSH

Has clonat amb l'adreça `https://...`. Canvia-la per la d'SSH:

```bash
git remote set-url origin git@gitlab.com:<usuari>/git-rocinante.git
```

## M'he equivocat en escriure l'adreça d'`upstream`

`git remote add` no es pot repetir amb el mateix nom. Corregeix-la:

```bash
git remote set-url upstream git@gitlab.com:fp-dev-academy/git-rocinante.git
```

## `python: command not found`

A Windows, de vegades el Python només respon com a `py`:

```bash
py --version
py verifica.py 00
```

## No veig els tags

Si `git tag` no mostra res, demana'ls a `origin`:

```bash
git fetch origin --tags
```

## M'he equivocat en el nom o el correu

Torna a executar la mateixa ordre amb el valor correcte. La configuració
nova substitueix l'anterior.
