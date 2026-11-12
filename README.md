# Introducció a Git · La Rocinante

Curs pràctic de **Git per terminal** per a alumnat de 2n de CFGS de
**Desenvolupament d'Aplicacions Multiplataforma (DAM)**, pensat per a una
sessió de 2 hores. El fil narratiu és el diari de bord de la Rocinante
(*The Expanse*).

> **Estat:** en desenvolupament. El curs encara no està publicat.

## Com funciona

L'alumnat fa un fork del repositori guia `git-rocinante` i avança pas a pas.
Cada pas és un tag (`pas-00` … `pas-07`) amb un repte que es resol al
terminal i que comprova l'script `verifica.py`:

```bash
git switch -c treball/pas-NN pas-NN   # parteix de l'estat inicial del pas
cat REPTE.md                          # llegeix l'enunciat
# ... resol el repte ...
python verifica.py NN                 # comprova el resultat
```

| Pas | Títol | Aprenentatge |
|---|---|---|
| 00 | Embarcament | fork, `clone` per SSH, `remote`, configuració |
| 01 | Primera entrada al diari | `status`, `add`, `commit`, `.gitignore` |
| 02 | La caixa negra | `log`, `show`, `diff`, detached HEAD, `restore --source` |
| 03 | Esborrar les proves | `commit --amend`, `revert`, `restore --staged` |
| 04 | Nova secció de tripulació | branques, merge fast-forward |
| 05 | Conflicte a la sala de màquines | merge de tres vies i resolució de conflictes |
| 06 | Algú ha trencat la navegació | `bisect`, `bisect run` |
| 07 | Informe a la flota | `push`, branques de seguiment, merge requests |

## Aquest repositori

Aquest és el repositori **font**. Conté el generador que construeix el
repositori guia, el verificador, les solucions de referència i els tests.
El repositori guia es genera i **no s'edita mai a mà**.

| Document | Contingut |
|---|---|
| [`ESPECIFICACIO.md`](ESPECIFICACIO.md) | Font de veritat: passos, estats inicials i criteris de verificació |
| [`CLAUDE.md`](CLAUDE.md) | Regles del generador, del verificador i definició de feina acabada |

## Llicència

- Codi: [MIT](LICENSE).
- Textos: [CC BY-SA 4.0](LICENSE-docs).

Material del grup [fp-dev-academy](https://gitlab.com/fp-dev-academy).
