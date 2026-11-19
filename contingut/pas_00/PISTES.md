# Pistes · Pas 00

Llegeix només la pista que necessitis.

## `git clone` diu `Permission denied (publickey)`

GitHub no reconeix la teva clau SSH. Comprova-ho:

```bash
ssh -T git@github.com
```

Si no respon `Hi <usuari>! You've successfully authenticated`, la clau no
està configurada. Revisa *Settings → SSH and GPG keys* al teu compte de
GitHub i que la clau pública que hi has posat és la del fitxer
`~/.ssh/id_ed25519.pub` d'aquest ordinador.

## `verifica.py` diu que `origin` apunta al repositori guia

Has clonat el repositori de la flota en lloc del teu fork. No cal tornar a
clonar: canvia l'adreça d'`origin` per la del teu fork.

```bash
git remote set-url origin git@github.com:<usuari>/git-rocinante.git
```

## `verifica.py` diu que `origin` no fa servir SSH

Has clonat amb l'adreça `https://...`. Canvia-la per la d'SSH:

```bash
git remote set-url origin git@github.com:<usuari>/git-rocinante.git
```

## M'he equivocat en escriure l'adreça d'`upstream`

`git remote add` no es pot repetir amb el mateix nom. Corregeix-la:

```bash
git remote set-url upstream git@github.com:fp-dev-academy/git-rocinante.git
```

## `python: command not found`

A Windows, de vegades el Python només respon com a `py`:

```bash
py --version
py verifica.py 00
```

## No veig els tags

Si `git tag` no mostra res, segurament has fet el fork amb *Copy the `main`
branch only* marcada. Demana els tags a la flota:

```bash
git fetch upstream --tags
```

Les branques de la tripulació també hi falten, però les trobaràs a
`upstream` quan les necessitis (pas 05).

## M'he equivocat en el nom o el correu

Torna a executar la mateixa ordre amb el valor correcte. La configuració
nova substitueix l'anterior.
