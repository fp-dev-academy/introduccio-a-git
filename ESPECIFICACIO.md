# Especificació — git-rocinante

## 1. Marc

| Paràmetre | Valor |
|---|---|
| Alumnat | 2n CFGS DAM. Coneixen Git conceptualment, no l'utilitzen habitualment |
| Durada | **2 hores** (sessió única) |
| Plataforma | Windows 11, Git for Windows, Git Bash al terminal integrat de PyCharm, Python 3.15 |
| Remot | Compte propi a gitlab.com amb claus SSH ja configurades |
| Model | Fork del repositori guia `git-rocinante` → clon per SSH → un tag per pas |

### Repositoris

| Repositori | Contingut | Visibilitat |
|---|---|---|
| `fp-dev-academy/introduccio-a-git` | Font: generador, verificador, solucions, tests i aquesta especificació | Privat durant el desenvolupament; públic quan estigui acabat i comprovat |
| `fp-dev-academy/git-rocinante` | Guia **generada**. L'alumnat en fa fork. Mai s'edita a mà | Públic |

Com que el font serà públic, les solucions i les respostes esperades seran consultables.
S'accepta: `verifica.py` és una eina d'autoavaluació formativa, no d'avaluació qualificadora.

### Flux de cada pas (és al `README.md`)

```bash
git switch -c treball/pas-NN pas-NN   # parteix de l'estat inicial del pas
cat REPTE.md                          # llegeix l'enunciat
# ... resol el repte ...
python verifica.py NN                 # comprova el resultat
```

El treball de cada pas queda a la seva branca `treball/pas-NN`. Cap pas no depèn del que
l'alumne hagi fet en el pas anterior: l'estat inicial de cada pas el construeix el generador.

## 2. Planificació temporal

| Pas | Títol | Temps | Ajuda | Bloc |
|---|---|---|---|---|
| 00 | Embarcament | 10' (o abans de classe) | Comandes completes | Preparació |
| 01 | Primera entrada al diari | 10' | Comandes completes | Fonaments |
| 02 | La caixa negra | 15' | Comandes completes | Història |
| 03 | Esborrar les proves | 15' | Comandes + objectiu | Desfer |
| 04 | Nova secció de tripulació | 10' | Comandes + objectiu | Branques |
| 05 | Conflicte a la sala de màquines | 20' | Només l'objectiu i les comandes que caldran | Branques |
| 06 | Algú ha trencat la navegació | 15' | Només l'objectiu | Eines |
| 07 | Informe a la flota | 15' | Només l'objectiu | Remot |
| | **Total** | **110'** + 10' de marge | | |

**Risc:** el temps és ajustat. El pas 00 s'ha d'encarregar com a **feina prèvia** (fork, clon
i `ssh -T git@gitlab.com`). Si el grup va endarrerit, el pas 06 passa a ser opcional i el pas 07 es fa igualment.

Els passos 08 a 11 (secció 5) són d'**ampliació autònoma**, fora de la sessió.

## 3. Repositori generat

### Tripulació (autors dels commits)

| Nom | Correu | Rol als commits |
|---|---|---|
| James Holden | holden@rocinante.mcrn | Funcionalitats generals, missatges una mica idealistes |
| Naomi Nagata | naomi@rocinante.mcrn | Enginyeria, refactors cuidats |
| Amos Burton | amos@rocinante.mcrn | Canvis directes, missatges curts |
| Alex Kamal | alex@rocinante.mcrn | Navegació |

### Aplicació

```
rocinante/
  __init__.py
  __main__.py          # CLI: python -m rocinante [tripulacio|consum|trajecte]
  tripulacio.py        # llista i alta de tripulants
  combustible.py       # calcula_consum(...)
  navegacio.py         # temps_trajecte(...)
tests/
  test_combustible.py
  test_navegacio.py
README.md  REPTE.md  PISTES.md  verifica.py  .gitattributes
LICENSE  LICENSE-docs                 # des del primer commit
.gitignore                            # a main a partir del commit posterior a pas-01
```

Estat inicial de l'aplicació (a `pas-00`):

- `TRIPULACIO`: llista literal de diccionaris `{"nom": ..., "rol": ...}` amb els quatre
  tripulants, perquè l'alumne s'hi pugui afegir copiant una línia i perquè `verifica.py` la
  pugui llegir amb `ast.literal_eval` sense executar el codi de l'alumne.
- `calcula_consum(massa_t, acceleracio_g)` → `massa_t * acceleracio_g * 0.8`.
- `temps_trajecte(distancia_km, velocitat_kms)` → hores: `distancia_km / velocitat_kms / 3600`.
- Els tests fan servir `unittest` i s'executen amb `python tests/test_x.py` (codi 0 o 1).

`LICENSE` (MIT, per al codi) i `LICENSE-docs` (CC BY-SA 4.0, per als textos `README.md`,
`REPTE.md` i `PISTES.md`) segueixen la decisió 0006 del grup. Formen part del primer commit, i
cap commit posterior no els toca.

### Branques i tags del repositori publicat

- `main`: història completa fins a l'últim pas.
- Tags `pas-00` … `pas-07` sobre `main`, i `v1.0` (vegeu el pas 06).
- `tripulacio/naomi-eficiencia` i `tripulacio/amos-potencia`, que surten de `pas-05` (vegeu el pas 05).

### Coherència de `main` entre passos

Cada tag `pas-NN` és un estat sa **excepte el problema del seu propi pas**. Després del tag
`pas-NN` i abans de construir l'estat inicial del pas següent, el generador fa que un tripulant
arregli a `main` el problema del pas, amb commits propis i diferents de la solució de
referència:

| Després de | Commit de la tripulació a `main` |
|---|---|
| `pas-01` | Amos afegeix el `.gitignore` |
| `pas-02` | Alex recupera `rumb_emergencia()` |
| `pas-03` | Naomi fa el `revert` de l'"AMOS WAS HERE". El commit `asdf` es queda a la història: ja està compartit i no es reescriu |
| `pas-05` | Naomi fa el merge de les dues branques `tripulacio/*` i resol el conflicte. Aquest commit és `v1.0` |
| `pas-06` | Alex fa el `revert` del commit culpable |

Així, `python -m rocinante` i els tests que no són objecte del pas funcionen a cada tag, i el pas
11 (CI) es pot fer sobre un `main` en verd.

## 3 bis. Regles comunes de `verifica.py`

### Fitxers de respostes (`respostes/pas-NN.txt`)

- Es llegeixen amb la codificació `utf-8-sig` (accepta el BOM que pot afegir el Bloc de notes)
  i s'accepten salts de línia LF i CRLF.
- Una parella `clau=valor` per línia. S'ignoren les línies buides i les que comencen amb `#`,
  i també els espais al voltant de la clau, del `=` i del valor.
- Abans de calcular el SHA-256, el valor es normalitza:
  - **noms**: es passen a minúscules i els espais interns es redueixen a un de sol. S'accepta
    el nom complet o només el nom de pila (`Amos Burton`, `amos`).
  - **hashos**: es passen a minúscules, i s'accepta qualsevol prefix de 7 a 40 caràcters
    hexadecimals. Es comparen els 7 primers.
- Si falta una clau, el criteri falla amb una pista que en diu el nom. Si el format és
  incorrecte, la pista mostra un exemple de línia vàlida.

### Missatges de commit

«Format Conventional Commits» vol dir que la primera línia compleix
`^(feat|fix|docs|refactor|test|chore)(\([a-z0-9-]+\))?!?: \S.*$` i té 72 caràcters com a
màxim. Els missatges que genera git (`Merge branch ...`, `Revert "..."`) no es comproven.

### Abast dels criteris

Quan un criteri parla de «commits nous», «commits de merge» o «la història de `HEAD`», es
refereix al rang `pas-NN..HEAD`, excepte si s'indica una altra cosa.

### Punt de partida

Si `pas-NN` no és avantpassat de `HEAD` (l'alumne no és a la seva branca `treball/pas-NN`
o n'ha reescrit l'inici), el verificador mostra només el criteri «la branca parteix de
`pas-NN`», amb la pista `git switch -c treball/pas-NN pas-NN`. Els altres criteris no tindrien
sentit. Aquesta comprovació no s'aplica al pas 00, que es fa des de `main`. Al pas 03 es
comprova `pas-03~1`, perquè l'`--amend` substitueix precisament el commit `pas-03`.

### Errors de l'entorn

Si `git` no és al PATH, el directori no és un repositori o el pas no existeix en aquella
versió de `verifica.py`, l'script ho diu en una sola línia i acaba amb el codi 2, sense traça
de Python.

## 4. Passos de la sessió

### Pas 00 — Embarcament

- **Narrativa:** l'alumne s'enrola a la Rocinante i ha de registrar-se a bord.
- **Aprenentatge:** fork, `clone` per SSH, `remote`, configuració.
- **Repte:**
  1. Fer el fork de `git-rocinante` a GitLab (web).
  2. `git clone git@gitlab.com:<usuari>/git-rocinante.git`
  3. `git remote add upstream <url SSH del repositori guia>`
  4. `git config --global user.name`, `user.email` i `core.editor notepad`
  5. `python verifica.py 00` (des de `main`)
- **Criteris de `verifica.py 00`:**
  - `user.name` i `user.email` definits; `user.email` amb format de correu.
  - `core.editor` definit.
  - `origin` existeix, té URL SSH (`git@`) i no apunta al repositori guia.
  - `upstream` existeix i apunta al repositori guia.
  - Hi ha els tags `pas-00` … `pas-07` i `v1.0` en local.
  - `python` respon i té la versió 3.12 o superior (el `REPTE.md` explica l'alternativa `py`
    si `python` no es troba a Git Bash).

### Pas 01 — Primera entrada al diari

- **Narrativa:** cal registrar l'alumne com a nou tripulant i evitar que la brossa de PyCharm entri al diari.
- **Aprenentatge:** les tres zones, `status`, `add`, `commit`, `.gitignore`.
- **Estat inicial (`pas-01`):** sense `.gitignore`. Els fitxers a ignorar no poden venir del
  repositori, així que els genera l'alumne: el `REPTE.md` demana executar `python -m rocinante`
  (que crea `__pycache__/`) i obrir el projecte a PyCharm (que crea `.idea/`), i després
  observar-los a `git status` abans de crear el `.gitignore`.
- **Repte:**
  1. Afegir-se a `rocinante/tripulacio.py` (llista `TRIPULACIO`) → commit.
  2. Crear `.gitignore` amb `__pycache__/`, `*.pyc` i `.idea/` → commit.
- **Criteris:**
  - Almenys 2 commits nous sobre `pas-01`.
  - `TRIPULACIO` té almenys un element més que a `pas-01`.
  - `.gitignore` versionat, que conté `__pycache__` i `.idea`.
  - Cap fitxer sota `__pycache__/` ni `.idea/` versionat (`git ls-files`).
  - Directori de treball net (`git status --porcelain` buit; per defecte, aquesta ordre ja no
    mostra els fitxers ignorats).
  - Els missatges dels commits nous estan en format Conventional Commits (secció 3 bis).

### Pas 02 — La caixa negra

- **Narrativa:** algú ha esborrat la funció de rumb d'emergència. La caixa negra (la història) ho recorda tot.
- **Aprenentatge:** `log --oneline --graph`, `show`, `diff`, `switch --detach` a un commit
  antic, detached HEAD, tornar amb `switch -`, `restore --source`.
- **Estat inicial (`pas-02`):** la funció `rumb_emergencia()` de `navegacio.py` es va afegir
  en un commit d'Alex i es va esborrar 3 commits després en un commit d'Amos (`refactor: neteja codi mort`).
- **Repte:**
  1. Respondre a `respostes/pas-02.txt` (format `clau=valor`):
     - `autor_esborrat=` nom de l'autor del commit que va esborrar la funció.
     - `hash_afegit=` hash curt (7 caràcters) del commit que la va afegir.
  2. Visitar aquell commit en detached HEAD, comprovar que la funció hi és i tornar.
  3. Recuperar la funció: `git restore --source=<hash> rocinante/navegacio.py`, revisar el `diff` i fer commit.
  4. Fer commit de `respostes/pas-02.txt` (pot ser el mateix commit o un altre).
- **Restricció del generador:** entre el commit que afegeix `rumb_emergencia()` i `pas-02`,
  `navegacio.py` només canvia al commit que l'esborra. Així el `restore --source` no desfà
  cap altre canvi.
- **Criteris:**
  - `respostes/pas-02.txt` versionat; el SHA-256 de cada valor normalitzat coincideix amb el
    de la resposta esperada (secció 3 bis).
  - `rumb_emergencia` existeix a `navegacio.py` a `HEAD`.
  - `pas-02` és avantpassat de `HEAD` i hi ha almenys un commit nou (no s'ha reescrit la història).
  - `HEAD` no està en detached HEAD.
- **Nota:** el pas 02 ha de quedar resoluble també amb
  `git log -S rumb_emergencia -- rocinante/navegacio.py`. Les `PISTES.md` ho mencionen com a
  pista final. Cal la ruta: `REPTE.md`, `PISTES.md` i `verifica.py` també mencionen la funció, i
  sense la ruta la cerca en trobaria el commit.

### Pas 03 — Esborrar les proves

- **Narrativa:** Amos ha fet un commit amb el missatge `asdf` i, abans, un commit que fa que
  la CLI imprimeixi "AMOS WAS HERE" a cada execució.
- **Aprenentatge:** `commit --amend` (només en local, no compartit), `revert` (per al que sí
  que s'ha compartit), diferència amb `reset`, `restore` i `restore --staged`.
- **Estat inicial (`pas-03`):** el commit apuntat per `pas-03` té el missatge `asdf` (canvi
  vàlid a `tripulacio.py`). Uns quants commits abans hi ha `feat: millora la sortida de la CLI`,
  que introdueix el `print("AMOS WAS HERE")` a `__main__.py`.
  - Entre aquest commit i `pas-03`, cap commit no toca `__main__.py`, perquè el `revert` no
    tingui conflictes.
- **Ficció didàctica:** el commit `asdf` ja és a `main` del fork, és a dir, tècnicament ja
  està compartit. El `REPTE.md` demana a l'alumne que faci com si Amos encara no l'hagués pujat
  i remarca que, a la vida real, un commit pujat no es modifica amb `--amend`. Per això la
  tripulació, a `main`, no el toca (secció 3).
- **Repte** (l'ordre dels apartats 2 i 3 és obligatori: `--amend` només modifica l'últim commit):
  1. Practicar (sense verificació): modificar un fitxer, afegir-lo al staging, treure'l amb
     `restore --staged` i descartar el canvi amb `restore`.
  2. Corregir el missatge `asdf` amb `--amend` (Conventional Commits).
  3. Desfer el commit de l'"AMOS WAS HERE" amb `revert` (el missatge per defecte del revert és vàlid).
- **Pista específica:** si `HEAD` és el revert però `HEAD~1` encara té el missatge `asdf`,
  `verifica.py` indica que l'ordre ha estat el contrari i explica com tornar a començar
  (`git switch -C treball/pas-03 pas-03`).
- **Criteris:**
  - `HEAD` és un commit de revert del commit de l'"AMOS WAS HERE" (missatge amb `This reverts commit <hash>`).
  - `HEAD~1` té com a pare `pas-03~1`, el mateix arbre que `pas-03` i un missatge diferent de
    `asdf` en format Conventional Commits.
  - El commit de l'"AMOS WAS HERE" continua sent avantpassat de `HEAD` (no s'ha reescrit la història compartida).
  - `__main__.py` a `HEAD` no conté `AMOS WAS HERE`.
  - Directori de treball i staging nets.

### Pas 04 — Nova secció de tripulació

- **Narrativa:** cal poder llistar la tripulació per rol sense trencar la versió estable.
- **Aprenentatge:** `branch`, `switch -c`, treballar en una branca, merge fast-forward.
- **Repte:**
  1. Des de `treball/pas-04`, crear `feature/rols`.
  2. Afegir `per_rol(rol)` a `tripulacio.py` (almenys 1 commit).
  3. Tornar a `treball/pas-04` i fer el merge de `feature/rols` (fast-forward).
- **Criteris:**
  - La branca `feature/rols` existeix i té almenys 1 commit sobre `pas-04`.
  - `treball/pas-04` apunta al mateix commit que `feature/rols` (fast-forward, sense commit de merge).
  - `per_rol` existeix a `tripulacio.py`.

### Pas 05 — Conflicte a la sala de màquines

- **Narrativa:** Naomi i Amos han modificat alhora el càlcul de consum. Tots dos tenen raó, però a la seva manera.
- **Aprenentatge:** branques remotes (`origin/tripulacio/...`), merge de tres vies, conflicte,
  marcadors, resolució, commit de merge.
- **Estat inicial (`pas-05`):**
  ```python
  def calcula_consum(massa_t, acceleracio_g):
      return massa_t * acceleracio_g * 0.8
  ```
  - `tripulacio/naomi-eficiencia` (1 commit de Naomi): afegeix el paràmetre `eficiencia=1.0` i
    divideix el resultat per `eficiencia`.
  - `tripulacio/amos-potencia` (1 commit d'Amos): afegeix el paràmetre `mode_combat=False` i
    multiplica per 1.5 si és `True`.
  - Totes dues modifiquen la signatura i la línia del `return`, cosa que provoca el conflicte.
    No hi ha cap altra línia en conflicte, ni en aquest fitxer ni en cap altre.
  - `tests/test_combustible.py` ja és a `pas-05` amb la versió final: comprova els dos
    comportaments i també la combinació, amb arguments per nom. **A `pas-05` i a cadascuna de
    les branques `tripulacio/*` el test falla a propòsit**: fer-lo passar és l'objectiu del
    pas, i el `REPTE.md` ho diu. Cap de les dues branques no modifica el test.
- **Repte:** integrar les dues branques a `treball/pas-05` (primer la de Naomi, que és fast-forward
  o merge simple, i després la d'Amos, que genera el conflicte) i resoldre el conflicte de manera que el test passi.
- **Criteris:**
  - Les puntes de totes dues branques són avantpassades de `HEAD`.
  - Hi ha almenys un commit de merge amb 2 pares al rang `pas-05..HEAD`.
  - `HEAD` no és `v1.0` ni la té com a avantpassat (no s'ha copiat el merge de la tripulació).
  - Cap fitxer versionat que hagi canviat respecte de `pas-05` conté `<<<<<<<`, `=======` o
    `>>>>>>>` a principi de línia. (Els fitxers que no han canviat no poden tenir marcadors de
    l'alumne, i el `REPTE.md` en mostra uns d'exemple.)
  - `python tests/test_combustible.py` acaba amb codi 0.
- **Solució de referència:**
  ```python
  def calcula_consum(massa_t, acceleracio_g, eficiencia=1.0, mode_combat=False):
      factor = 1.5 if mode_combat else 1.0
      return massa_t * acceleracio_g * 0.8 * factor / eficiencia
  ```

### Pas 06 — Algú ha trencat la navegació

- **Narrativa:** mentre resolies el conflicte, la tripulació ha fet 16 commits. Ara
  `temps_trajecte()` dona temps 10 vegades massa grans. Alex jura que no ha estat ell.
- **Aprenentatge:** `bisect` manual i `git bisect run`, `bisect reset`, `revert` d'un commit antic.
- **Estat inicial:**
  - El tag `v1.0` apunta al commit de merge amb què Naomi integra les dues branques
    `tripulacio/*` a `main` (secció 3). És una versió bona: tots els tests hi passen.
  - Entre `v1.0` i `pas-06` hi ha 16 commits de farciment lineals (autors variats, canvis
    plausibles), sense merges, perquè `bisect` sigui fàcil de seguir, i després el commit del
    repte (`REPTE.md`, `PISTES.md` i `verifica.py`), que és el que apunta `pas-06`. En total, el
    rang `v1.0..pas-06` té 17 commits.
  - El commit 9 (`refactor: unifica conversions d'unitats`) canvia `/ 3600` per `/ 360` a `navegacio.py`.
  - Cap commit posterior no toca la línia afectada (el revert s'ha de poder fer sense conflictes).
  - `tests/test_navegacio.py` existeix i és idèntic a tot el rang `v1.0..pas-06`. Passa als
    commits 1–8 i falla als commits 9–17. **A `pas-06` falla a propòsit.**
  - `tests/test_combustible.py` passa a tot el rang (el merge de la tripulació ja hi és).
- **Repte:**
  1. `git bisect start pas-06 v1.0` i `git bisect run python tests/test_navegacio.py`
     (o `py` en lloc de `python`, vegeu el pas 00).
  2. Escriure el hash curt del commit culpable a `respostes/pas-06.txt` (`culpable=<hash>`).
  3. `git bisect reset`, `revert` del commit culpable i commit de la resposta.
- **Criteris:**
  - El SHA-256 de `culpable` coincideix amb el de la resposta esperada.
  - Hi ha un commit de revert del commit culpable al rang `pas-06..HEAD`.
  - `python tests/test_navegacio.py` acaba amb codi 0 a `HEAD`.
  - No hi ha cap bisect en curs (no existeix `.git/BISECT_LOG`).

### Pas 07 — Informe a la flota

- **Narrativa:** cal enviar l'informe de la missió a la flota perquè el revisi un company.
- **Aprenentatge:** `push`, `push -u`, branques de seguiment, merge requests a GitLab.
- **Repte:**
  1. Pujar a `origin` totes les branques `treball/pas-*`.
  2. Obrir una merge request **dins del propi fork** de `treball/pas-05` cap a `main`.
     Atenció: per defecte GitLab proposa el repositori guia com a destinació, i cal canviar-la.
  3. Demanar a un company que la revisi i hi deixi un comentari.
- **Criteris de `verifica.py 07`:**
  - Per a cada branca local `treball/pas-*`, existeix la remota a `origin` i apunta al mateix commit (`git ls-remote`).
    El pas 06 pot faltar si s'ha fet opcional (secció 2): el criteri només exigeix les branques que existeixen en local.
  - `treball/pas-05` té branca upstream configurada.
- **Xarxa:** és l'únic pas que fa servir la xarxa. Si `git ls-remote origin` falla, el criteri
  falla amb la pista `ssh -T git@gitlab.com`, i no amb una traça de Python.
- **Limitació:** la merge request i la revisió no es poden comprovar en local. Les revisa el docent a GitLab.

## 5. Ampliació autònoma (fase 2, fora de la sessió)

| Pas | Títol | Contingut |
|---|---|---|
| 08 | Història neta | `rebase` sobre `main`, regla d'or de no fer rebase del que ja és compartit |
| 09 | Peces de recanvi | `stash` i `cherry-pick` d'un fix cap a una branca `release/1.x` |
| 10 | Viatge sense retorn? | `reset --soft/--mixed/--hard` i recuperació amb `reflog` d'una branca esborrada |
| 11 | Pilot automàtic | `.gitlab-ci.yml` que executa `tests/` a cada push |

Cal especificar-los amb el mateix nivell de detall abans d'implementar-los.

## 6. Publicació i manteniment

1. El docent executa `python generador/build.py --out <dir>`, revisa el resultat i fa push a `git-rocinante` (públic) amb `--force --all` i `--force --tags`.
   El push forçat només és admissible **abans** que l'alumnat faci el fork.
2. El repositori guia no té `.gitlab-ci.yml` fins al pas 11, que l'afegeix l'alumne. La CI del
   repositori font (`introduccio-a-git`) executa `tests/` en una imatge amb `git` (la imatge
   `python:<versió>-slim` del component `python-tests` del grup no en porta).
3. **Un cop l'alumnat ha fet el fork, el repositori queda congelat.** Si cal una correcció,
   s'afegeix un tag nou (`pas-NN-b`) i no es mou cap tag existent.

## 7. Hipòtesis pendents de validar

- L'alumnat té Git for Windows amb Git Bash i el pot fer servir com a terminal de PyCharm.
- El portàtil té `python` al PATH dins de Git Bash (a Windows de vegades només hi ha `py`).
  El pas 00 ho ha de comprovar, i el `README.md` ha d'indicar l'alternativa.
- `notepad` com a editor funciona des de Git Bash per a `commit` sense `-m` i per al missatge del merge.
- GitLab copia tots els tags i les branques `tripulacio/*` en fer el fork (el pas 00 ho comprova).
- Els identificadors en català de l'aplicació són una excepció didàctica a la convenció del
  grup (identificadors en anglès). Cal recollir-ho en una decisió de `comu/decisions/`.
