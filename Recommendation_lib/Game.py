class Game:
    """
    A game object contains information about one played match in a certain season

    Parameters
    ----------
    ht : String
        The name of the home team
    hf : String
        The formation of the home team
    at : String
        The name of the away team
    af : String
        The formation of the away team
    h_score : int
        The amount of goals scored by the home team
    a_score : int
        The amount of goals scored by the away team
    season : String
        The season in which the match is played

    Attributes
    ----------
    home_team : String
        Stores the name of the home team
    home_formation : String
        Stores the formation of the home team
    away_team : String
        Stores the name of the away team
    away_formation : String
        Stores the formation of the away team
    home_score : int
        Stores the amount of scored goals by the home team
    away_score : int
        Stores the amound of scored goals by the away team
    season : String
        Stores season in which the match is played
    """

    # constructor
    def __init__(self, ht, hf, at, af, h_score, a_score, season):
        self.home_team = str(ht)
        self.home_formation = str(hf)
        self.away_team = str(at)
        self.away_formation = str(af)
        self.home_score = int(h_score)
        self.away_score = int(a_score)
        self.season = str(season)

    # public methods
    def get_home_team(self):
        return self.home_team

    def get_home_formation(self):
        return self.home_formation

    def get_away_team(self):
        return self.away_team

    def get_away_formation(self):
        return self.away_formation

    def get_home_score(self):
        return self.home_score

    def get_away_score(self):
        return self.away_score

    def get_season(self):
        return self.season
