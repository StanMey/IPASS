import mysql_connect as mc
import recommendations_formations as rf


def validate_formation_algorithm(recom_dict, test_matches):
    """Per formation the two most promising counter formations are given back
    Over these counter formations the algorithm is validated
    The recommendation dictionary is validated and a string with the accuracy is returned

    Parameters
    ----------
    recom_dict : dictionary
        The dictionary which holds all the recommendations for the formations
    test_matches : list
        A list of Game objects to test the recommendation dictionary

    Returns
    -------
    String
        the function returns a string which gives some information about the accuracy of the recommendation
        dictionary over the test_matches
   """

    # a dictionary to save the actual recommendations
    actual_recom = {}

    # loop over every key in the recommendation dictionary
    for first_key in recom_dict:

        # initiate an empty list for storing the recommendations
        actual_recom[first_key] = []

        if len(recom_dict[first_key]) == 1:
            # the formation only has one recom formation
            actual_recom[first_key].append(list(recom_dict[first_key].keys())[0])

        elif len(recom_dict[first_key]) == 2:
            # the formation only has two recom formations
            formations = list(recom_dict.keys())
            actual_recom[first_key].append(formations[0])
            actual_recom[first_key].append(formations[1])
        else:
            # the formation has more than two recom formations
            loop_count = 1
            first_recom = []
            second_recom = []

            # loop over every key in the dictionary
            for second_key in recom_dict[first_key]:
                if loop_count == 1:
                    # first loop
                    first_recom.append(second_key)
                    first_recom.append(recom_dict[first_key][second_key])
                elif loop_count == 2:
                    # second loop
                    second_recom.append(second_key)
                    second_recom.append(recom_dict[first_key][second_key])
                else:
                    # 3rd or higher loop
                    if recom_dict[first_key][second_key] > first_recom[1]:
                        # if the new formation is better than the one on first_recom
                        first_recom[0] = second_key
                        first_recom[1] = recom_dict[first_key][second_key]
                    else:
                        # the new formation is not better
                        if recom_dict[first_key][second_key] > second_recom[1]:
                            # if the new formation is better than the one on second_recom
                            second_recom[0] = second_key
                            second_recom[1] = recom_dict[first_key][second_key]
                        else:
                            # the new formation is not better
                            continue
                # increment the loop count
                loop_count += 1

            # save the recommendations into the actual_recom dict
            actual_recom[first_key].append(first_recom[0])
            actual_recom[first_key].append(second_recom[0])

    #
    total_count = 0
    win_count = 0

    # loop over all game objects
    for match in test_matches:
        if match.get_home_formation() in actual_recom:
            # the formation of the home team is in the recommendation dict
            if match.get_away_formation in actual_recom[match.get_home_formation()]:
                # the formation of the away score is given as a recommended formation
                if match.get_home_score > match.get_away_score():
                    # match won
                    win_count += 1
                    total_count += 1
                else:
                    # match lost or draw
                    total_count += 1

        if match.get_away_formation() in actual_recom:
            # the formation of the away team is in the recommendation dict
            if match.get_home_formation() in actual_recom[match.get_away_formation()]:
                # the formation of the home score is given as a recommended formation
                if match.get_away_score() > match.get_home_score():
                    # match won
                    win_count += 1
                    total_count += 1
                else:
                    # match lost or draw
                    total_count += 1

    # return a string with the accuracy
    return "The algorithm recommends with an accuracy of {0}%".format(round((win_count / total_count) * 100))


# testing the code
if __name__ == "__main__":
    # select the training match data
    training_data_dates = ('2016/17', '2017/18', '2018/19')
    training_data_matches = mc.retrieve_seasonal_table_data('Game', 'Premier League', training_data_dates)
    training_data_matches_list = mc.sql_data_to_game_objects(training_data_matches)

    # select the training ranking data
    seasons_ranking = mc.retrieve_seasonal_table_data('Ranking', 'Premier League', training_data_dates)
    training_data_ranking = mc.sql_data_to_ranking_objects(seasons_ranking)
    training_data_ranking_dict = rf.ranking_list_to_dict(training_data_ranking)

    # train the recommendations dictionary
    match_recommendation = rf.formations_info_recom(training_data_matches_list, training_data_ranking_dict, 2, 1)

    # select the test data
    test_data_dates = ('2015/16', 0)
    test_data_matches = mc.retrieve_seasonal_table_data('Game', 'Premier League', test_data_dates)
    test_data_matches_list = mc.sql_data_to_game_objects(test_data_matches)

    # validate the recommendation
    validate_result = validate_formation_algorithm(match_recommendation, test_data_matches_list)
    print(validate_result)
