import cProfile
from Recommendation_lib import Ranking, Game, LeagueRecom

if __name__ == "__main__":
    cp = cProfile.Profile()
    cp.enable()

    rank_list = []
    rank_list.append(Ranking.Ranking("A", 1, "2019", "eredivisie"))
    rank_list.append(Ranking.Ranking("B", 2, "2019", "eredivisie"))
    rank_list.append(Ranking.Ranking("C", 3, "2019", "eredivisie"))
    rank_list.append(Ranking.Ranking("D", 4, "2019", "eredivisie"))

    game_list = []
    game_list.append(Game.Game("A", "4-4-2", "B", "4-3-3", 4, 2, "2019"))
    game_list.append(Game.Game("C", "4-4-2", "D", "4-1-4-1", 2, 2, "2019"))
    game_list.append(Game.Game("D", "3-5-2", "A", "3-4-3", 1, 0, "2019"))
    game_list.append(Game.Game("A", "4-4-2", "C", "3-5-2", 0, 4, "2019"))

    test_game_list = []
    test_game_list.append(Game.Game("A", "4-4-2", "B", "4-3-3", 1, 0, "2019"))
    test_game_list.append(Game.Game("B", "4-1-4-1", "C", "4-4-2", 1, 0, "2019"))
    test_game_list.append(Game.Game("C", "3-5-2", "D", "3-4-3", 1, 1, "2019"))
    test_game_list.append(Game.Game("D", "5-3-2", "A", "4-4-2", 1, 0, "2019"))

    league_recom = LeagueRecom.LeagueRecom(game_list, rank_list, 2, 1)
    league_recom.create_league_recom()
    league_recom.validate_recom_dict(test_game_list)

    cp.disable()
    cp.print_stats()
