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
        self.assertEqual(git(self.repo, "cat-file", "-t", "pas-00"), "tag")
        self.assertEqual(
            git(self.repo, "tag", "-l", "pas-00", "--format=%(contents:subject)"),
            "Pas 00 - Embarcament",
        )

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
        for assumpte in git(self.repo, "log", "--format=%s").splitlines():
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

    def test_cap_commit_posterior_no_toca_les_llicencies(self) -> None:
        primer = git(self.repo, "rev-list", "--max-parents=0", "HEAD")
        canvis = git(self.repo, "log", "--format=", "--name-only",
                     f"{primer}..HEAD", "--", "LICENSE", "LICENSE-docs")
        self.assertEqual(canvis, "")


if __name__ == "__main__":
    unittest.main()
