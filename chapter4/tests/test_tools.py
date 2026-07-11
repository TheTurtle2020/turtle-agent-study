import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import mask_secret


class MaskSecretTests(unittest.TestCase):
    def test_masks_long_secret_value(self):
        self.assertEqual(mask_secret("abcdef123456"), "ab****56")

    def test_masks_empty_value(self):
        self.assertEqual(mask_secret(""), "")


if __name__ == "__main__":
    unittest.main()
