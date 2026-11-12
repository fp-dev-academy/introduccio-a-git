"""Tests del wrapper de git del generador (generador/git_utils.py)."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "generador"))

from git_utils import Repo  # noqa: E402


def git(repo: Path, *args: str) -> str:
    """Executa git fora del wrapper per inspeccionar el resultat."""
    resultat = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, encoding="utf-8", check=True,
    )
    return resultat.stdout.strip()


class TestRepo(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name) / "repo"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_inicia_repositori_amb_branca_main(self) -> None:
        with Repo.crea(self.dir) as repo:
            repo.escriu("a.txt", "a\n")
            repo.commit("chore: primer", "holden")
        self.assertEqual(git(self.dir, "branch", "--show-current"), "main")

    def test_autor_i_committer_son_el_tripulant(self) -> None:
        with Repo.crea(self.dir) as repo:
            repo.escriu("a.txt", "a\n")
            repo.commit("chore: primer", "naomi")
        self.assertEqual(
            git(self.dir, "log", "-1", "--format=%an <%ae>|%cn <%ce>"),
            "Naomi Nagata <naomi@rocinante.mcrn>|Naomi Nagata <naomi@rocinante.mcrn>",
        )

    def test_dates_fixades_amb_17_minuts_per_commit(self) -> None:
        with Repo.crea(self.dir) as repo:
            for i in range(3):
                repo.escriu("a.txt", f"{i}\n")
                repo.commit(f"chore: commit {i}", "amos")
        self.assertEqual(
            git(self.dir, "log", "--reverse", "--format=%aI|%cI").splitlines(),
            [
                "2026-01-05T09:00:00+01:00|2026-01-05T09:00:00+01:00",
                "2026-01-05T09:17:00+01:00|2026-01-05T09:17:00+01:00",
                "2026-01-05T09:34:00+01:00|2026-01-05T09:34:00+01:00",
            ],
        )

    def test_commit_retorna_el_hash(self) -> None:
        with Repo.crea(self.dir) as repo:
            repo.escriu("a.txt", "a\n")
            hash_commit = repo.commit("chore: primer", "alex")
        self.assertEqual(hash_commit, git(self.dir, "rev-parse", "HEAD"))

    def test_tag_anotat_amb_tagger_i_data_fixats(self) -> None:
        with Repo.crea(self.dir) as repo:
            repo.escriu("a.txt", "a\n")
            repo.commit("chore: primer", "holden")
            repo.escriu("a.txt", "b\n")
            repo.commit("chore: segon", "holden")
            repo.tag("pas-00", "Pas 00 - Embarcament", "naomi")
        self.assertEqual(git(self.dir, "cat-file", "-t", "pas-00"), "tag")
        self.assertEqual(
            git(self.dir, "tag", "-l", "pas-00",
                "--format=%(taggername) %(taggeremail)|%(taggerdate:iso-strict)|%(contents:subject)"),
            "Naomi Nagata <naomi@rocinante.mcrn>|2026-01-05T09:17:00+01:00|Pas 00 - Embarcament",
        )

    def test_escriu_amb_salts_de_linia_lf_i_crea_carpetes(self) -> None:
        with Repo.crea(self.dir) as repo:
            repo.escriu("rocinante/a.py", "x = 1\ny = 2\n")
        self.assertEqual((self.dir / "rocinante/a.py").read_bytes(), b"x = 1\ny = 2\n")

    def test_ignora_la_configuracio_de_git_de_l_usuari(self) -> None:
        config_usuari = Path(self._tmp.name) / "gitconfig-usuari"
        config_usuari.write_text(
            "[user]\n\tname = Intrus\n[commit]\n\tgpgsign = true\n"
            "[init]\n\tdefaultBranch = master\n",
            encoding="utf-8",
        )
        anterior = os.environ.get("GIT_CONFIG_GLOBAL")
        os.environ["GIT_CONFIG_GLOBAL"] = str(config_usuari)
        try:
            with Repo.crea(self.dir) as repo:
                repo.escriu("a.txt", "a\n")
                repo.commit("chore: primer", "holden")
        finally:
            if anterior is None:
                del os.environ["GIT_CONFIG_GLOBAL"]
            else:
                os.environ["GIT_CONFIG_GLOBAL"] = anterior
        self.assertEqual(git(self.dir, "branch", "--show-current"), "main")
        self.assertEqual(git(self.dir, "log", "-1", "--format=%an"), "James Holden")

    def test_mateixes_operacions_mateixos_hashos(self) -> None:
        hashos = []
        for nom in ("u", "dos"):
            with Repo.crea(Path(self._tmp.name) / nom) as repo:
                repo.escriu("a.txt", "a\n")
                repo.commit("chore: primer", "holden")
                repo.tag("pas-00", "Pas 00 - Embarcament", "holden")
            hashos.append(git(Path(self._tmp.name) / nom, "rev-parse", "pas-00", "HEAD"))
        self.assertEqual(hashos[0], hashos[1])

    def test_revert_amb_missatge_de_git_i_identitat_fixada(self) -> None:
        with Repo.crea(self.dir) as repo:
            repo.escriu("a.txt", "a\n")
            repo.commit("chore: primer", "holden")
            repo.escriu("a.txt", "b\n")
            desfet = repo.commit("feat: canvia a", "amos")
            hash_revert = repo.revert(desfet, "naomi")
        self.assertEqual(hash_revert, git(self.dir, "rev-parse", "HEAD"))
        self.assertEqual((self.dir / "a.txt").read_text(encoding="utf-8"), "a\n")
        self.assertEqual(
            git(self.dir, "log", "-1", "--format=%an|%cI|%s"),
            'Naomi Nagata|2026-01-05T09:34:00+01:00|Revert "feat: canvia a"',
        )
        self.assertIn(f"This reverts commit {desfet}.", git(self.dir, "log", "-1", "--format=%b"))

    def test_tripulant_desconegut_es_un_error(self) -> None:
        with Repo.crea(self.dir) as repo:
            repo.escriu("a.txt", "a\n")
            with self.assertRaises(KeyError):
                repo.commit("chore: primer", "miller")


if __name__ == "__main__":
    unittest.main()
