# Pas 06 · Algú ha trencat la navegació

Mentre resolies el conflicte de la sala de màquines, la tripulació no ha
parat: 16 commits més. Ara el càlcul del temps de trajecte dona resultats
**10 vegades massa grans**, i el test de navegació falla:

```bash
git switch -c treball/pas-06 pas-06
python tests/test_navegacio.py
python -m rocinante trajecte 36000 10
```

L'Alex jura que no ha estat ell. A la versió `v1.0` tot funcionava.

## Què aprendràs

- Trobar el commit que ha introduït un error amb una **cerca binària**:
  `git bisect`.
- Automatitzar-la amb `git bisect run`.
- Desfer un commit antic amb `git revert`, encara que en tingui d'altres al
  damunt.

## L'objectiu

1. Troba el **primer commit dolent** entre `v1.0` (bo) i `pas-06` (dolent).
2. Escriu-ne el hash curt a `respostes/pas-06.txt`:

   ```
   culpable=<hash>
   ```

3. Acaba el bisect, desfés el commit culpable amb un `revert` i fes commit
   de la resposta.
4. Comprova que el test de navegació torna a passar i executa
   `python verifica.py 06`.

## Com funciona `git bisect`

Revisar 17 commits un per un és lent. `git bisect` fa una **cerca binària**:
et porta al commit del mig, tu li dius si és bo o dolent, i descarta la
meitat de la llista. En quatre o cinc passos troba el culpable.

Les ordres que necessitaràs:

| Ordre | Per a què |
|---|---|
| `git bisect start <dolent> <bo>` | comença la cerca |
| `git bisect good` / `git bisect bad` | marca el commit actual |
| `git bisect run <ordre>` | ho fa sol: executa l'ordre a cada pas (codi 0 = bo, 1 = dolent) |
| `git bisect reset` | acaba i torna a la teva branca |

Durant el bisect estàs en **detached HEAD**: és normal. No facis commits
fins que hagis fet `git bisect reset`.

> Si fas servir `py` en lloc de `python`, escriu `py` també a
> `git bisect run`.
