# La Rocinante · Aprèn Git al terminal

[![pipeline](https://gitlab.com/fp-dev-academy/introduccio-a-git/badges/main/pipeline.svg)](https://gitlab.com/fp-dev-academy/introduccio-a-git/-/pipelines)

**Vuit reptes de Git per resoldre al terminal, amb un verificador que et diu
a l'instant si ho tens bé.** Res de diapositives: un repositori real, amb una
història real, una tripulació que trenca coses i tu arreglant-les.

Ets el membre nou de la tripulació de la Rocinante (*The Expanse*). El diari
de bord de la nau és un repositori de Git, i a cada pas hi ha una feina:
recuperar una funció que algú ha esborrat, desfer les proves de l'Amos,
resoldre un conflicte entre la Naomi i l'Amos, trobar qui ha trencat la
navegació...

> **Estat:** en desenvolupament. El repositori de pràctica
> (`git-rocinante`) encara no s'ha publicat.

## Com es juga

1. Fes un **fork** del repositori de pràctica `git-rocinante` a GitLab i
   clona'l per SSH.
2. Cada repte comença en un tag. Crea-hi la teva branca i llegeix
   l'enunciat:

   ```bash
   git switch -c treball/pas-02 pas-02
   cat REPTE.md
   ```

3. Resol-lo amb Git i comprova-ho:

   ```bash
   python verifica.py 02
   ```

El verificador mira l'estat del repositori, no les ordres que has escrit: hi
ha més d'una manera de resoldre cada repte. Si falla algun criteri, et dona
una pista:

```
Pas 02 - La caixa negra

[OK] respostes/pas-02.txt versionat i amb format clau=valor
[OK] autor_esborrat correcte
[FALLA] hash_afegit correcte
        Pista: Hash curt (7 caràcters) del commit que va AFEGIR la funció, no del que la va esborrar.
[OK] rumb_emergencia existeix a rocinante/navegacio.py
[OK] almenys un commit nou sobre pas-02
[OK] no estàs en detached HEAD

5 de 6 criteris superats.
Encara no. Revisa les pistes o llegeix PISTES.md.
```

Encallat? Cada pas té un `PISTES.md`, ordenat de la pista més suau a la
més concreta, i totes les ordres del curs són a una
[xuleta](contingut/pas_00/ORDRES.md) (`ORDRES.md` al repositori de pràctica). Vols tornar a començar? `git switch -C treball/pas-NN pas-NN`.
Cada pas parteix del seu propi tag, de manera que pots saltar-te'n un.

## Els reptes

| Pas | Repte | Hi practiques |
|---|---|---|
| 00 | Embarcament | fork, `clone` per SSH, remots `origin` i `upstream`, `git config` |
| 01 | Primera entrada al diari | `status`, `add`, `commit`, `.gitignore`, Conventional Commits |
| 02 | La caixa negra | `log`, `show`, `diff`, detached HEAD, `restore --source`, `log -S` |
| 03 | Esborrar les proves | `restore --staged`, `commit --amend`, `revert` |
| 04 | Nova secció de tripulació | branques, `switch -c`, merge fast-forward |
| 05 | Conflicte a la sala de màquines | branques remotes, merge de tres vies, resoldre un conflicte |
| 06 | Algú ha trencat la navegació | `bisect`, `bisect run` |
| 07 | Informe a la flota | `push -u`, branques de seguiment, merge requests i revisió |

Tot plegat són unes **2 hores**. Els primers passos donen les ordres
completes, i els últims només l'objectiu.

Ampliació en preparació: `rebase`, `stash` i `cherry-pick`, `reset` i
`reflog`, i integració contínua.

## Què necessites

- **Git** i **Python 3.12 o superior**. No cal instal·lar res més.
- Un compte a **gitlab.com** amb una **clau SSH** (per al fork i per al
  pas 07).

Els enunciats estan escrits per a **Git Bash** (Windows). A macOS i Linux
funcionen igual: només cal triar un altre editor al pas 00 (`nano`,
`code --wait`...) en lloc de `notepad`.

## Fer-lo servir en un taller o en una classe

El repositori de pràctica es genera a partir d'aquest. Si vols adaptar els
reptes, traduir-los o publicar-ne la teva pròpia versió:

```bash
python3 generador/build.py --out sortida/git-rocinante   # genera el repositori de pràctica
python3 -m unittest discover -s tests -v                 # comprova que tot funciona
```

El generador és **determinista**: amb el mateix codi, produeix sempre els
mateixos hashos, a qualsevol màquina. Per això el verificador pot comparar
respostes com «el hash del commit que va afegir la funció» sense que la
resposta aparegui en clar enlloc.

| Carpeta | Contingut |
|---|---|
| `generador/` | Construeix el repositori de pràctica commit a commit (`passos/pas_NN.py`) |
| `contingut/` | Enunciats (`REPTE.md`), pistes (`PISTES.md`) i codi de cada pas |
| `verificador/` | `verifica.py`, que es copia al repositori de pràctica |
| `solucions/` | Una resolució correcta i diverses d'incorrectes de cada pas |
| `tests/` | Determinisme, estructura de la història i el verificador contra les solucions |

## Contribuir

Les propostes i els errors són benvinguts, en forma d'*issue* o de merge
request. Abans de canviar un pas, llegeix [`ESPECIFICACIO.md`](ESPECIFICACIO.md):
és la font de veritat. Primer es canvia l'especificació, i després el codi.

Un canvi està acabat quan:

- el generador continua sent determinista;
- la solució correcta de cada pas afectat supera `verifica.py` i cada
  solució incorrecta hi falla amb el missatge esperat;
- la CI és verda;
- la [prova manual](PROVA-MANUAL.md) no hi troba res a corregir (GitLab,
  Windows i PyCharm, que els tests no poden comprovar).

Les regles detallades són a [`CLAUDE.md`](CLAUDE.md).

## Llicència

- Codi: [MIT](LICENSE).
- Textos: [CC BY-SA 4.0](LICENSE-docs).

Un projecte de [fp-dev-academy](https://gitlab.com/fp-dev-academy).
