from src.utils import *
import unittest

PAGE_STORAGE = "pages"


class UtilsTest(unittest.TestCase):
    def test_current_version_1( self ):
        version = get_page_current_version("0")
        self.assertEqual(version, "1", "Current Version for page 0 is 1")

    def test_current_version_2( self ):
        version = get_page_current_version("a")
        self.assertEqual(version, "1", "Current Version for page 0 is 1")

    def test_current_version_invalid_page_1( self ):
        version = get_page_current_version("10")
        self.assertEqual(version, "-1", "Page does exists!")

    def test_current_version_invalid_page_2( self ):
        version = get_page_current_version("ab")
        self.assertEqual(version, "-1", "Page does exists!")

    def test_update_version( self ):
        result = update_version("0")
        version = get_page_current_version("0")
        self.assertEqual(result, "Success", "Successfully updated Version")
        self.assertEqual(version, "2", "Updated version is 2")

    def test_update_version_invalid_page( self ):
        result = update_version("11")
        self.assertEqual(result, "Error", "Page does not exist")


if __name__ == '__main__':
    unittest.main()
