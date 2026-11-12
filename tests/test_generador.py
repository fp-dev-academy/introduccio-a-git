"""Tests del generador (generador/build.py): determinisme i estructura."""

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

    def test_cap_commit_posterior_no_toca_les_llicencies(self) -> None:
        primer = git(self.repo, "rev-list", "--max-parents=0", "HEAD")
        canvis = git(self.repo, "log", "--format=", "--name-only",
                     f"{primer}..HEAD", "--", "LICENSE", "LICENSE-docs")
        self.assertEqual(canvis, "")


if __name__ == "__main__":
    unittest.main()
