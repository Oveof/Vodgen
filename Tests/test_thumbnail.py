"""Thumbnail tests"""
import unittest
from thumbnail import MatchInfo

class MatchInfoTests(unittest.TestCase):
    """Tests match info methods"""
    def tests_set_tournament_round(self):
        """Tests the parser who shortens title"""
        match = MatchInfo("Brult")

        match.set_tournament_round("Round 1")
        self.assertEqual(match.tournament_round, "R1")
