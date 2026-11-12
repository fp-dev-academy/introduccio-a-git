# Pistes · Pas 06

Llegeix només la pista que necessitis. Les últimes són les més concretes.

## Com sé si un commit és bo o dolent?

Executa el test de navegació. Si acaba bé (`OK`), el commit és bo; si
falla, és dolent:

```bash
python tests/test_navegacio.py
```

## Per on començo?

```bash
git bisect start pas-06 v1.0
```

Primer el dolent i després el bo. Git et porta a un commit del mig.

## `git bisect` em fa marcar els commits a mà i és pesat

Deixa que ho faci sol:

```bash
git bisect run python tests/test_navegacio.py
```

## On és el hash del culpable?

Al final, `git bisect` escriu `<hash> is the first bad commit`, amb el
missatge i el diff del commit. Els 7 primers caràcters del hash són la
resposta.

## Ja tinc el culpable. I ara?

Primer, acaba el bisect. Si no, continues en detached HEAD:

```bash
git bisect reset
```

Després, desfés el culpable. El revert obrirà el Bloc de notes amb el
missatge per defecte: desa i tanca.

```bash
git revert <hash>
```

## `git revert` ha donat un conflicte

No n'hi hauria d'haver cap. Comprova que has escrit el hash del **primer**
commit dolent, i no el d'un altre. Per cancel·lar-ho: `git revert --abort`.

## M'he equivocat marcant un commit

Torna a començar el bisect:

```bash
git bisect reset
git bisect start pas-06 v1.0
```

## `verifica.py` diu que hi ha un bisect en curs

```bash
git bisect reset
```
