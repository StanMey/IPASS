import mysql_connect as mc


def ranking_list_to_dict(rank_data):
    """Constructs based on Ranking data a dictionary with per season
    the rank of a club

    Parameters
    ----------
    rank_data : list
        A list with Ranking objects

    Returns
    -------
    dictionary
        A dictionary is returned with per year the rank per team
   """

    # initialize a dictionary to save the rank info
    ranking_dict = {}

    # loop over all objects in the list
    for rank in rank_data:
        if rank.get_season() not in ranking_dict:
            # if the season key doesn't already exist
            ranking_dict[rank.get_season()] = {}

        # saves the team as key and its rank as value in a season
        ranking_dict[rank.get_season()][rank.get_team()] = rank.get_rank()

    # return the ranking dictionary
    return ranking_dict


def formations_info_recom(games_list, ranking_dict, win_points, draw_points):
    """Go over every game object in the games_list and gives every winning and draw
    formation a certain amount of points based on the clubs rank in a season

    Parameters
    ----------
    games_list : list
        A list with Game objects
    ranking_dict : dictionary
        A dictionary with per year the rank per team
    win_points : int
        The amount of points a win is given
    draw_points : int
        The amount of points a draw is given

    Returns
    -------
    dictionary
        A dictionary with per formation the counter-formations with a certain amount of points
        These points are an indicator how effective a formation is against a counter-formation
   """

    # initialize a dictionary to save the formations and their points
    formations_dict = {}

    # save the win and draw points
    WIN_POINTS = win_points
    DRAW_POINTS = draw_points

    # loop over all game objects
    for game in games_list:
        if game.get_home_score() > game.get_away_score():
            # home team wins
            if game.get_home_formation() not in formations_dict:
                # if the formation doesn't already exist as key
                formations_dict[game.get_home_formation()] = {}

            if game.get_away_formation() not in formations_dict[game.get_home_formation()]:
                # if the formation doesn't exist in the dictionary of the first formation as key
                formations_dict[game.get_home_formation()][game.get_away_formation()] = [0.0, 0]

            # calculate the amount of points for the home team win
            points = WIN_POINTS * ranking_dict[game.get_season()][game.get_home_team()]
            # save the points and increment the games played in the array
            formations_dict[game.get_home_formation()][game.get_away_formation()][0] += points
            formations_dict[game.get_home_formation()][game.get_away_formation()][1] += 1

        elif game.get_home_score() == game.get_away_score():
            # draw
            if game.get_home_formation() not in formations_dict:
                # if the formation doesn't already exist as key
                formations_dict[game.get_home_formation()] = {}

            if game.get_away_formation() not in formations_dict[game.get_home_formation()]:
                # if the formation doesn't exist in the dictionary of the first formation as key
                formations_dict[game.get_home_formation()][game.get_away_formation()] = [0.0, 0]

            if game.get_away_formation() not in formations_dict:
                # if the formation doesn't already exist as key
                formations_dict[game.get_away_formation()] = {}

            if game.get_home_formation() not in formations_dict[game.get_away_formation()]:
                # if the formation doesn't exist in the dictionary of the first formation as key
                formations_dict[game.get_away_formation()][game.get_home_formation()] = [0.0, 0]

            # calculate the amount of point for a draw
            points = DRAW_POINTS * ((ranking_dict[game.get_season()][game.get_home_team()] +
                                     ranking_dict[game.get_season()][game.get_away_team()]) / 2)
            # save the points and increment the games played in the array
            formations_dict[game.get_home_formation()][game.get_away_formation()][0] += points
            formations_dict[game.get_home_formation()][game.get_away_formation()][1] += 1
            # save the points and increment the games played in the array
            formations_dict[game.get_away_formation()][game.get_home_formation()][0] += points
            formations_dict[game.get_away_formation()][game.get_home_formation()][1] += 1

        else:
            # away team wins
            if game.get_away_formation() not in formations_dict:
                # if the formation doesn't already exist as key
                formations_dict[game.get_away_formation()] = {}

            if game.get_home_formation() not in formations_dict[game.get_away_formation()]:
                # if the formation doesn't exist in the dictionary of the first formation as key
                formations_dict[game.get_away_formation()][game.get_home_formation()] = [0.0, 0]

            # calculate the amount of points for the away team win
            points = WIN_POINTS * ranking_dict[game.get_season()][game.get_away_team()]
            # save the points and increment the games played in the array
            formations_dict[game.get_away_formation()][game.get_home_formation()][0] += points
            formations_dict[game.get_away_formation()][game.get_home_formation()][1] += 1

    # iterate over every formation
    for key in formations_dict:
        # iterate over every counter-formation
        for key_2 in formations_dict[key]:
            result_list = formations_dict[key][key_2]
            # divide the total points by the amount of games played and save the result
            formations_dict[key][key_2] = result_list[0] / result_list[1]

    # return the recommendation dictionary
    return formations_dict


# testing the code
if __name__ == '__main__':
    # getting rank info and setting the rank dictionary
    sql_ranking = mc.retrieve_table_data('Ranking', 'Premier League')
    ranking_list = mc.sql_data_to_ranking_objects(sql_ranking)
    ranking_dict = ranking_list_to_dict(ranking_list)

    # getting all the matches
    sql_formation = mc.retrieve_table_data('Game', 'Premier League')
    matches_list = mc.sql_data_to_game_objects(sql_formation)

    # construct the recommendation dictionary
    recom_dict = formations_info_recom(matches_list, ranking_dict, 2, 1)

    # save the recommendation dictionary in the db
    # mc.recom_formations_dict_to_db('Recom_formation', recom_dict, 'Premier League')
