import unittest
from Recommendation_lib.Ranking import Ranking


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.ranking1 = Ranking("A", 1, "2019", "eredivisie")
        self.ranking2 = Ranking("B", 2, "2017", "Serie A")

    def tearDown(self) -> None:
        self.ranking1 = None
        self.ranking2 = None

    def test_attributes(self):
        self.assertEqual(self.ranking1.get_team(), "A")
        self.assertEqual(self.ranking2.get_team(), "B")

        self.assertEqual(self.ranking1.get_rank(), 1)
        self.assertEqual(self.ranking2.get_rank(), 2)

        self.assertEqual(self.ranking1.get_season(), "2019")
        self.assertEqual(self.ranking2.get_season(), "2017")

        self.assertEqual(self.ranking1.get_league(), "eredivisie")
        self.assertEqual(self.ranking2.get_league(), "Serie A")


if __name__ == '__main__':
    unittest.main()
