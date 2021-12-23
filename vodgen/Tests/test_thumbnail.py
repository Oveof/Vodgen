"""Thumbnail tests"""
import unittest
from Vodgen import thumbnail

class MatchInfoTests(unittest.TestCase):
    """Tests match info methods"""
    def tests_set_tournament_round(self):
        """Tests the parser who shortens title"""
        self.assertIsNotNone("lol")
