# Pas 07 · Informe a la flota

La missió s'ha acabat. Tot el que has fet és al teu ordinador, i ningú més
no ho pot veure. Cal enviar l'informe a la flota: pujar la teva feina al
teu fork de GitHub i demanar que algú la revisi.

## Què aprendràs

- Pujar branques amb `git push`.
- Què és una **branca de seguiment** (*upstream*) i què fa `push -u`.
- Obrir una **pull request** a GitHub i fer-ne una revisió.

## L'objectiu

1. Puja a `origin` totes les teves branques `treball/pas-*`.
2. Obre una **pull request** dins del **teu fork**, de `treball/pas-05` cap
   a `main`.
3. Demana a algú que la revisi i hi deixi un comentari.

## El que necessitaràs

Comença des de la branca del pas, perquè `verifica.py 07` hi sigui:

```bash
git switch -c treball/pas-07 pas-07
```

### `git push` i les branques de seguiment

```bash
git push -u origin treball/pas-05
git branch -vv
```

La `-u` (`--set-upstream`) connecta la branca local amb la remota
`origin/treball/pas-05`. Des d'aleshores, des d'aquesta branca n'hi ha prou
amb `git push` i `git pull`, i `git status` et diu si vas per davant o per
darrere:

```
Your branch is up to date with 'origin/treball/pas-05'.
```

Per pujar totes les branques d'un cop, també amb seguiment:

```bash
git push -u origin --all
```

### La pull request

Una pull request (PR) és una proposta: «vull integrar aquesta branca en
aquella altra; reviseu-la». És on l'equip comenta el codi abans
d'acceptar-lo. A GitLab se'n diu *merge request*: és el mateix.

1. Obre el teu fork a GitHub: `https://github.com/<usuari>/git-rocinante`.
2. *Pull requests → New pull request*.
3. **base repository**: GitHub hi proposa `fp-dev-academy/git-rocinante`
   (el repositori de la flota). **Canvia-ho** per `<usuari>/git-rocinante`.
   La PR ha de quedar dins del teu fork.
4. **base**: `main`. **compare**: `treball/pas-05`.
5. Fes clic a *Create pull request*, posa-hi un títol, per exemple
   «Integra el càlcul de consum de la tripulació», i crea-la.

No la fusionis: només és per revisar-la.

### La revisió

Passa l'enllaç de la PR a algú altre: una persona que també faci els reptes,
o algú de l'equip. A la pestanya *Files changed*, pot fer clic al `+` d'una
línia i deixar-hi un comentari. Respon-li a la mateixa PR. Si fas els reptes sol,
fes-ho tu: comentar el codi abans d'integrar-lo també és un hàbit.

## Comprova-ho

```bash
python verifica.py 07
```

`verifica.py` comprova que les branques són a GitHub i que `treball/pas-05`
té seguiment. La pull request i la revisió no es poden comprovar des del
teu ordinador: comprova-les tu a GitHub. La PR ha de ser dins del teu fork,
de `treball/pas-05` cap a `main`, i ha de tenir almenys un comentari.

Bon viatge, tripulant.
