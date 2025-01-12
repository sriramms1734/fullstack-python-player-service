import sqlite3
from sqlalchemy import create_engine

class PlayerService:
    def __init__(self):
        conn = sqlite3.connect("player.db")
        self.conn = conn
        self.cursor = conn.cursor()

    def get_all_players(self, limit=10, offset=10):
        if limit is None: 
            limit = 10
        if offset is None:
            offset = 10;    
        print(f"{limit} {offset}")
        query = "SELECT * FROM players LIMIT {limit} OFFSET {offset}".format(limit=limit, offset=offset)
        print(query)
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
    def search_by_country(self, name):
        query = "SELECT * FROM players WHERE birthCountry LIKE '%{}%'".format(name)
        players = self.cursor.execute(query).fetchall()
        columns = [column[0] for column in self.cursor.description]
        response = []

        for player in players:
            response.append(dict(zip(columns,player)))

        return response

