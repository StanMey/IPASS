import mysql_connect as mc


def get_competitions_choice():
    """Gets all the different leagues that exist in the recommendation table"""

    cursor = mc.get_db_cursor(mc.DB_NAME)
    select_query = "SELECT DISTINCT(league) FROM recom_formation;"
    cursor.execute(select_query)
    leagues = cursor.fetchall()

    # initialize a dictionary for storing the different leagues
    result_dict = {
        "values": []
    }
    # save all the different leagues in the dictionary
    for league in leagues:
        result_dict["values"].append(league[0])
    return result_dict


def get_formations_options(league):
    """Gets all the different formations that exist in a certain league"""

    cursor = mc.get_db_cursor(mc.DB_NAME)
    select_query = """SELECT DISTINCT(formation_2) FROM recom_formation
                        WHERE league = %s;"""
    cursor.execute(select_query, (league, ))
    formations = cursor.fetchall()

    # initializes a dictionary for storing the different formations
    result_dict = {
        "values": []
    }
    # save all the different formations in the dictionary
    for formation in formations:
        result_dict["values"].append(formation[0])
    return result_dict


def get_recommended_formations(opponent_formation, league, limit):
    """Gets the recommended formations from the db for a certain formation in a certain league"""

    cursor = mc.get_db_cursor(mc.DB_NAME)
    select_query = """SELECT formation_1 FROM recom_formation
                        WHERE formation_2 = %s
                        AND league = %s
                        ORDER BY formation_points DESC limit %s"""
    insert_value = (opponent_formation, league, limit)
    cursor.execute(select_query, insert_value)
    formations = cursor.fetchall()

    # initializes a dictionary for storing the recom formations
    result_dict = {
        "recoms": []
    }
    # save all the formations in the dictionary
    for formation in formations:
        result_dict["recoms"].append(formation[0])
    return result_dict
