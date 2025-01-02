import sqlite3
from sqlalchemy import create_engine

class PlayerService:
    def __init__(self):
        conn = sqlite3.connect("player.db")
        self.conn = conn
        self.cursor = conn.cursor()

    def get_all_players(self):
        query = "SELECT * FROM players"
        players = self.cursor.execute(query).fetchall()
        columns = [column[0] for column in self.cursor.description]
        response = []

        for player in players:
            response.append(dict(zip(columns,player)))

        return response

    def search_by_player(self, player_id):
        query = "SELECT * FROM players WHERE playerId='{}'".format(player_id)
        players = self.cursor.execute(query).fetchall()
        columns = [column[0] for column in self.cursor.description]
        response = []

        for player in players:
            response.append(dict(zip(columns,player)))

        return response
    
    # sriram
    def update_column(self, id, colName, value):
        query = "UPDATE players SET weight=? WHERE playerId = ?"

        self.cursor.execute(query,(value, id,))
        self.conn.commit()
    
    # sriram
    def search_fuzzy_text_player(self, text):
        text = "%{}%".format(text)  # Prepare the text for the LIKE clause
        query = "SELECT * FROM players WHERE (coalesce(playerId, '') || coalesce(nameGiven, '')) LIKE ?"
        players = self.cursor.execute(query, (text,)).fetchall()
        columns = [column[0] for column in self.cursor.description]
        response = []

        for player in players:
            response.append(dict(zip(columns,player)))

        return response
    
    # sriram
    def search_by_player_name(self, name):
        query = "SELECT * FROM players WHERE nameGiven LIKE '%{}%'".format(name)
        players = self.cursor.execute(query).fetchall()
        columns = [column[0] for column in self.cursor.description]
        response = []

        for player in players:
            response.append(dict(zip(columns,player)))

        return response

