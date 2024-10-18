import sqlite3
from sqlalchemy import create_engine

class PlayerService:
    def __init__(self):
        conn = sqlite3.connect("player.db")
        self.conn = conn
        self.cursor = conn.cursor()

    def get_all_players(self):

        query = "SELECT * FROM players"
        result = self.cursor.execute(query).fetchall()

        return result

    def search_by_player(self, player_id):

        query = "SELECT * FROM players WHERE playerID='{}'".format(player_id)
        result = self.cursor.execute(query).fetchall()

        return result


    def search_by_country(self, birth_country):

        query = "SELECT * FROM players WHERE birthCountry='{}'".format(birth_country)
        result = self.cursor.execute(query).fetchall()

        return result

