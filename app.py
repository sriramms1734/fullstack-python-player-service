from flask import Flask, request, jsonify
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from player_service import PlayerService

app = Flask(__name__)

# Load CSV file in pandas dataframe and create SQLite database
df = pd.read_csv('Player.csv')
engine = create_engine('sqlite:///player.db', echo=True)
df.to_sql('players', con=engine, if_exists='replace', index=False)

# Get all players
@app.route('/v1/players', methods=['GET'])
def get_players():
    player_service = PlayerService()
    result = player_service.get_all_players()
    return result

@app.route('/v1/players/<string:player_id>')
def query_player_id(player_id):
    player_service = PlayerService()
    result = player_service.search_by_player(player_id)

    if len(result) == 0:
        return jsonify({"error": "No record found with player_id={}".format(player_id)})
    else:
        return jsonify(result)

@app.route('/v1/players/country/<string:birth_country>')
def query_player_country(birth_country):
    player_service = PlayerService()
    result = player_service.search_by_country(birth_country)

    if len(result) == 0:
        return jsonify({"error": "No record found with birth_country={}".format(birth_country)})
    else:
        return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
