import unittest

from config import Config

class ConfigTest(unittest.TestCase):
    example = "../config/userdata.txt"

    def test_loadFile(self):
        config = Config.fromFile(self.example)
        self.assertEqual(open(self.example, "r").readlines(), config.data)


if __name__ == '__main__':
    unittest.main()