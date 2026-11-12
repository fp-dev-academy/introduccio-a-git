"""Tests de rocinante/combustible.py. Ús: python tests/test_combustible.py"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rocinante.combustible import calcula_consum  # noqa: E402


class TestCalculaConsum(unittest.TestCase):
    def test_consum_basic(self):
        self.assertAlmostEqual(calcula_consum(100, 1), 80.0)

    def test_consum_proporcional_a_l_acceleracio(self):
        self.assertAlmostEqual(calcula_consum(100, 3), 3 * calcula_consum(100, 1))


if __name__ == "__main__":
    unittest.main()
