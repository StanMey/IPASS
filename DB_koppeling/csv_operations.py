import csv
from mysql_connect import *


def insert_data_from_csv_to_db(file_name, table_name, iter_numb):
    """inserts the data from a csv file into a table by iter_numb rows at the same time"""

    with open(file_name, mode='r') as file:
        csv_reader = csv.reader(file, delimiter=',')

        # initialize a boolean to skip the first row
        is_first_row = True
        many_rows = []

        # loop over every row in the file
        for row in csv_reader:
            if is_first_row:
                # first row
                is_first_row = False
                continue
            else:
                # not first row
                if len(many_rows) % iter_numb == 0:
                    add_new_table_transaction(many_rows, table_name)
                    many_rows = []
                many_rows.append(row)
        add_new_table_transaction(many_rows, table_name)


def insert_data_from_db_to_csv(file_name, table_name, league):
    """Selects the data from a certain table and prints it into a csv file"""

    with open(file_name, mode='w', newline="") as file:
        item_writer = csv.writer(file, delimiter=',')

        csv_cursor = get_db_cursor(DB_NAME)
        select_query = """SELECT * FROM {0} WHERE league = '{1}'""".format(table_name, league)
        csv_cursor.execute(select_query)

        for item in csv_cursor:
            item_writer.writerow(item)
        csv_cursor.close()


def match_data_to_csv(matches_list, file_name):
    """Gets a list with dictionaries, writes them into a csv file
    (home_team, home_formation, away_team, away_formation, home_score, away_score, season, league)"""

    with open(file_name, mode='w', newline="") as file:
        fieldnames = ['home_team', 'home_formation', 'away_team', 'away_formation',
                      'home_score', 'away_score', 'season', 'league']
        match_writer = csv.DictWriter(file, fieldnames=fieldnames)

        match_writer.writeheader()
        for match in matches_list:
            match_writer.writerow(match)
