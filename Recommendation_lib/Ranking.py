class Ranking:
    """
    The Vehicles object contains lots of vehicles

    Parameters
    ----------
    team : String
        The name of the team
    season : String
        The season in which the rank exists
    rank : int
        The rank of a team in a season
    league : String
        The league in which the rank is given

    Attributes
    ----------
    team : String
        Stores the name of the team
    season : String
        Stores the season in which the rank exists
    rank : int
        Stores the rank of the team this particular season
    league : String
        Stores the league in which the rank exists for the team
    """

    # constructor
    def __init__(self, team: str, rank: int, season: str, league: str):
        try:
            self.team = team
            self.rank = rank
            self.season = season
            self.league = league
        except ValueError as e:
            print("An incorrect variable type was entered\n", e)

    # public methods
    def get_team(self):
        return self.team

    def get_rank(self):
        return self.rank

    def get_season(self):
        return self.season

    def get_league(self):
        return self.league
