"""Thumbnail tests"""
import unittest
import sys
sys.path.append("..")
from Vodgen import thumbnail

class MatchInfoTests(unittest.TestCase):
    """Tests match info methods"""

    def tests_set_tournament_round(self):
        """Tests the parser who shortens title"""
        match = thumbnail.MatchInfo("Brult")

        match.set_tournament_round("Round 1")
        self.assertEqual(match.tournament_round, "R1")
