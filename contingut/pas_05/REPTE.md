# Pas 05 · Conflicte a la sala de màquines

La Naomi i l'Amos han millorat alhora el càlcul del consum, cadascun a la
seva branca:

- la **Naomi** hi ha afegit l'eficiència del motor (`eficiencia`);
- l'**Amos** hi ha afegit el mode de combat (`mode_combat`), «perquè quan
  disparen no és moment d'estalviar».

Tots dos tenen raó, però han tocat les mateixes línies. Al capità Holden li
toca integrar-ho, i avui el capità ets tu.

El capità ja ha escrit els tests que han de passar quan tot estigui
integrat. Ara mateix fallen:

```bash
git switch -c treball/pas-05 pas-05
python tests/test_combustible.py
```

## Què aprendràs

- Què són les **branques remotes** (`origin/...`).
- El **merge de tres vies** i quan provoca un **conflicte**.
- Llegir els marcadors de conflicte, resoldre'l i acabar el merge.

## L'objectiu

Integra les dues branques de la tripulació a `treball/pas-05`, **primer la
de la Naomi i després la de l'Amos**, de manera que
`python tests/test_combustible.py` passi.

## El que necessitaràs

### Branques remotes

Les branques de la tripulació són al teu fork, a GitHub. Les tens com a
**branques remotes**: còpies de només lectura de com estaven a `origin`
l'última vegada que hi vas parlar.

```bash
git branch -a
git log --oneline --graph --all -6
```

Pots fer merge directament d'una branca remota: `git merge origin/<branca>`.
Si no veus les branques `origin/tripulacio/*`, el teu fork només té `main`:
fes `git fetch upstream` i usa `upstream/<branca>`.

### El merge de tres vies

Quan les dues branques han avançat per separat, Git no pot fer
fast-forward. Compara cada branca amb el seu **avantpassat comú** i combina
els canvis de totes dues. Si totes dues han canviat **les mateixes línies**,
no sap quina versió triar: és un **conflicte**, i t'ho deixa resoldre a tu.

### Llegir un conflicte

Git escriu les dues versions al fitxer, entre marcadors:

```
<<<<<<< HEAD
la teva versió (la branca on ets)
=======
la versió de la branca que integres
>>>>>>> origin/tripulacio/amos-potencia
```

En aquest pas hi haurà **dos blocs** en conflicte dins de la mateixa
funció. Has de deixar el fitxer com hauria de quedar: amb els dos
paràmetres i els dos càlculs, i **sense cap marcador**.

### Les ordres

| Ordre | Per a què |
|---|---|
| `git merge <branca>` | integra una branca |
| `git status` | mostra els fitxers en conflicte (`both modified`) |
| `git diff` | mostra el conflicte |
| `git add <fitxer>` | marca el conflicte com a resolt |
| `git commit` | acaba el merge (el missatge per defecte és vàlid) |
| `git merge --abort` | cancel·la el merge i torna a l'estat d'abans |

Quan hagis acabat:

```bash
python tests/test_combustible.py
git log --oneline --graph -5
python verifica.py 05
```

> A `main`, la Naomi també ha resolt aquest conflicte (és la versió
> `v1.0`). No t'hi fixis: integrar `main` no val com a solució.
