from __future__ import absolute_import
import os
from src.combine_diff import Diff
import unittest
import tempfile

PAGE_STORAGE = "pages"
DIFF_SUFFIX = ".diff"
TMP_DIR = tempfile.gettempdir()


class DiffTest(unittest.TestCase):

    def test_generate_diff(self):
        diff = Diff()
        diff.generate_diffs(1, 0)

    def test_combine_diffs(self):
        diff = Diff()
        diff.combine_diffs(0, 1, 0)
        new_diff_file = os.path.join(TMP_DIR, "comb_diff_" + str(0) + "_" + str(0) + "_" + str(1) + DIFF_SUFFIX)
        new_diff = open(new_diff_file).readlines()[2:]
        original_diff_file = os.path.join(PAGE_STORAGE, "0_1.diff")
        original_diff = open(original_diff_file).readlines()[2:]
        self.assertEqual(new_diff, original_diff, "Both diff should match")

    def test_reset_env(self):
        new_path = os.path.join(PAGE_STORAGE, "0_1")
        command = 'echo "I dont know what to write" > ' + new_path
        os.system(command)

if __name__ == '__main__':
    unittest.main()
