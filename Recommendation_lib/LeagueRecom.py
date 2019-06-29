class LeagueRecom:
    """
    A LeagueRecom object holds information about the rankings and results of a couple of seasons
    from a certain league

    Parameters
    ----------
    games : list
        A list with Game objects stored in it
    rankings : list
        A list with Ranking objects stored in it
    w_points : int
        The amount of points a formation gets when it wins
    d_points : int
        The amount of points a formation gets when it plays a draw

    Attributes
    ----------
    matches_list : list
        Stores all the Game objects in a list
    ranking_list : list
        Stores all the Ranking objects in a list
    win_points : int
        Stores the amount of points a winning formation gets
    draw_points : int
        Stores the amount of points a formation gets for a draw
    ranking_dict : dictionary
        Stores the dictionary of all the rankings of a team per year once it's generated
    recom_dict : dictionary
        Stores the recommendation dictionary of the league once it's generated
    """

    def __init__(self, games: list, rankings: list, w_points: int, d_points: int):
        try:
            self.matches_list = games
            self.ranking_list = rankings
            self.win_points = w_points
            self.draw_points = d_points
            self.ranking_dict = None
            self.recom_dict = None
        except ValueError as e:
            print("An incorrect variable type was entered\n", e)

    def ranking_list_to_dict(self):
        """
        Constructs based on the Ranking a dictionary with per season the rank of a club

        Raises
        ----------
        AttributeError
            When the ranking_list doesn't contain objects of the Ranking class
        TypeError
            When a wrong type is inserted into the object as ranking_list
        Exception
            When an unexpected error happens

        Returns
        -------
        dictionary
            A dictionary with per season/year the rank of a certain club
       """
        try:
            # initialize a dictionary to save the rank info
            ranking_dict = {}

            # loop over all objects in the list
            for rank in self.ranking_list:
                if rank.get_season() not in ranking_dict:
                    # if the season key doesn't already exist
                    ranking_dict[rank.get_season()] = {}

                # saves the team as key and its rank as value in a season
                ranking_dict[rank.get_season()][rank.get_team()] = rank.get_rank()

            # update the ranking_dict of the object
            self.ranking_dict = ranking_dict
            # return the ranking_dict
            return self.ranking_dict

        # handle exceptions
        except AttributeError as e:
            print("The list does not contain objects of the class Ranking\n", e)
        except TypeError as e:
            print("No iterable type is given\n", e)
        except Exception as e:
            print("Unexpected error while generating the ranking dictionary\n", e)

    def formations_info_recom(self):
        """
        Goes over every game object in the matches_list and gives every winning and draw
        formation a certain amount of points based on the clubs rank in a season

        Raises
        ----------
        AttributeError
            When the matches_list doesn't contain objects of the Game class,
            or the ranking_dict doesn't accord with the Game objects in the matches_list
        TypeError
            When a wrong type is inserted into the object as matches_list,
            or no integer was inserted as points for a win/draw
        Exception
            When the ranking dictionary is not (yet) instantiated or an unexpected error happens

        Returns
        -------
        dictionary
            A dictionary with per formation the counter-formations with a certain amount of points
            These points are an indicator how effective a formation is against a counter-formation
       """
        try:
            if self.ranking_dict is None:
                raise Exception("The ranking dictionary is not initiated")
            # initialize a dictionary to save the formations and their points
            formations_dict = {}

            # save the win and draw points
            WIN_POINTS = self.win_points
            DRAW_POINTS = self.draw_points

            # loop over all game objects
            for game in self.matches_list:
                if game.get_home_score() > game.get_away_score():
                    # home team wins
                    # check if keys exists in the dictionary
                    self.check_for_keys_in_dict(game.get_home_formation(), game.get_away_formation(), formations_dict)

                    # calculate the amount of points for the home team win
                    points = WIN_POINTS * self.ranking_dict[game.get_season()][game.get_home_team()]
                    # save the points and increment the games played in the array
                    formations_dict[game.get_home_formation()][game.get_away_formation()][0] += points
                    formations_dict[game.get_home_formation()][game.get_away_formation()][1] += 1

                elif game.get_home_score() == game.get_away_score():
                    # draw
                    # check if keys exists in the dictionary
                    self.check_for_keys_in_dict(game.get_home_formation(), game.get_away_formation(), formations_dict)
                    self.check_for_keys_in_dict(game.get_away_formation(), game.get_home_formation(), formations_dict)

                    # calculate the amount of point for a draw
                    points = DRAW_POINTS * ((self.ranking_dict[game.get_season()][game.get_home_team()] +
                                             self.ranking_dict[game.get_season()][game.get_away_team()]) / 2)
                    # save the points and increment the games played in the array
                    formations_dict[game.get_home_formation()][game.get_away_formation()][0] += points
                    formations_dict[game.get_home_formation()][game.get_away_formation()][1] += 1
                    # save the points and increment the games played in the array
                    formations_dict[game.get_away_formation()][game.get_home_formation()][0] += points
                    formations_dict[game.get_away_formation()][game.get_home_formation()][1] += 1

                else:
                    # away team wins
                    # check if keys exists in the dictionary
                    self.check_for_keys_in_dict(game.get_away_formation(), game.get_home_formation(), formations_dict)

                    # calculate the amount of points for the away team win
                    points = WIN_POINTS * self.ranking_dict[game.get_season()][game.get_away_team()]
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

            # update the recom_dict of the object
            self.recom_dict = formations_dict
            # return the recommendation dictionary
            return formations_dict

        # handle the exceptions
        except AttributeError as e:
            print("The list does not contain objects of the class Game /"
                  "The ranking_dict may not accord with the inserted matches_list\n", e)
        except TypeError as e:
            print("No iterable type is given / win/draw points are not of type int\n", e)
        except Exception as e:
            print("Unexpected error while generating the recommendation dictionary\n", e)

    def check_for_keys_in_dict(self, key_1, key_2, chosen_dict):
        """
        Checks if key_1 exists in the chosen_dict
        hereafter checks if key_2 exists in the dictionary of key_1

        Parameters
        ----------
        key_1 : String
            The first key to be checked
        key_2 : String
            The second key to be checked in the dictionary of the first key
        chosen_dict : dictionary
            The dictionary that is being checked for the existence of certain keys
        """
        if key_1 not in chosen_dict:
            # if the key doesn't already exist as key
            chosen_dict[key_1] = {}

        if key_2 not in chosen_dict[key_1]:
            # if the key doesn't exist in the dictionary of the first key as key
            chosen_dict[key_1][key_2] = [0.0, 0]

    def create_league_recom(self):
        """
        Calls all the methods of the object in order to build a recommendation
        dictionary for the Games in the matches_list and the Rankings in the ranking_list

        Returns
        -------
            Returns the recommendation dictionary
       """
        # build the ranking_dict
        self.ranking_list_to_dict()
        self.formations_info_recom()

        # return the recommendation dictionary
        return self.recom_dict

    def validate_recom_dict(self, test_matches):
        """Per formation the two most promising counter formations are given back
        Over these counter formations the algorithm is validated
        The recommendation dictionary is validated and a string with the accuracy is returned

        Parameters
        ----------
        test_matches : list
            A list of Game objects to test the recommendation dictionary

        Raises
        ------
        AttributeError
            When the test_matches list doesn't contain objects of the Game class
        TypeError
            When a wrong type is inserted into as a parameter
        Exception
            When the recommendation dictionary is not (yet) instantiated or an unexpected error happens

        Returns
        -------
        String
            the function returns a string which gives some information about the accuracy of the recommendation
            dictionary over the test_matches
       """
        try:
            if self.recom_dict is None:
                raise Exception("The recommendation dictionary is not initiated")

            # a dictionary to save the actual recommendations
            actual_recom = {}

            # loop over every key in the recommendation dictionary
            for first_key in self.recom_dict:

                # initiate an empty list for storing the recommendations
                actual_recom[first_key] = []

                if len(self.recom_dict[first_key]) == 1:
                    # the formation only has one recom formation
                    actual_recom[first_key].append(list(self.recom_dict[first_key].keys())[0])

                elif len(self.recom_dict[first_key]) == 2:
                    # the formation only has two recom formations
                    formations = list(self.recom_dict[first_key].keys())
                    actual_recom[first_key].append(formations[0])
                    actual_recom[first_key].append(formations[1])
                else:
                    # the formation has more than two recom formations
                    loop_count = 1
                    first_recom = []
                    second_recom = []

                    # loop over every key in the dictionary of the first key
                    for second_key in self.recom_dict[first_key]:
                        if loop_count == 1:
                            # first loop
                            first_recom.append(second_key)
                            first_recom.append(self.recom_dict[first_key][second_key])
                        elif loop_count == 2:
                            # second loop
                            second_recom.append(second_key)
                            second_recom.append(self.recom_dict[first_key][second_key])
                        else:
                            # 3rd or higher loop
                            if self.recom_dict[first_key][second_key] > first_recom[1]:
                                # if the new formation is better than the one on first_recom
                                first_recom[0] = second_key
                                first_recom[1] = self.recom_dict[first_key][second_key]
                            else:
                                # the new formation is not better
                                if self.recom_dict[first_key][second_key] > second_recom[1]:
                                    # if the new formation is better than the one on second_recom
                                    second_recom[0] = second_key
                                    second_recom[1] = self.recom_dict[first_key][second_key]
                                else:
                                    # the new formation is not better
                                    continue
                        # increment the loop count
                        loop_count += 1

                    # save the recommendations into the actual_recom dict
                    actual_recom[first_key].append(first_recom[0])
                    actual_recom[first_key].append(second_recom[0])

            # initialize the variables to save the amount of matches and wins
            total_count = 0
            win_count = 0

            # loop over all game objects
            for match in test_matches:
                if match.get_home_formation() in actual_recom:
                    # the formation of the home team is in the recommendation dict
                    if match.get_away_formation() in actual_recom[match.get_home_formation()]:
                        # the formation of the away score is given as a recommended formation
                        if match.get_home_score() > match.get_away_score():
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

            # check if total_count is 0
            if total_count == 0:
                # total_count is 0, therefore the recom_dict can't be tested properly
                total_accuracy = "The accuracy can't be properly calculated"
            else:
                # total count is above 0, so the recom_dict has been tested
                total_accuracy = "The algorithm recommends with an accuracy of {0}%".format(round((win_count / total_count) * 100))
            # return a string with the accuracy
            return total_accuracy

        # handling the exceptions
        except AttributeError as e:
            print("The test_matches list does not contain objects of the class Game\n", e)
        except TypeError as e:
            print("No iterable type is given as parameter\n", e)
        except Exception as e:
            print("Unexpected error while testing the accuracy\n", e)
