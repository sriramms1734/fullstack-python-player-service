from flask import Flask, request, jsonify
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from player_service import PlayerService
import ollama

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
    return {"players": result}

@app.route('/v1/players/<string:player>')
def query_player_id(player):
    player_service = PlayerService()
    if player:
        result = player_service.search_by_player(player) 
    # sriram
    if len(result) == 0:
        result = player_service.search_by_country(player)
        if len(result) == 0:
            return {"error": "No record found with player={}".format(player)}
        else: 
            return {"player": result}
    else:
        return {"player": result}

# sriram
@app.route('/v1/players/fuzzy_search/<string:text>')
def query_player_fuzzy(text):
    player_service = PlayerService()
    if text:
        result = player_service.search_fuzzy_text_player(text) 

    if len(result) == 0:
        return {"error": "No record found with text={}".format(text)}
    else:
        return {"player": result}

@app.route('/v1/players/update_column/<string:id>', methods=['PATCH'])
def update_column(id):
    player_service = PlayerService()
    colName  = request.args.get('colName', None)
    if colName:
        value  = request.args.get('value', None)
        player_service.update_column(id,colName, value)
        return {"player": []} 
    else:
        return {}             
      

@app.route('/v1/chat/list-models')
def list_models():
    return jsonify(ollama.list())

@app.route('/v1/chat', methods=['POST'])
def chat():
    # Process the data as needed
    response = ollama.chat(model='tinyllama', messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ])
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
