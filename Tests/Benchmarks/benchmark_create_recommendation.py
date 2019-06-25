import cProfile
import Recommendation_lib.recommendations_formations as rl
from Recommendation_lib import Ranking, Game

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

    ranking_dict = rl.ranking_list_to_dict(rank_list)
    recom_dict = rl.formations_info_recom(game_list, ranking_dict, 2, 1)

    cp.disable()
    cp.print_stats()
