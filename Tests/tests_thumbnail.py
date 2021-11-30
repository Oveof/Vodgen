"""Thumbnail tests"""
import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Vodgen import thumbnail

class MatchInfoTests(unittest.TestCase):
    """Tests match info methods"""
    
    def tests_set_tournament_round(self):
        """Tests the parser who shortens title"""
        match = thumbnail.MatchInfo("Brult")

        match.set_tournament_round("R1")
        self.assertEqual(match.tournament_round, "Round 1")
