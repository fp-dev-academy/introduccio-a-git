# Pas 04 · Nova secció de tripulació

El capità Holden vol poder consultar la tripulació per rol: qui pilota, qui
fa de mecànic... La Naomi hi està d'acord, amb una condició: «A la versió
estable no s'hi toca fins que funcioni».

Per això existeixen les **branques**: una línia de treball separada on
pots fer commits sense afectar la branca principal fins que decideixes
integrar-los.

## Què aprendràs

- Què és una branca: una etiqueta mòbil que apunta a un commit.
- Crear-ne una i canviar-hi: `git switch -c`, `git branch`.
- Integrar-la amb un **merge fast-forward**.

## El repte

```bash
git switch -c treball/pas-04 pas-04
```

Aquí `treball/pas-04` fa el paper de la versió estable.

### 1. Crea la branca de la funcionalitat

```bash
git switch -c feature/rols
git branch
```

L'asterisc indica la branca on ets. Ara mateix, totes dues branques
apunten al mateix commit:

```bash
git log --oneline --graph --all -3
```

### 2. Programa-hi la funcionalitat

Afegeix al final de `rocinante/tripulacio.py`:

```python


def per_rol(rol):
    """Retorna els tripulants que tenen el rol indicat."""
    return [tripulant for tripulant in TRIPULACIO if tripulant["rol"] == rol]
```

Prova-la i fes-ne commit **a la branca `feature/rols`**:

```bash
python -c "from rocinante.tripulacio import per_rol; print(per_rol('pilot'))"
git add rocinante/tripulacio.py
git commit -m "feat: llista la tripulació per rol"
git log --oneline --graph --all -3
```

Ara `feature/rols` va un commit per davant de `treball/pas-04`:

```
treball/pas-04
     |
     v
 o---o---A          (A = commit del pas 04)
          \
           B        <- feature/rols
```

Comprova que la versió estable no s'ha tocat:

```bash
git switch treball/pas-04
grep -c "def per_rol" rocinante/tripulacio.py     # 0: aquí encara no hi és
```

### 3. Integra la branca

Des de `treball/pas-04`:

```bash
git merge feature/rols
```

Git respon `Fast-forward`. Com que `treball/pas-04` no s'havia mogut des
que vas crear `feature/rols`, no cal combinar res: Git simplement **avança**
l'etiqueta `treball/pas-04` fins al commit B. No es crea cap commit nou.

```
 o---o---A---B      <- treball/pas-04, feature/rols
```

```bash
git log --oneline --graph --all -3
```

### 4. Comprova-ho

```bash
python verifica.py 04
```

Quan una branca ja s'ha integrat, es pot esborrar (`git branch -d
feature/rols`). Ara no ho facis: `verifica.py` la necessita.
