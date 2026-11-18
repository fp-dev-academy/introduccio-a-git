# Guia docent

Com provar el curs, entendre'l i portar-lo a l'aula. Complementa
`ESPECIFICACIO.md` (què fa cada pas i per què) i `PROVA-MANUAL.md` (llista de
comprovació a Windows abans de publicar).

L'ordre recomanat és:

1. **Assaig al Mac** (1 h aprox.): fer els vuit passos un mateix, amb la
   configuració de git aïllada, per entendre què demana cada pas i com respon
   el verificador. Són els apartats 1 i 2 d'aquesta guia.
2. **Prova manual a Windows** amb un compte de prova: `PROVA-MANUAL.md`.
3. **A l'aula**: apartat 3.

Totes les sortides d'aquesta guia s'han obtingut executant les ordres
(2026-11-18, macOS, Python 3.15.2). Els hashos corresponen al repositori
generat amb `pas-07` = `74e5a15`.

## 1. Preparar l'assaig

El pas 00 escriu a la configuració **global** de git (`user.name`,
`user.email`, `core.editor notepad`). Per no tocar la teva, obre un terminal
nou i fes que git en faci servir una de buida només en aquell terminal:

```bash
mkdir -p ~/assaig-rocinante/xdg && cd ~/assaig-rocinante
: > gitconfig
export GIT_CONFIG_GLOBAL=~/assaig-rocinante/gitconfig  # en lloc de ~/.gitconfig
export XDG_CONFIG_HOME=~/assaig-rocinante/xdg          # en lloc de ~/.config/git/ignore
export GIT_EDITOR=nano                                 # al Mac no hi ha notepad
alias python=python3                                   # els enunciats diuen python
```

- `XDG_CONFIG_HOME` cal perquè `~/.config/git/ignore` ja ignora `.idea/`, i
  al pas 01 no el veuries a `git status` (l'alumnat sí que el veurà).
- `GIT_EDITOR` té prioritat sobre `core.editor`: el pas 00 hi posarà
  `notepad`, però `git revert` i el merge del pas 05 obriran `nano`
  (`Ctrl+O`, `Enter`, `Ctrl+X`).
- En tancar el terminal, tot torna a ser com abans.

Després tens dues opcions per al repositori:

- **Amb GitLab (recomanat, com l'alumnat):** fes el fork de
  `fp-dev-academy/git-rocinante` al teu espai de noms i clona'l per SSH
  (`git clone git@gitlab.com:<usuari>/git-rocinante.git`). El pas 07 hi
  crearà branques i una merge request; en acabar, esborra el fork.
- **Sense xarxa:** genera el repositori i fes-ne un clon local. Els passos
  01–06 funcionen igual; el 00 i el 07 només es poden simular.

  ```bash
  python3 ~/gitLab/fp-dev-academy/introduccio-a-git/generador/build.py --out ~/assaig-rocinante/guia
  git clone ~/assaig-rocinante/guia git-rocinante && cd git-rocinante
  git remote set-url origin git@gitlab.com:provador/git-rocinante.git
  ```

Tingues obert al costat el `REPTE.md` de cada pas: aquesta guia no el
repeteix, explica què hi ha al darrere.

## 2. Els passos, un per un

Cada pas comença igual: `git switch -c treball/pas-NN pas-NN` i
`cat REPTE.md`. El verificador (`python verifica.py NN`) mira **l'estat del
repositori**, no les ordres; per això hi ha més d'una manera bona de fer-ho.
Si un criteri falla, la línia `[FALLA]` porta una pista, i `PISTES.md` en té
més.

> Les respostes dels passos 02 i 06 apareixen més avall perquè les necessitaràs
> per ajudar a l'aula. `verifica.py` no les mostra (les compara pel SHA-256).

### Pas 00 · Embarcament (10', millor com a feina prèvia)

- **Idea clau:** un *fork* és una còpia teva a GitLab; `origin` és el teu
  fork i `upstream`, el repositori original.
- **Què es comprova:** nom, correu i editor configurats; `origin` per SSH i
  que no sigui el repositori guia; `upstream` existeix; hi ha els 9 tags;
  `python` ≥ 3.12.
- **Sortida real** abans de configurar git: `5 de 8 criteris superats`, amb
  una pista que és literalment l'ordre que falta
  (`git config --global user.name "El teu nom i cognom"`). Després,
  `8 de 8`.
- **A l'aula:** el problema típic no és git, és l'entorn (clau SSH, `python`
  que no respon a Git Bash). Per això convé que arribin amb el pas 00 fet i
  amb `ssh -T git@gitlab.com` funcionant.

### Pas 01 · Primera entrada al diari (10')

- **Idea clau:** les tres zones (directori de treball → staging → història)
  i que hi ha fitxers que no s'han de versionar mai.
- **Què fan:** executen l'aplicació (crea `__pycache__/`), s'afegeixen a
  `TRIPULACIO` i en fan commit; creen el `.gitignore` i en fan un altre.
- **Què es comprova:** 2 commits nous, un tripulant més, `.gitignore` amb
  `__pycache__` i `.idea`, res d'això versionat, directori net i missatges
  en format Conventional Commits.
- **Sortida real** amb només el primer commit: `3 de 6`, amb pistes per al
  segon commit i el `.gitignore`.
- **Error que val la pena provocar:** `git add .` abans del `.gitignore`. La
  pista porta a `git rm -r --cached`, i és el moment d'explicar que ignorar
  un fitxer no el treu si ja és al repositori.

### Pas 02 · La caixa negra (15')

- **Idea clau:** la història ho recorda tot; es pot consultar
  (`log`, `show`, `diff`), visitar (*detached HEAD*) i recuperar-ne fitxers
  (`restore --source`) sense reescriure-la.
- **Què fan:** troben qui va esborrar `rumb_emergencia()` i en quin commit
  es va afegir, ho escriuen a `respostes/pas-02.txt`, visiten aquell commit,
  tornen i recuperen la funció.
- **Respostes:** `autor_esborrat=Amos Burton` (commit `609551f refactor:
  neteja codi mort`) i `hash_afegit=dc6a2c1` (`feat: afegeix el rumb
  d'emergència`). S'accepta també només `amos`, i qualsevol prefix de 7 o més
  caràcters del hash.
- **La drecera:** `git log --oneline -S rumb_emergencia --
  rocinante/navegacio.py` mostra exactament aquests dos commits.
- **Error típic:** posar el hash del commit que la va esborrar. La pista ho
  diu: «del commit que va AFEGIR la funció, no del que la va esborrar».
- **A l'aula:** el `git status` en detached HEAD (`HEAD detached at dc6a2c1`)
  espanta. Explica que no és un error: és mirar el passat sense estar a cap
  branca, i `git switch -` hi torna.

### Pas 03 · Esborrar les proves (15')

- **Idea clau:** dues maneres de desfer. `--amend` **reescriu** l'últim
  commit (només si no s'ha compartit); `revert` crea un commit nou que el
  desfà (per al que ja és compartit).
- **Què fan:** practiquen `restore --staged` i `restore` (no es verifica),
  corregeixen el missatge `asdf` amb `--amend` i fan el revert del commit
  `24b8ee6 feat: millora la sortida de la CLI`, que imprimeix
  `AMOS WAS HERE`.
- **L'ordre importa:** primer l'`--amend`, després el revert. Si es fa al
  revés, el verificador ho detecta (`5 de 7`) i dona la sortida:
  «Has fet el revert abans de l'--amend? ... Torna a començar
  (`git switch -C treball/pas-03 pas-03`)».
- **A l'aula:** la «ficció» del pas és que el commit `asdf` encara no s'ha
  compartit. Val la pena dir en veu alta que, a la feina, un commit pujat no
  es toca amb `--amend`.

### Pas 04 · Nova secció de tripulació (10')

- **Idea clau:** una branca és només un punter; si la branca on integres no
  ha avançat, el merge només mou el punter (*fast-forward*).
- **Què fan:** creen `feature/rols`, hi afegeixen `per_rol()`, tornen a
  `treball/pas-04` (on la funció encara no hi és: `grep -c` dona `0`) i fan
  el merge. Git diu `Fast-forward`.
- **Què es comprova:** la branca existeix amb un commit, `treball/pas-04`
  apunta al mateix commit i `per_rol` hi és (`3 de 3`).
- **A l'aula:** dibuixar el graf de l'enunciat a la pissarra abans i després
  del merge. És la base del pas 05.

### Pas 05 · Conflicte a la sala de màquines (20')

- **Idea clau:** quan dues branques canvien les mateixes línies, git no
  decideix: marca el conflicte i ho resol una persona.
- **Què fan:** integren `origin/tripulacio/naomi-eficiencia`
  (fast-forward) i `origin/tripulacio/amos-potencia`, que dona
  `CONFLICT (content): Merge conflict in rocinante/combustible.py` amb **dos
  blocs**: la signatura i el `return`.
- **La resolució bona** combina les dues idees, i el test ho exigeix:

  ```python
  def calcula_consum(massa_t, acceleracio_g, eficiencia=1.0, mode_combat=False):
      ...
      factor = 1.5 if mode_combat else 1.0
      return massa_t * acceleracio_g * 0.8 * factor / eficiencia
  ```

- **Què es comprova:** les dues branques integrades, un commit de merge,
  cap marcador, `python tests/test_combustible.py` en verd i que la
  resolució no sigui una còpia del merge de la tripulació (`v1.0`).
- **A l'aula:** és el pas on més s'encallen. El test falla **a propòsit**
  abans de començar (`FAILED (errors=3)`): avisa'ls perquè no pensin que han
  trencat res. Error típic: quedar-se només amb una de les dues versions; el
  test ho detecta.

### Pas 06 · Algú ha trencat la navegació (15', opcional si es va tard)

- **Idea clau:** `git bisect` busca el commit culpable per cerca binària:
  17 commits es resolen en 4 proves.
- **El símptoma:** `python -m rocinante trajecte 36000 10` diu
  `10.00 h` i hauria de dir `1.00 h`.
- **Què fan:** `git bisect start pas-06 v1.0` i
  `git bisect run python tests/test_navegacio.py`. Git acaba amb
  `9f0fd88... is the first bad commit` (`refactor: unifica conversions
  d'unitats`, de la Naomi: Alex tenia raó). Després, `git bisect reset`,
  `culpable=9f0fd88` a `respostes/pas-06.txt`, revert del culpable i commit.
- **Comprovació final:** el trajecte torna a donar `1.00 h` i el verificador
  dona `5 de 5`.
- **Atenció:** si executen `python verifica.py 06` **abans** de
  `git bisect reset`, el verificador que tenen al directori és el d'un commit
  antic. Respon que el pas 06 no existeix, que hi ha un bisect en curs i
  que cal fer `git bisect reset` (codi de sortida 2).

### Pas 07 · Informe a la flota (15')

- **Idea clau:** `push -u` puja una branca i la deixa enllaçada amb la
  remota; la revisió es fa amb una merge request.
- **Què fan:** `git push -u origin --all`, obren una merge request **dins
  del propi fork** de `treball/pas-05` cap a `main` (GitLab proposa per
  defecte el repositori guia: cal canviar-ho) i algú hi comenta una línia.
- **Què es comprova:** cada branca `treball/pas-*` local existeix a `origin`
  amb el mateix commit, i `treball/pas-05` té upstream. Abans del push,
  `0 de 8`; després, `8 de 8`.
- **El que no es pot comprovar en local:** la merge request i el comentari.
  Es revisen a GitLab.

## 3. A l'aula

**Abans de la sessió**

- `git-rocinante` ha de ser **públic**: si és privat, qui no és membre del
  grup no el veu ni en pot fer el fork.
- Encarregar el pas 00 com a feina prèvia, amb `python verifica.py 00` en
  `8 de 8` i `ssh -T git@gitlab.com` saludant-los pel nom d'usuari.
- Tenir a mà les respostes de l'apartat 2 i `ORDRES.md` (la xuleta).

**Durant la sessió (110' + 10' de marge)**

| Temps | Pas | Punt de control |
|---|---|---|
| 0–10' | 00 (repàs) | Tothom té `8 de 8` |
| 10–20' | 01 | `git log --oneline -3` amb els dos commits seus |
| 20–35' | 02 | Han vist `HEAD detached at ...` i n'han sortit |
| 35–50' | 03 | `python -m rocinante` ja no diu `AMOS WAS HERE` |
| 50–60' | 04 | Han vist `Fast-forward` |
| 60–80' | 05 | Test en verd després del merge |
| 80–95' | 06 | `Temps de trajecte: 1.00 h` (si es va tard, se salta) |
| 95–110' | 07 | Merge request oberta al seu fork |

- Els passos 00–02 donen les ordres completes; el 03 i el 04, ordres i
  objectiu; del 05 en endavant, només l'objectiu. A partir del 05 conviden
  a buscar a `ORDRES.md` abans de preguntar.
- Cap pas no depèn de l'anterior: qui s'encalla pot passar al següent amb
  `git switch -c treball/pas-NN pas-NN` i tornar-hi més tard.

**Després de la sessió**

- Revisar les merge requests (el pas 07 és l'únic resultat visible a
  GitLab).
- Els passos 08–11 (ampliació autònoma) encara no estan publicats.

## 4. Troballes de l'assaig (2026-11-18)

1. **Pas 06, verificador durant el bisect (resolt).** Amb el bisect a mig
   fer, `HEAD` és un commit anterior a `pas-06` i el `verifica.py` del
   directori no coneix el pas 06. Abans suggeria `git switch -C`, que no
   tanca el bisect. Ara, si hi ha un `BISECT_LOG`, demana `git bisect reset`
   (especificació, apartat 3 bis), i `PISTES.md` del pas 06 ho explica.
   Com que `verifica.py` és a tots els passos, tots els hashos han canviat.
2. **Fitxers ignorats globalment (pendent).** Si l'ordinador té una llista global
   d'ignorats (`~/.config/git/ignore` o `core.excludesFile`) amb `.idea/`, al
   pas 01 `git status` no el mostra i l'enunciat no quadra. A l'assaig
   s'evita amb `XDG_CONFIG_HOME`; caldria comprovar-ho als ordinadors de
   l'aula (afegit com a idea a la prova manual?).
