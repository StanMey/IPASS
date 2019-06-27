import unittest
from Recommendation_lib.Game import Game


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game1 = Game("A", "4-4-2", "B", "4-3-3", 4, 2, "2019")
        self.game2 = Game("C", "4-3-2-1", "D", "4-1-4-1", 2, 2, "2019")

    def tearDown(self) -> None:
        self.game1 = None
        self.game2 = None

    def test_attributes(self):
        self.assertEqual(self.game1.get_home_team(), "A")
        self.assertEqual(self.game2.get_home_team(), "C")

        self.assertEqual(self.game1.get_home_formation(), "4-4-2")
        self.assertEqual(self.game2.get_home_formation(), "4-3-2-1")

        self.assertEqual(self.game1.get_away_team(), "B")
        self.assertEqual(self.game2.get_away_team(), "D")

        self.assertEqual(self.game1.get_away_formation(), "4-3-3")
        self.assertEqual(self.game2.get_away_formation(), "4-1-4-1")

        self.assertEqual(self.game1.get_home_score(), 4)
        self.assertEqual(self.game2.get_home_score(), 2)

        self.assertEqual(self.game1.get_away_score(), 2)
        self.assertEqual(self.game2.get_away_score(), 2)

        self.assertEqual(self.game1.get_season(), "2019")
        self.assertEqual(self.game2.get_season(), "2019")


if __name__ == '__main__':
    unittest.main()
