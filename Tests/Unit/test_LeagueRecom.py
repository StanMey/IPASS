import unittest
from Recommendation_lib.Game import Game
from Recommendation_lib.Ranking import Ranking
from Recommendation_lib.LeagueRecom import LeagueRecom


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game1 = Game("A", "4-4-2", "B", "4-3-3", 4, 2, "2019")
        self.game2 = Game("C", "4-4-2", "D", "4-1-4-1", 2, 2, "2019")
        self.game3 = Game("D", "3-5-2", "A", "3-4-3", 1, 0, "2019")
        self.game4 = Game("A", "4-4-2", "C", "3-5-2", 0, 4, "2019")
        self.match_list = [self.game1, self.game2, self.game3, self.game4]

        self.rank1 = Ranking("A", 1, "2019", "eredivisie")
        self.rank2 = Ranking("B", 2, "2019", "eredivisie")
        self.rank3 = Ranking("C", 3, "2019", "eredivisie")
        self.rank4 = Ranking("D", 4, "2019", "eredivisie")
        self.rank_list = [self.rank1, self.rank2, self.rank3, self.rank4]

        self.test_game1 = Game("A", "4-4-2", "B", "4-3-3", 1, 0, "2019")
        self.test_game2 = Game("B", "4-1-4-1", "C", "4-4-2", 1, 0, "2019")
        self.test_game3 = Game("C", "3-5-2", "D", "3-4-3", 1, 1, "2019")
        self.test_game4 = Game("D", "5-3-2", "A", "4-4-2", 1, 0, "2019")
        self.test_match_list = [self.test_game1, self.test_game2, self.test_game3, self.test_game4]

        self.league_recom1 = LeagueRecom(self.match_list, self.rank_list, 2, 1)

        self.league_recom1.ranking_list_to_dict()
        self.league_recom1.formations_info_recom()
        self.league_recom1.create_league_recom()
        self.league_recom1.validate_recom_dict(self.test_match_list)

    def tearDown(self) -> None:
        self.game1 = None
        self.game2 = None
        self.game3 = None
        self.game4 = None
        self.match_list = None

        self.rank1 = None
        self.rank2 = None
        self.rank3 = None
        self.rank4 = None
        self.rank_list = None

        self.test_game1 = None
        self.test_game2 = None
        self.test_game3 = None
        self.test_game4 = None
        self.test_match_list = None

        self.league_recom1 = None

    def test_ranking_list_to_dict(self):
        expected_rank_list = {"2019": {"A": 1, "B": 2, "C": 3, "D": 4}}
        self.assertEqual(self.league_recom1.ranking_list_to_dict(), expected_rank_list)

    def test_formations_info_recom(self):
        expected_recom_dict = {"4-4-2": {"4-3-3": 2.0,
                                         "4-1-4-1": 3.5},
                               "3-5-2": {"3-4-3": 8.0,
                                         "4-4-2": 6.0},
                               "4-1-4-1": {"4-4-2": 3.5}}
        self.assertEqual(self.league_recom1.formations_info_recom(), expected_recom_dict)

    def test_create_league_recom(self):
        expected_recom_dict = {"4-4-2": {"4-3-3": 2.0,
                                         "4-1-4-1": 3.5},
                               "3-5-2": {"3-4-3": 8.0,
                                         "4-4-2": 6.0},
                               "4-1-4-1": {"4-4-2": 3.5}}
        self.assertEqual(self.league_recom1.create_league_recom(), expected_recom_dict)

    def test_validate_recom_dict(self):
        expected_output = "The algorithm recommends with an accuracy of 50%"
        self.assertEqual(self.league_recom1.validate_recom_dict(self.test_match_list), expected_output)


if __name__ == '__main__':
    unittest.main()
