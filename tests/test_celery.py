import unittest
from tasks.import_triple_data.tasks import open_file

class TestCelery(unittest.TestCase):
    def test_open_file(self):
        result = open_file('tests/test_triple.csv')
        assert result == 1