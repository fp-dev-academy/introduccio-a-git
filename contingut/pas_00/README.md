# Diari de bord de la Rocinante

Benvinguda a bord. La Rocinante és una corbeta marciana amb una tripulació de
quatre persones que s'equivoquen, discuteixen i, de tant en tant, trenquen
coses. Tu acabes d'enrolar-t'hi i el teu primer encàrrec és aprendre a fer
servir el seu **diari de bord**: un repositori de Git.

Aquest és un curs pràctic de **Git per terminal**. Cada pas és un repte que
resols tu mateix i que comprova l'script `verifica.py`.

## Abans de començar

Necessites:

- **Git for Windows**, amb **Git Bash** com a terminal de PyCharm
  (*Settings → Tools → Terminal → Shell path*:
  `C:\Program Files\Git\bin\bash.exe`).
- **Python 3.12 o superior**. Comprova-ho amb `python --version`.
  Si Git Bash respon `command not found`, prova `py --version`: si funciona,
  escriu `py` cada vegada que aquí posi `python`.
- Un compte a **github.com** amb una **clau SSH** configurada. Comprova-ho:

  ```bash
  ssh -T git@github.com
  ```

  Ha de respondre `Hi el-teu-usuari! You've successfully authenticated`.

## Primer pas: l'embarcament

El primer repte (pas 00) es fa **abans de clonar**, de manera que no el
pots llegir al terminal. Llegeix-lo aquí, a GitHub:
[`REPTE.md` del pas 00](https://github.com/fp-dev-academy/git-rocinante/blob/pas-00/REPTE.md).

## Com funciona cada pas

Cada pas comença en un tag (`pas-01`, `pas-02`...), que és l'estat del diari
de bord en aquell moment. Per a cada pas:

```bash
git switch -c treball/pas-NN pas-NN   # crea la teva branca de treball
cat REPTE.md                          # llegeix l'enunciat
# ... resol el repte ...
python verifica.py NN                 # comprova el resultat
```

Canvia `NN` pel número del pas (`01`, `02`...). Si et quedes encallat,
llegeix `PISTES.md`. Totes les ordres del curs són a la
[xuleta d'ordres](ORDRES.md).

Cada pas parteix del seu propi tag: encara que un pas anterior et surti
malament, pots fer el següent. Si vols tornar a començar un pas des de zero:

```bash
git switch -C treball/pas-NN pas-NN
```

## Els passos

| Pas | Títol | Aprendràs |
|---|---|---|
| 00 | Embarcament | fork, `clone` per SSH, `remote`, configuració |
| 01 | Primera entrada al diari | `status`, `add`, `commit`, `.gitignore` |
| 02 | La caixa negra | `log`, `show`, `diff`, detached HEAD, `restore --source` |
| 03 | Esborrar les proves | `commit --amend`, `revert`, `restore --staged` |
| 04 | Nova secció de tripulació | branques, merge fast-forward |
| 05 | Conflicte a la sala de màquines | merge de tres vies i conflictes |
| 06 | Algú ha trencat la navegació | `bisect` |
| 07 | Informe a la flota | `push`, branques de seguiment, pull requests |

## L'aplicació

El diari de bord porta una petita aplicació en Python. No cal que en
modifiquis gaire res: és l'excusa per fer commits.

```bash
python -m rocinante                        # ajuda
python -m rocinante tripulacio             # llista la tripulació
python -m rocinante consum 100 1           # consum de massa de reacció
python -m rocinante trajecte 384400 20     # temps de trajecte, en hores
python tests/test_navegacio.py             # executa un fitxer de tests
```

## Llicència

- Codi: [MIT](LICENSE).
- Textos: [CC BY-SA 4.0](LICENSE-docs).

Material del grup [fp-dev-academy](https://github.com/fp-dev-academy).
