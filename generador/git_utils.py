"""Wrapper de git per al generador, amb entorn aïllat i dates fixades.

Tot el que influeix en els hashos (autor, committer, dates, configuració)
està fixat, de manera que les mateixes operacions produeixen sempre els
mateixos hashos, independentment de la màquina i de la configuració de git
de qui executa el generador.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from types import TracebackType

TRIPULACIO: dict[str, tuple[str, str]] = {
    "holden": ("James Holden", "holden@rocinante.mcrn"),
    "naomi": ("Naomi Nagata", "naomi@rocinante.mcrn"),
    "amos": ("Amos Burton", "amos@rocinante.mcrn"),
    "alex": ("Alex Kamal", "alex@rocinante.mcrn"),
}

DATA_BASE = datetime.fromisoformat("2026-01-05T09:00:00+01:00")
INTERVAL = timedelta(minutes=17)

# Configuració que s'aplica a cada ordre (equivalent a `git -c clau=valor`).
CONFIGURACIO = {
    "commit.gpgsign": "false",
    "tag.gpgsign": "false",
    "init.defaultBranch": "main",
    "core.autocrlf": "false",
}


class Repo:
    """Repositori git que el generador construeix commit a commit."""

    def __init__(self, directori: Path, config_buida: Path) -> None:
        self.directori = directori
        self._config_buida = config_buida
        self._commits = 0

    @classmethod
    def crea(cls, directori: Path) -> Repo:
        """Crea el directori i hi inicia un repositori buit."""
        directori.mkdir(parents=True)
        descriptor, ruta = tempfile.mkstemp(prefix="gitconfig-generador-")
        os.close(descriptor)
        repo = cls(directori, Path(ruta))
        repo.git("init", "--quiet")
        return repo

    def __enter__(self) -> Repo:
        return self

    def __exit__(
        self,
        tipus: type[BaseException] | None,
        error: BaseException | None,
        traca: TracebackType | None,
    ) -> None:
        self._config_buida.unlink(missing_ok=True)

    def _entorn(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        entorn = {
            clau: valor for clau, valor in os.environ.items()
            if not clau.startswith("GIT_")
        }
        entorn["GIT_CONFIG_NOSYSTEM"] = "1"
        entorn["GIT_CONFIG_GLOBAL"] = str(self._config_buida)
        entorn["GIT_CONFIG_COUNT"] = str(len(CONFIGURACIO))
        for i, (clau, valor) in enumerate(CONFIGURACIO.items()):
            entorn[f"GIT_CONFIG_KEY_{i}"] = clau
            entorn[f"GIT_CONFIG_VALUE_{i}"] = valor
        entorn.update(extra or {})
        return entorn

    def git(self, *args: str, extra: dict[str, str] | None = None) -> str:
        """Executa una ordre de git dins del repositori i en retorna la sortida."""
        resultat = subprocess.run(
            ["git", *args],
            cwd=self.directori,
            env=self._entorn(extra),
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
        return resultat.stdout.strip()

    def escriu(self, ruta: str, contingut: str) -> None:
        """Escriu un fitxer (UTF-8, salts de línia LF) i l'afegeix a l'índex."""
        fitxer = self.directori / ruta
        fitxer.parent.mkdir(parents=True, exist_ok=True)
        fitxer.write_text(contingut, encoding="utf-8", newline="\n")
        self.git("add", "--", ruta)

    def _identitat(self, tripulant: str, data: datetime) -> dict[str, str]:
        nom, correu = TRIPULACIO[tripulant]
        return {
            "GIT_AUTHOR_NAME": nom,
            "GIT_AUTHOR_EMAIL": correu,
            "GIT_AUTHOR_DATE": data.isoformat(),
            "GIT_COMMITTER_NAME": nom,
            "GIT_COMMITTER_EMAIL": correu,
            "GIT_COMMITTER_DATE": data.isoformat(),
        }

    def commit(self, missatge: str, tripulant: str) -> str:
        """Fa un commit del que hi ha a l'índex i en retorna el hash."""
        identitat = self._identitat(tripulant, DATA_BASE + self._commits * INTERVAL)
        self.git("commit", "--quiet", "--message", missatge, extra=identitat)
        self._commits += 1
        return self.git("rev-parse", "HEAD")

    def revert(self, commit: str, tripulant: str) -> str:
        """Fa `git revert` d'un commit amb el missatge per defecte i en retorna el hash."""
        identitat = self._identitat(tripulant, DATA_BASE + self._commits * INTERVAL)
        self.git("revert", "--no-edit", commit, extra=identitat)
        self._commits += 1
        return self.git("rev-parse", "HEAD")

    def merge(self, branca: str, tripulant: str,
              resolucio: dict[str, str] | None = None) -> str:
        """Fa un merge amb commit de merge (--no-ff) i en retorna el hash.

        Si hi ha conflictes, `resolucio` dona el contingut final de cada fitxer
        en conflicte. Si en falta algun, és un error.
        """
        identitat = self._identitat(tripulant, DATA_BASE + self._commits * INTERVAL)
        resultat = subprocess.run(
            ["git", "merge", "--no-ff", "--no-edit", branca],
            cwd=self.directori, env=self._entorn(identitat),
            capture_output=True, encoding="utf-8",
        )
        if resultat.returncode != 0:
            en_conflicte = set(self.git("diff", "--name-only", "--diff-filter=U").splitlines())
            if not en_conflicte or not en_conflicte <= set(resolucio or {}):
                self.git("merge", "--abort")
                raise RuntimeError(f"merge de {branca} amb conflictes sense resoldre: "
                                   f"{sorted(en_conflicte)}\n{resultat.stdout}{resultat.stderr}")
            for ruta in sorted(en_conflicte):
                self.escriu(ruta, resolucio[ruta])
            self.git("commit", "--quiet", "--no-edit", extra=identitat)
        self._commits += 1
        return self.git("rev-parse", "HEAD")

    def tag(self, nom: str, missatge: str, tripulant: str) -> None:
        """Crea un tag anotat a HEAD amb la data de l'últim commit."""
        data = DATA_BASE + (self._commits - 1) * INTERVAL
        self.git("tag", "--annotate", nom, "--message", missatge,
                 extra=self._identitat(tripulant, data))
