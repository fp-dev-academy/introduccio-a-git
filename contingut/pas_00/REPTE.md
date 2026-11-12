# Pas 00 · Embarcament

> Feina prèvia: fes aquest pas **abans de la sessió**.

Ningú no puja a la Rocinante sense registrar-se. Necessites la teva còpia
del diari de bord, connectada amb la de la flota, i que Git sàpiga qui ets.

## Què aprendràs

- Què és un **fork** i per què en fas un.
- Clonar un repositori per **SSH**.
- Què són els **remots** `origin` i `upstream`.
- Configurar Git: nom, correu i editor.

## El repte

### 1. Fes el fork (a GitLab, al navegador)

Un fork és una còpia del repositori al **teu** compte de GitLab. Hi podràs
pujar canvis sense tocar el repositori de la flota.

1. Obre <https://gitlab.com/fp-dev-academy/git-rocinante>.
2. Fes clic a **Fork**.
3. A *Project URL*, tria el teu usuari com a espai de noms. Deixa la resta
   com està i fes clic a **Fork project**.

### 2. Clona el teu fork per SSH

Obre el terminal de PyCharm (Git Bash), situa't a la carpeta on vulguis
guardar els projectes i clona el **teu fork** (no el de la flota). Canvia
`<usuari>` pel teu usuari de GitLab:

```bash
git clone git@gitlab.com:<usuari>/git-rocinante.git
cd git-rocinante
```

Git ha creat automàticament el remot `origin`, que apunta al teu fork:

```bash
git remote -v
```

### 3. Connecta't amb la flota

Afegeix un segon remot, `upstream`, que apunti al repositori de la flota.
D'aquí és d'on arribaran les correccions, si mai n'hi ha:

```bash
git remote add upstream git@gitlab.com:fp-dev-academy/git-rocinante.git
git remote -v
```

Ara n'hi ha d'haver quatre línies: `origin` i `upstream`, totes dues per a
`fetch` i `push`.

### 4. Digues a Git qui ets

```bash
git config --global user.name "El teu nom i cognom"
git config --global user.email "el-teu-correu@exemple.cat"
git config --global core.editor notepad
```

- El nom i el correu apareixeran a cada commit que facis. Fes servir el
  correu del teu compte de GitLab, perquè GitLab associï els commits al
  teu usuari.
- `core.editor notepad` fa que, quan Git necessiti que escriguis un
  missatge, obri el Bloc de notes. Escriu el missatge, desa i **tanca** la
  finestra: fins que no la tanquis, Git espera.

Comprova-ho:

```bash
git config --global --list
```

### 5. Mira els passos del curs

Cada pas del curs és un tag:

```bash
git tag
```

### 6. Comprova-ho

Des de la branca `main`:

```bash
python verifica.py 00
```

Si `python` no es troba, fes servir `py verifica.py 00` (i, a partir d'ara,
`py` cada cop que el curs digui `python`).

## Quan ho tinguis

Quan `verifica.py` digui que ho tens tot, ja ets a bord. El pas següent
comença així:

```bash
git switch -c treball/pas-01 pas-01
cat REPTE.md
```
