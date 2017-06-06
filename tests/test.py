from .context import package
import unittest


class BasicTestSuite(unittest.TestCase):

    def test_something(self):
        self.assertIsNone(package.start())

if __name__ == '__main__':
    unittest.main()
