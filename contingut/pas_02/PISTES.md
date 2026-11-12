# Pistes · Pas 02

Llegeix només la pista que necessitis. L'última resol el pas.

## `git log` no s'acaba i no puc escriure

Git fa servir un paginador quan la sortida és llarga. Fes servir les
fletxes per moure't i prem `q` per sortir.

## No sé quin commit va esborrar la funció

Mira els commits que han tocat el fitxer i, de cadascun, què va canviar:

```bash
git log --oneline -- rocinante/navegacio.py
git show <hash>
```

Busca un `-def rumb_emergencia` (esborrada) o un `+def rumb_emergencia`
(afegida).

## Com sé qui va fer un commit?

```bash
git log -1 --format="%h %an %s" <hash>
```

## `verifica.py` diu que el format del fitxer de respostes no és correcte

Cada línia ha de ser `clau=valor`, sense cometes. Les línies buides i les
que comencen amb `#` s'ignoren. Per exemple:

```
autor_esborrat=Nom Cognom
hash_afegit=1a2b3c4
```

## M'he quedat en detached HEAD i no sé com tornar

```bash
git switch treball/pas-02
```

Si havies fet commits en detached HEAD, Git t'avisarà i et dirà com
recuperar-los.

## He restaurat el fitxer equivocat

Mentre no n'hagis fet commit, pots tornar-lo a l'estat de l'últim commit:

```bash
git restore <fitxer>
```

## Pista final: la cerca per contingut

Git pot buscar directament els commits que han afegit o esborrat un text
en un fitxer:

```bash
git log --oneline -S rumb_emergencia -- rocinante/navegacio.py
```

Sense `-- rocinante/navegacio.py`, també sortiria el commit que va afegir
aquest repte, perquè el `REPTE.md` també menciona la funció. Amb el fitxer,
surten dos commits: el de dalt és el més recent (el que la va esborrar) i el
de baix, el més antic (el que la va afegir).
