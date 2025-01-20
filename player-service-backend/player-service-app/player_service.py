import sqlite3
from sqlalchemy import create_engine

class PlayerService:
    def __init__(self):
        conn = sqlite3.connect("player.db")
        self.conn = conn
        self.cursor = conn.cursor()

    def get_all_players(self, isAdmin):
        admin = isAdmin.lower()
        if admin in ['false', 'none']:
            query = "SELECT nameFirst FROM players"
        else: 
            query = "SELECT nameFirst, nameLast FROM players"  
  
        players = self.cursor.execute(query).fetchall()
        columns = [column[0] for column in self.cursor.description]
        response = []

        for player in players:
            response.append(dict(zip(columns,player)))

        return response
    
    def search_by_player_country(self, player_country, limit, offset):
        query = "SELECT * FROM players where birthCountry like '%{}%' LIMIT {} OFFSET {}".format(player_country, limit, offset)
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

