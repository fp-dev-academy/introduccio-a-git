"""Tests de verifica.py amb les solucions de referència (solucions/).

Per a cada pas NN:
- solucions/pas_NN_ok.sh ha de superar `python verifica.py NN`;
- cada solucions/pas_NN_ko_*.sh hi ha de fallar, i la sortida ha de tenir
  una línia [FALLA] amb el text de la capçalera `# espera: <text>`.

Cada solució s'executa amb bash dins d'un clon nou del repositori guia
generat, com si fos el fork de l'alumne, i amb una configuració de git
global pròpia i buida.
"""

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ARREL = Path(__file__).resolve().parents[1]
SOLUCIONS = ARREL / "solucions"


def entorn_alumne(directori: Path) -> dict[str, str]:
    """Entorn net: sense configuració de sistema ni de l'usuari real."""
    entorn = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    config = directori / "gitconfig"
    config.touch()
    entorn.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=str(config),
                  HOME=str(directori))
    return entorn


def espera(script: Path) -> str:
    coincidencia = re.search(r"^# espera: (.+)$", script.read_text(encoding="utf-8"), re.M)
    if coincidencia is None:
        raise AssertionError(f"{script.name} no té la capçalera '# espera: <text>'")
    return coincidencia.group(1).strip()


class TestVerificador(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.tmp = Path(cls._tmp.name)
        cls.guia = cls.tmp / "guia"
        subprocess.run([sys.executable, str(ARREL / "generador" / "build.py"),
                        "--out", str(cls.guia)], capture_output=True, check=True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def prepara_alumne(self, nom: str) -> tuple[Path, dict[str, str]]:
        """Clona el repositori guia com si fos el fork de l'alumne."""
        base = Path(tempfile.mkdtemp(dir=self.tmp, prefix=nom + "-"))
        entorn = entorn_alumne(base)
        clon = base / "git-rocinante"
        subprocess.run(["git", "clone", "--quiet", str(self.guia), str(clon)],
                       env=entorn, capture_output=True, check=True)
        return clon, entorn

    def resol_i_verifica(self, script: Path, pas: str) -> subprocess.CompletedProcess[str]:
        clon, entorn = self.prepara_alumne(script.stem)
        entorn["PYTHON"] = sys.executable
        if pas != "00":
            # A partir del pas 01, l'alumne ja ha fet el pas 00. L'editor `true`
            # accepta el missatge per defecte sense obrir cap finestra.
            for clau, valor in (("user.name", "Camina Drummer"),
                                ("user.email", "camina.drummer@exemple.cat"),
                                ("core.editor", "true")):
                subprocess.run(["git", "config", "--global", clau, valor],
                               env=entorn, check=True)
        solucio = subprocess.run(["bash", str(script)], cwd=clon, env=entorn,
                                 capture_output=True, encoding="utf-8")
        self.assertEqual(solucio.returncode, 0, f"{script.name}: {solucio.stderr}")
        return subprocess.run([sys.executable, "verifica.py", pas], cwd=clon, env=entorn,
                              capture_output=True, encoding="utf-8")

    def test_solucions_correctes_superen_la_verificacio(self) -> None:
        scripts = sorted(SOLUCIONS.glob("pas_*_ok.sh"))
        self.assertTrue(scripts, "no hi ha cap solució correcta")
        for script in scripts:
            pas = script.name.split("_")[1]
            with self.subTest(script=script.name):
                resultat = self.resol_i_verifica(script, pas)
                self.assertEqual(resultat.returncode, 0, resultat.stdout + resultat.stderr)
                self.assertNotIn("[FALLA]", resultat.stdout)
                self.assertIn("[OK]", resultat.stdout)

    def test_solucions_incorrectes_fallen_amb_el_missatge_esperat(self) -> None:
        scripts = sorted(SOLUCIONS.glob("pas_*_ko_*.sh"))
        self.assertTrue(scripts, "no hi ha cap solució incorrecta")
        for script in scripts:
            pas = script.name.split("_")[1]
            with self.subTest(script=script.name):
                resultat = self.resol_i_verifica(script, pas)
                self.assertEqual(resultat.returncode, 1, resultat.stdout + resultat.stderr)
                falles = [l for l in resultat.stdout.splitlines() if l.startswith("[FALLA]")]
                text = espera(script)
                self.assertTrue(any(text in l for l in falles),
                                f"cap línia [FALLA] conté «{text}»:\n{resultat.stdout}")

    def test_cada_pas_amb_solucio_te_almenys_una_solucio_incorrecta(self) -> None:
        passos_ok = {s.name.split("_")[1] for s in SOLUCIONS.glob("pas_*_ok.sh")}
        passos_ko = {s.name.split("_")[1] for s in SOLUCIONS.glob("pas_*_ko_*.sh")}
        self.assertEqual(passos_ok, passos_ko)

    def test_no_modifica_el_repositori(self) -> None:
        clon, entorn = self.prepara_alumne("nomes-llegeix")
        abans = self._estat(clon, entorn)
        subprocess.run([sys.executable, "verifica.py", "00"], cwd=clon, env=entorn,
                       capture_output=True, encoding="utf-8")
        self.assertEqual(self._estat(clon, entorn), abans)

    @staticmethod
    def _estat(clon: Path, entorn: dict[str, str]) -> str:
        ordres = (["for-each-ref"], ["status", "--porcelain", "--ignored"],
                  ["config", "--list", "--show-origin"])
        return "\n".join(
            subprocess.run(["git", *o], cwd=clon, env=entorn, capture_output=True,
                           encoding="utf-8").stdout for o in ordres)

    def test_errors_d_entorn_acaben_amb_codi_2(self) -> None:
        clon, entorn = self.prepara_alumne("errors")
        verifica = clon / "verifica.py"
        self.assertTrue(verifica.is_file(), "el repositori guia no té verifica.py")
        fora = Path(tempfile.mkdtemp(dir=self.tmp))
        casos = {
            "sense arguments": ([], clon),
            "pas inexistent": (["99"], clon),
            "fora d'un repositori": (["00"], fora),
        }
        for nom, (arguments, directori) in casos.items():
            with self.subTest(cas=nom):
                resultat = subprocess.run([sys.executable, str(verifica), *arguments],
                                          cwd=directori, env=entorn,
                                          capture_output=True, encoding="utf-8")
                self.assertEqual(resultat.returncode, 2, resultat.stdout + resultat.stderr)
                self.assertNotIn("Traceback", resultat.stderr)


if __name__ == "__main__":
    unittest.main()
