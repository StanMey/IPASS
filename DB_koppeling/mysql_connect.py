import mysql.connector as sql
from inlogdata import *
from Recommendation_lib import Game, Ranking

mydb = sql.connect(
    user=inlogdata_user,
    password=inlogdata_password,
    host=inlogdata_host
)

DB_NAME = inlogdata_db

# save all the insert query's to INSERT_QUERIES
INSERT_QUERIES = {}
INSERT_QUERIES['Game'] = ("INSERT INTO Game "
                    "(home_team, home_formation, away_team, away_formation, home_score,"
                    "away_score, season, league)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

INSERT_QUERIES['Ranking'] = ("INSERT INTO Ranking "
                             "(team, season_rank, season, league)"
                             "VALUES (%s, %s, %s, %s)")

INSERT_QUERIES['Recom_formation'] = ("INSERT INTO Recom_formation "
                                     "(formation_1, formation_2, formation_points, league)"
                                     "VALUES (%s, %s, %s, %s)")


def get_db_cursor(db_name):
    """Set a connection to a certain database for one cursor"""

    try:
        cursor = mydb.cursor()
        cursor.execute("USE {0};".format(db_name))
        return mydb.cursor()
    except Exception as e:
        print(e)


def add_new_table_transaction(insert_info, table_name):
    """Adds new transactions to the database in TABLE table_name"""

    cursor = get_db_cursor(DB_NAME)
    insert_query = INSERT_QUERIES[table_name]

    if len(insert_info) == 0:
        # insert_info is an empty list
        return
    elif len(insert_info) == 1:
        # insert_info has only one element
        try:
            cursor.execute(insert_query, insert_info[0])
            mydb.commit()
            cursor.close()
        except Exception as e:
            print(insert_info)
            print(e)
    else:
        # insert_info has more than one element
        try:
            cursor.executemany(insert_query, insert_info)
            mydb.commit()
            cursor.close()
        except Exception as e:
            print(len(insert_info))
            print(insert_info)
            print(e)


def retrieve_table_data(table_name, league):
    """"""

    try:
        cursor = get_db_cursor(DB_NAME)
        select_query = "SELECT * FROM {0} WHERE league = '{1}'".format(table_name, league)
        cursor.execute(select_query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)


def retrieve_seasonal_table_data(table_name, league, seasons):
    """"""

    if table_name == 'Ranking':
        select_query = "SELECT * FROM Ranking WHERE league = %s AND season IN {0};".format(tuple(seasons))
    elif table_name == 'Game':
        select_query = "SELECT * FROM Game WHERE league = %s AND season IN {0};".format(tuple(seasons))
    else:
        return

    try:
        cursor = get_db_cursor(DB_NAME)
        insert_value = (str(league), )
        cursor.execute(select_query, insert_value)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)


def recom_formations_dict_to_db(table_name, recom_dict, league):
    """Writes the recommendations about a league into a database

    Parameters
    ----------
    table_name : String
        asdf
    recom_dict : dictionary
        asdf
    league : String
        asdf

    Returns
    -------
    None
   """

    cursor = get_db_cursor(DB_NAME)
    select_query = "SELECT * FROM recom_formation WHERE league = '{0}';".format(league)
    cursor.execute(select_query)
    values = cursor.fetchall()

    if len(values) > 0:
        #
        delete_query = "DELETE FROM recom_formation WHERE league = '{0}';".format(league)
        cursor.execute(delete_query)
    #
    many_rows = []

    for first_key in recom_dict:
        for second_key in recom_dict[first_key]:

            row = [first_key, second_key, recom_dict[first_key][second_key], league]
            many_rows.append(row)
            add_new_table_transaction(many_rows, table_name)
            many_rows = []


def sql_data_to_game_objects(sql_match_data):
    """Sets the match data from the db into match objects

    Parameters
    ----------
    sql_match_data : list
        a 2-dimensional list with lists in it that hold information about a certain match
        the inside lists should be structured as follows:
        [id, home_team, home_formation, away_team, away_formation, home_score, away_score, season, league]

    Returns
    -------
    list
        a list is returned with match objects which holds information about a played match
   """
    # initialize a list which holds the Game objects
    match_list = []

    # loop over every match
    for match in sql_match_data:
        match_list.append(Game.Game(match[1], match[2], match[3], match[4], match[5], match[6], match[7]))

    # return the list with all the Game objects
    return match_list


def sql_data_to_ranking_objects(sql_ranking_data):
    """Sets the ranking data from the db into ranking objects

    Parameters
    ----------
    sql_ranking_data : list
        a 2-dimensional list with lists in it that hold information about a certain ranking in a season of a team
        the inside lists should be structured as follows:
        [id, team, season_rank, season, league]

    Returns
    -------
    list
        a list is returned with all the ranking objects which holds information about a ranking in a season
   """

    # initialize a list which holds the ranking objects
    ranking_list = []

    # loop over every ranking
    for rank in sql_ranking_data:
        ranking_list.append(Ranking.Ranking(rank[1], rank[2], rank[3], rank[4]))

    # return the list with all the Ranking objects
    return ranking_list
