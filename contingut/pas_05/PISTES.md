# Pistes · Pas 05

Llegeix només la pista que necessitis. Les últimes són les més concretes.

## No veig les branques de la tripulació

```bash
git branch -a
```

Si no surten `remotes/origin/tripulacio/...`, actualitza les branques
remotes:

```bash
git fetch origin
```

## Per on començo?

```bash
git merge origin/tripulacio/naomi-eficiencia
```

Ha de dir `Fast-forward`: `treball/pas-05` no s'havia mogut des que la
Naomi va crear la seva branca. Després, la de l'Amos:

```bash
git merge origin/tripulacio/amos-potencia
```

Aquesta vegada Git diu `CONFLICT`.

## M'he fet un embolic i vull tornar a començar

Si el merge encara no està acabat:

```bash
git merge --abort
```

Si ja l'havies acabat, torna a començar el pas:

```bash
git switch -C treball/pas-05 pas-05
```

## El merge ha obert el Bloc de notes

És el missatge del commit de merge (`Merge remote-tracking branch ...`).
És vàlid tal com està: desa i tanca.

## No entenc què he de deixar al fitxer

Obre `rocinante/combustible.py` i busca `<<<<<<<`. Al primer bloc hi ha
dues signatures de `calcula_consum`: cadascuna afegeix un paràmetre. La
bona en té **tots dos**. Al segon bloc, cada versió fa un càlcul: el bo
**combina** tots dos (multiplica pel factor de combat i divideix per
l'eficiència).

PyCharm també té una eina per resoldre conflictes: *Git → Resolve
Conflicts*.

## El test continua fallant

Executa'l i llegeix què diu:

```bash
python tests/test_combustible.py
```

- `TypeError: ... unexpected keyword argument` → a la signatura li falta
  un paràmetre.
- `AssertionError: 120.0 != 60.0` (o semblant) → el càlcul no combina els
  dos factors.

## Solució del primer bloc

```python
def calcula_consum(massa_t, acceleracio_g, eficiencia=1.0, mode_combat=False):
```

## Solució del segon bloc

```python
    factor = 1.5 if mode_combat else 1.0
    return massa_t * acceleracio_g * 0.8 * factor / eficiencia
```

Després: `git add rocinante/combustible.py` i `git commit`.
