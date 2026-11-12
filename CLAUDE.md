# git-rocinante — Curs introductori de Git (DAM2)

Curs pràctic de Git per terminal per a alumnat de 2n de CFGS DAM. L'alumnat fa un fork d'un
repositori guia a GitLab i avança pas a pas: cada pas és un tag (`pas-NN`) amb un repte que
resol al terminal i que comprova `verifica.py`. Fil narratiu: el diari de bord de la
Rocinante (The Expanse).

**Font de veritat:** `ESPECIFICACIO.md`. Si cal canviar el comportament d'un pas, primer
s'actualitza l'especificació i després el codi. No s'inventen passos ni criteris que no hi
siguin.

## Dos repositoris

| Repositori | Visibilitat | Contingut |
|---|---|---|
| `fp-dev-academy/introduccio-a-git` (aquest) | Privat fins que estigui acabat i comprovat; després, públic | Generador, verificador, solucions, tests, especificació |
| `fp-dev-academy/git-rocinante` | Públic a gitlab.com | **Generat** pel generador. L'alumnat en fa fork. **Mai s'edita a mà.** |

## Estructura d'aquest repositori

```
generador/
  build.py              # punt d'entrada: python generador/build.py --out <dir>
  git_utils.py          # wrapper de git amb entorn aïllat i dates fixades
  passos/pas_NN.py      # una funció build(repo) per pas; afegeix commits, branques i tags
contingut/
  pas_NN/               # REPTE.md, PISTES.md i fitxers de codi propis de cada pas
verificador/
  verifica.py           # es copia al repositori generat (versió acumulativa fins al pas NN)
solucions/
  pas_NN_ok.sh          # resolució correcta (només per als tests)
  pas_NN_ko_*.sh        # resolucions incorrectes representatives
tests/
  test_generador.py     # determinisme, tags, branques, escenaris
  test_verificador.py   # per a cada pas: solució ok -> OK; solucions ko -> FALLA
```

## Regles del generador

- Python >= 3.12, **només biblioteca estàndard**. S'executa a la màquina del docent (macOS).
- **Determinisme obligatori:** dues execucions han de produir exactament els mateixos hashos.
  - `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME`, `GIT_COMMITTER_EMAIL` fixats
    per commit (personatges de la tripulació, vegeu l'especificació).
  - `GIT_AUTHOR_DATE` i `GIT_COMMITTER_DATE` fixats: base `2026-01-05T09:00:00+01:00` i +17 minuts per commit.
  - Configuració aïllada: `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` apuntant a un fitxer
    temporal buit, `commit.gpgsign=false`, `init.defaultBranch=main`, `core.autocrlf=false`.
  - Els tags anotats també tenen data i autor fixats.
- `.gitattributes` amb `* text=auto eol=lf` al primer commit (l'alumnat fa servir Windows 11).
- Tags anotats `pas-NN` amb el missatge `Pas NN - <títol>`. Tag addicional `v1.0` (vegeu el pas 06).
- Les branques d'escenari van sota `tripulacio/` (p. ex. `tripulacio/naomi-eficiencia`).
- **Les branques d'escenari i els commits de farciment no toquen mai `README.md`, `REPTE.md`,
  `PISTES.md` ni `verifica.py`.** Els conflictes només han d'aparèixer on l'especificació diu.
- `build.py` és idempotent: esborra i recrea el directori de sortida.
- El generador **no** fa push. La publicació la fa el docent manualment.

## Regles de `verifica.py`

- Python >= 3.12, només biblioteca estàndard. Plataforma objectiu: **Windows 11** (Python 3.15).
- Ús: `python verifica.py NN` des de l'arrel del repositori de l'alumne.
- Crida git amb `subprocess.run([...], capture_output=True, encoding="utf-8")` i
  `-c core.quotepath=off`. Mai `shell=True`. Rutes amb `pathlib`.
- **Només llegeix. No modifica mai el repositori.**
- Verifica l'estat del repositori, no les comandes que s'han executat.
- Una funció `verifica_pas_NN(repo) -> list[Resultat]` per pas, registrada en un diccionari.
- La sortida mostra cada criteri com a `[OK]` o `[FALLA]` amb una pista breu en català.
  Codi de sortida 0 si ho supera tot, 1 en cas contrari. Sense colors ANSI.
- Les respostes esperades (hashos, valors) **no apareixen en clar**: es comparen pel seu SHA-256.
- A cada tag `pas-NN`, `verifica.py` només conté els passos fins al NN.

## Codi de l'aplicació Rocinante

- Paquet `rocinante/`, CLI `python -m rocinante`. Només biblioteca estàndard. Menys de 300 línies en total.
- Identificadors en català i sense accents (`calcula_consum`, `tripulacio`), també a
  `verifica.py` i al generador: decisió 0007 de `comu`.
- Tests **sense pytest**: `tests/test_*.py` executables amb `python tests/test_x.py`, amb codi
  de sortida 0 o 1 (necessari per a `git bisect run` sense dependències).
- El codi és l'excusa, no el focus: ha de ser senzill i llegible.

## Convencions

- Commits: Conventional Commits en català, en imperatiu, de 72 caràcters com a màxim
  (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).
- Tot el contingut per a l'alumnat és en català.
- To: humor de l'univers The Expanse per a un públic adult, sense que tapi la claredat tècnica.
- Les instruccions dels `REPTE.md` estan pensades per a **Git Bash** al terminal integrat de PyCharm.
- Editor de Git per a l'alumnat: `notepad` (configurat al pas 00).

## Definició de feina acabada

Una tasca no està acabada fins que:

1. `python generador/build.py` executat dues vegades produeix hashos idèntics (`test_generador.py`).
2. Per a cada pas afectat, `solucions/pas_NN_ok.sh` passa `verifica.py` i cada `pas_NN_ko_*.sh` hi falla amb el missatge esperat.
3. Escenaris especials: el conflicte del pas 05 apareix exactament al fitxer i a la funció
   especificats, i `git bisect run` del pas 06 troba el commit esperat.
4. `python -m rocinante` funciona a cada tag.
