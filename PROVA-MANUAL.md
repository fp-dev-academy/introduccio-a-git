# Prova manual del repositori de pràctica

Llista de comprovació per provar `git-rocinante` com ho farà qui segueixi
els reptes, **abans de fer-lo públic** i cada vegada que se'n publiqui una
versió nova. Els tests automàtics (`tests/`) ja comproven la història, els
criteris i les solucions. Aquesta prova cobreix el que no poden comprovar:
GitHub, Windows, PyCharm, el Bloc de notes i si els textos s'entenen.

Anota-hi cada problema amb el pas, què esperaves i què ha passat. Si cal
corregir alguna cosa, vegeu [Si alguna cosa falla](#si-alguna-cosa-falla).

## Preparació

- [ ] Ordinador amb **Windows 11**, **Git for Windows** i **Python 3.15**.
- [ ] **PyCharm** amb Git Bash com a terminal (*Settings → Tools →
      Terminal → Shell path*: `C:\Program Files\Git\bin\bash.exe`).
- [ ] Un **compte de GitHub de prova** que no sigui membre de
      l'organització, amb una clau SSH d'aquest ordinador.
- [ ] Una configuració de git neta per al compte de prova. Si l'ordinador ja
      té una configuració global, apunta-la abans de començar: el pas 00 la
      sobreescriu.
- [ ] Temps: unes 2 hores. Cronometra cada pas i compara'l amb la taula de
      l'apartat 2 de `ESPECIFICACIO.md`.

## Pas 00 · Embarcament

- [ ] L'enllaç del `README.md` al `REPTE.md` del pas 00 s'obre a GitHub.
- [ ] El fork es fa sense problemes i GitHub hi proposa el teu usuari com a
      *Owner*.
- [ ] Desmarcant *Copy the `main` branch only*, el fork té **totes** les
      branques (`main`, `tripulacio/naomi-eficiencia`,
      `tripulacio/amos-potencia`) i els **9 tags** (`git branch -a` i
      `git tag` després de clonar). Comprovat amb l'API el 2026-11-19; falta
      fer-ho a la web.
- [ ] **Hipòtesi:** la casella *Copy the `main` branch only* surt marcada
      per defecte. Si és així, el `REPTE.md` ho avisa prou clar.
- [ ] Error provocat: fes un fork amb la casella marcada. `verifica.py 00`
      diu que falten els tags i la pista `git fetch upstream --tags` ho
      resol.
- [ ] **Hipòtesi:** a Git Bash, `python --version` respon. Si només respon
      `py`, l'explicació del `README.md` i del `REPTE.md` és suficient.
- [ ] `python verifica.py 00` acaba amb `8 de 8 criteris superats`.
- [ ] Error provocat: clona per HTTPS. La pista d'`origin fa servir SSH`
      s'entén i `git remote set-url` ho resol.

## Pas 01 · Primera entrada al diari

- [ ] `git status` mostra `rocinante/__pycache__/` i `.idea/` com a fitxers
      sense seguiment, després d'executar l'aplicació i obrir PyCharm.
- [ ] PyCharm no afegeix fitxers a Git per la seva banda (si ho pregunta,
      el `REPTE.md` diu que cal respondre que no).
- [ ] L'ordre `printf` per crear el `.gitignore` funciona a Git Bash.
- [ ] Error provocat: fes `git add .` abans de crear el `.gitignore`. La
      pista de `git rm -r --cached` ho resol.
- [ ] Error provocat: un missatge de commit sense format. La pista diu quin
      missatge és.

## Pas 02 · La caixa negra

- [ ] `git log` obre el paginador i `q` en surt (la pista ho explica).
- [ ] `notepad respostes/pas-02.txt` pregunta si es vol crear el fitxer i el
      crea.
- [ ] **Hipòtesi:** les respostes desades amb el Bloc de notes
      (codificació i salts de línia de Windows) es llegeixen bé.
- [ ] `git switch --detach` i `git switch -` es comporten com diu l'enunciat.
- [ ] La pista final (`git log -S ... -- rocinante/navegacio.py`) troba
      exactament dos commits.

## Pas 03 · Esborrar les proves

- [ ] **Hipòtesi:** `git revert` sense `-m` obre el Bloc de notes amb el
      missatge per defecte, i en desar i tancar el revert s'acaba.
- [ ] La taula «quina eina, i quan» i la nota sobre la ficció del commit no
      compartit s'entenen.
- [ ] Error provocat: fes el revert abans de l'`--amend`. La pista de l'ordre
      invertit ho explica i `git switch -C` permet tornar a començar.

## Pas 04 · Nova secció de tripulació

- [ ] La prova `python -c "from rocinante.tripulacio import per_rol; ..."`
      funciona a Git Bash (comprova les cometes).
- [ ] El merge diu `Fast-forward`.
- [ ] Error provocat: `git merge --no-ff`. La pista ho detecta.

## Pas 05 · Conflicte a la sala de màquines

- [ ] `git branch -a` mostra les dues branques `remotes/origin/tripulacio/*`.
- [ ] El primer merge és fast-forward i el segon té un conflicte a
      `rocinante/combustible.py`, amb **dos blocs**.
- [ ] **Hipòtesi:** el commit de merge obre el Bloc de notes amb el missatge
      per defecte i s'acaba en tancar-lo.
- [ ] L'eina de conflictes de PyCharm (*Git → Resolve Conflicts*) també
      permet resoldre'l.
- [ ] Error provocat: fes el commit amb marcadors. La pista hi apunta.
- [ ] Temps: 20 minuts o menys amb l'ajuda de les pistes.

## Pas 06 · Algú ha trencat la navegació

- [ ] **Hipòtesi:** `git bisect run python tests/test_navegacio.py` funciona a
      Git Bash i troba el culpable (si cal `py`, també funciona).
- [ ] Durant el bisect, PyCharm no es queixa del detached HEAD ni dels
      fitxers que canvien.
- [ ] El revert no té conflictes.

## Pas 07 · Informe a la flota

- [ ] `git push -u origin --all` puja les branques al fork.
- [ ] **Hipòtesi:** en crear la pull request, GitHub proposa el repositori de
      la flota com a *base repository*, i es pot canviar pel fork tal com
      explica l'enunciat.
- [ ] Una altra persona (o un segon compte) pot comentar una línia de la
      pull request.
- [ ] `python verifica.py 07` funciona per SSH. Error provocat: desconnecta la
      xarxa i comprova que la pista és d'SSH i no una traça de Python.

## Al final

- [ ] La [xuleta d'ordres](contingut/pas_00/ORDRES.md) ha servit per trobar
      les ordres als passos 05–07, que només donen l'objectiu.
- [ ] Cap text no fa referència a una classe ni a un grup concret.
- [ ] Desfés la configuració de prova: torna a posar la configuració global
      de git que tenies i esborra el fork del compte de prova.

## Si alguna cosa falla

1. Si el problema és de comportament, corregeix primer `ESPECIFICACIO.md`, i
   després el codi o el text a `contingut/`, `generador/` o `verificador/`.
2. `python3 -m unittest discover -s tests`: tot en verd.
3. Regenera el repositori de pràctica:
   `python3 generador/build.py --out sortida/git-rocinante`.
4. **Abans que ningú de fora n'hagi fet el fork**, publica'l de nou. Si
   `main` té una regla de protecció que impedeix el *force push*
   (*Settings → Rules → Rulesets*, o *Settings → Branches*), desactiva-la
   abans i torna-la a activar en acabar. Si no, el push de les branques es
   rebutja i el repositori pot quedar inconsistent.

   ```bash
   cd sortida/git-rocinante
   git remote add origin git@github.com:fp-dev-academy/git-rocinante.git
   git push --force --all origin
   git push --force --tags origin
   ```

   Un cop algú n'ha fet el fork, el repositori queda congelat: cap tag no es
   mou, i les correccions van en tags nous (`pas-NN-b`), tal com diu
   l'apartat 6 de `ESPECIFICACIO.md`.
5. Torna a fer la part de la prova afectada.
