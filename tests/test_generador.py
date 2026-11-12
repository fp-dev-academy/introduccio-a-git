"""Tests del generador (generador/build.py): determinisme i estructura."""

import ast
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ARREL = Path(__file__).resolve().parents[1]
BUILD = ARREL / "generador" / "build.py"

# Missatges que no segueixen Conventional Commits perquè són l'objecte d'un pas.
MISSATGES_INCORRECTES_A_PROPOSIT = {
    "asdf",  # pas 03: l'alumne el corregeix amb --amend
}

# Títols dels passos implementats (ESPECIFICACIO.md, secció 2).
TITOLS = {
    "pas-00": "Embarcament",
    "pas-01": "Primera entrada al diari",
    "pas-02": "La caixa negra",
    "pas-03": "Esborrar les proves",
}


def build(sortida: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(BUILD), "--out", str(sortida)],
        capture_output=True, encoding="utf-8", check=True,
    )


def git(repo: Path, *args: str) -> str:
    resultat = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, encoding="utf-8", check=True,
    )
    return resultat.stdout.strip()


def exporta(repo: Path, referencia: str, desti: Path) -> None:
    """Copia l'arbre d'una referència a un directori (sense .git)."""
    arxiu = subprocess.run(
        ["git", "-C", str(repo), "archive", "--format=tar", referencia],
        capture_output=True, check=True,
    ).stdout
    subprocess.run(["tar", "-x", "-C", str(desti)], input=arxiu, check=True)


def executa(directori: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Executa Python dins d'un directori, com ho faria l'alumne."""
    return subprocess.run(
        [sys.executable, *args], cwd=directori,
        capture_output=True, encoding="utf-8",
    )


def referencies(repo: Path) -> str:
    """Totes les branques i tags amb el hash de l'objecte al qual apunten."""
    return git(repo, "for-each-ref", "--format=%(refname) %(objectname)")


class TestBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.tmp = Path(cls._tmp.name)
        cls.repo = cls.tmp / "guia"
        build(cls.repo)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_dues_execucions_produeixen_els_mateixos_hashos(self) -> None:
        segon = self.tmp / "guia-2"
        build(segon)
        self.assertNotEqual(referencies(self.repo), "")
        self.assertEqual(referencies(self.repo), referencies(segon))

    def test_es_idempotent_i_esborra_el_contingut_anterior(self) -> None:
        sortida = self.tmp / "guia-3"
        build(sortida)
        (sortida / "brossa.txt").write_text("x", encoding="utf-8")
        build(sortida)
        self.assertFalse((sortida / "brossa.txt").exists())
        self.assertEqual(referencies(self.repo), referencies(sortida))

    def test_branca_principal_main_i_sense_remots(self) -> None:
        self.assertEqual(git(self.repo, "branch", "--show-current"), "main")
        self.assertEqual(git(self.repo, "remote"), "")

    def test_directori_de_treball_net(self) -> None:
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")

    def test_primer_commit_porta_gitattributes_i_llicencies(self) -> None:
        primer = git(self.repo, "rev-list", "--max-parents=0", "HEAD")
        fitxers = git(self.repo, "ls-tree", "--name-only", primer).splitlines()
        for fitxer in (".gitattributes", "LICENSE", "LICENSE-docs"):
            self.assertIn(fitxer, fitxers)
        self.assertEqual(
            git(self.repo, "show", f"{primer}:.gitattributes"), "* text=auto eol=lf"
        )

    def test_tags_anotats_amb_el_titol_del_pas(self) -> None:
        for tag, titol in TITOLS.items():
            with self.subTest(tag=tag):
                self.assertEqual(git(self.repo, "cat-file", "-t", tag), "tag")
                self.assertEqual(
                    git(self.repo, "tag", "-l", tag, "--format=%(contents:subject)"),
                    f"Pas {tag[4:]} - {titol}",
                )

    def test_verifica_de_cada_tag_nomes_te_els_passos_fins_al_seu(self) -> None:
        for tag in TITOLS:
            with self.subTest(tag=tag):
                arbre = ast.parse(git(self.repo, "show", f"{tag}:verifica.py"))
                passos = {n.name[-2:] for n in arbre.body
                          if isinstance(n, ast.FunctionDef) and n.name.startswith("verifica_pas_")}
                esperats = {t[4:] for t in TITOLS if t <= tag}
                self.assertEqual(passos, esperats)

    def test_pas_01_sense_gitignore_i_amos_l_afegeix_just_despres(self) -> None:
        fitxers = git(self.repo, "ls-tree", "-r", "--name-only", "pas-01").splitlines()
        self.assertNotIn(".gitignore", fitxers)
        commit = git(self.repo, "log", "--format=%H", "--diff-filter=A", "HEAD", "--", ".gitignore")
        self.assertEqual(git(self.repo, "log", "-1", "--format=%an", commit), "Amos Burton")
        self.assertEqual(git(self.repo, "rev-parse", f"{commit}~1"),
                         git(self.repo, "rev-parse", "pas-01^{commit}"))
        gitignore = git(self.repo, "show", "HEAD:.gitignore")
        for patro in ("__pycache__/", ".idea/"):
            self.assertIn(patro, gitignore.splitlines())

    def test_els_tags_coincideixen_amb_els_que_espera_verifica(self) -> None:
        tags = set(git(self.repo, "tag", "-l").splitlines())
        verifica = git(self.repo, "show", "HEAD:verifica.py")
        linia = next(l for l in verifica.splitlines() if l.startswith("TAGS_DEL_CURS"))
        esperats = set(ast.literal_eval(linia.split("=", 1)[1].strip()))
        self.assertTrue(esperats)
        self.assertEqual(tags, esperats)

    def test_fitxers_del_pas_00(self) -> None:
        fitxers = git(self.repo, "ls-tree", "-r", "--name-only", "pas-00").splitlines()
        for fitxer in ("README.md", "REPTE.md", "PISTES.md", "verifica.py",
                       "rocinante/__init__.py", "rocinante/__main__.py",
                       "rocinante/tripulacio.py", "rocinante/combustible.py",
                       "rocinante/navegacio.py",
                       "tests/test_combustible.py", "tests/test_navegacio.py"):
            self.assertIn(fitxer, fitxers)
        self.assertNotIn(".gitignore", fitxers)

    def test_tripulacio_inicial_llegible_sense_executar_codi(self) -> None:
        font = git(self.repo, "show", "pas-00:rocinante/tripulacio.py")
        assignacio = next(
            n for n in ast.parse(font).body
            if isinstance(n, ast.Assign) and n.targets[0].id == "TRIPULACIO"
        )
        tripulacio = ast.literal_eval(assignacio.value)
        self.assertEqual(
            [t["nom"] for t in tripulacio],
            ["James Holden", "Naomi Nagata", "Amos Burton", "Alex Kamal"],
        )

    def test_tots_els_commits_son_conventional_commits(self) -> None:
        patro = re.compile(r"^(feat|fix|docs|refactor|test|chore)(\([a-z0-9-]+\))?!?: \S.*$")
        for assumpte in git(self.repo, "log", "--no-merges", "--format=%s").splitlines():
            if assumpte.startswith('Revert "'):
                continue  # missatge que genera git (ESPECIFICACIO.md, 3 bis)
            if assumpte in MISSATGES_INCORRECTES_A_PROPOSIT:
                continue
            self.assertRegex(assumpte, patro)
            self.assertLessEqual(len(assumpte), 72)

    def test_aplicacio_i_tests_funcionen_a_cada_tag(self) -> None:
        tags = git(self.repo, "tag", "-l", "pas-*").splitlines()
        self.assertTrue(tags, "no hi ha cap tag pas-*")
        for tag in tags:
            with self.subTest(tag=tag), tempfile.TemporaryDirectory() as directori:
                exporta(self.repo, tag, Path(directori))
                for ordre in ([], ["tripulacio"], ["consum", "100", "1"],
                              ["trajecte", "36000", "10"]):
                    resultat = executa(Path(directori), "-m", "rocinante", *ordre)
                    self.assertEqual(resultat.returncode, 0, resultat.stderr)
                for test in sorted(Path(directori, "tests").glob("test_*.py")):
                    resultat = executa(Path(directori), str(test))
                    self.assertEqual(resultat.returncode, 0, f"{test.name}: {resultat.stderr}")

    def _commits_rumb_emergencia(self) -> list[str]:
        """Commits fins a pas-02 que afegeixen o esborren rumb_emergencia (antic → nou)."""
        return git(self.repo, "log", "--reverse", "--format=%H", "-S", "rumb_emergencia",
                   "pas-02", "--", "rocinante/navegacio.py").splitlines()

    def test_pas_02_alex_afegeix_el_rumb_i_amos_l_esborra_3_commits_despres(self) -> None:
        commits = self._commits_rumb_emergencia()
        self.assertEqual(len(commits), 2)
        afegit, esborrat = commits
        self.assertEqual(git(self.repo, "log", "-1", "--format=%an", afegit), "Alex Kamal")
        self.assertEqual(git(self.repo, "log", "-1", "--format=%an|%s", esborrat),
                         "Amos Burton|refactor: neteja codi mort")
        self.assertEqual(git(self.repo, "rev-list", "--count", f"{afegit}..{esborrat}"), "3")
        self.assertNotIn("def rumb_emergencia",
                         git(self.repo, "show", "pas-02:rocinante/navegacio.py"))

    def test_pas_02_navegacio_nomes_canvia_quan_s_esborra_la_funcio(self) -> None:
        afegit, esborrat = self._commits_rumb_emergencia()
        canvis = git(self.repo, "log", "--format=%H", f"{afegit}..pas-02",
                     "--", "rocinante/navegacio.py").splitlines()
        self.assertEqual(canvis, [esborrat])

    def test_pas_02_alex_recupera_el_rumb_just_despres_del_tag(self) -> None:
        commit = git(self.repo, "rev-list", "--reverse", "pas-02..HEAD").splitlines()[0]
        self.assertEqual(git(self.repo, "log", "-1", "--format=%an", commit), "Alex Kamal")
        self.assertIn("def rumb_emergencia",
                      git(self.repo, "show", f"{commit}:rocinante/navegacio.py"))

    def test_pas_02_les_respostes_no_surten_en_clar_a_verifica(self) -> None:
        afegit, _ = self._commits_rumb_emergencia()
        verifica = git(self.repo, "show", "pas-02:verifica.py").lower()
        self.assertNotIn(afegit[:7], verifica)
        self.assertNotIn("amos", verifica)

    def _commit_amos_was_here(self) -> str:
        commits = git(self.repo, "log", "--format=%H", "-S", "AMOS WAS HERE",
                      "pas-03", "--", "rocinante/__main__.py").splitlines()
        self.assertEqual(len(commits), 1)
        return commits[0]

    def test_pas_03_el_tag_apunta_al_commit_asdf_d_amos(self) -> None:
        self.assertEqual(git(self.repo, "log", "-1", "--format=%an|%s", "pas-03"),
                         "Amos Burton|asdf")
        self.assertEqual(git(self.repo, "diff", "--name-only", "pas-03~1", "pas-03"),
                         "rocinante/tripulacio.py")

    def test_pas_03_amos_was_here_uns_commits_abans_i_ningu_mes_toca_main(self) -> None:
        commit = self._commit_amos_was_here()
        self.assertEqual(git(self.repo, "log", "-1", "--format=%an|%s", commit),
                         "Amos Burton|feat: millora la sortida de la CLI")
        self.assertGreaterEqual(int(git(self.repo, "rev-list", "--count", f"{commit}..pas-03")), 3)
        self.assertEqual(git(self.repo, "log", "--format=%H", f"{commit}..pas-03",
                             "--", "rocinante/__main__.py"), "")

    def test_pas_03_naomi_fa_el_revert_just_despres_del_tag(self) -> None:
        commit = git(self.repo, "rev-list", "--reverse", "pas-03..HEAD").splitlines()[0]
        self.assertEqual(git(self.repo, "log", "-1", "--format=%an", commit), "Naomi Nagata")
        self.assertIn(f"This reverts commit {self._commit_amos_was_here()}.",
                      git(self.repo, "log", "-1", "--format=%b", commit))
        self.assertNotIn("AMOS WAS HERE", git(self.repo, "show", "HEAD:rocinante/__main__.py"))

    def test_cap_commit_posterior_no_toca_les_llicencies(self) -> None:
        primer = git(self.repo, "rev-list", "--max-parents=0", "HEAD")
        canvis = git(self.repo, "log", "--format=", "--name-only",
                     f"{primer}..HEAD", "--", "LICENSE", "LICENSE-docs")
        self.assertEqual(canvis, "")


if __name__ == "__main__":
    unittest.main()
