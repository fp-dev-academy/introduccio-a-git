"""Tests de rocinante/navegacio.py. Ús: python tests/test_navegacio.py"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rocinante.navegacio import temps_trajecte  # noqa: E402


class TestTempsTrajecte(unittest.TestCase):
    def test_una_hora(self):
        # 36.000 km a 10 km/s són 3.600 s, és a dir, 1 hora.
        self.assertAlmostEqual(temps_trajecte(36_000, 10), 1.0)

    def test_terra_lluna(self):
        # 384.400 km a 20 km/s: 19.220 s, unes 5,34 hores (5,3389).
        self.assertAlmostEqual(temps_trajecte(384_400, 20), 5.339, places=3)


if __name__ == "__main__":
    unittest.main()
