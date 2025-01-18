from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine
from player_service import PlayerService
import ollama
import requests

app = Flask(__name__)

# Load CSV file in pandas dataframe and create SQLite database
df = pd.read_csv('Player.csv')
engine = create_engine('sqlite:///player.db', echo=True)
df.to_sql('players', con=engine, if_exists='replace', index=False)

# Get all players
@app.route('/v1/players', methods=['GET'])
def get_players():
    player_service = PlayerService()
    isAdmin = request.args.get('isAdmin')
    if isAdmin not in ['true', 'false', 'none']:
        return [], 400
    result = player_service.get_all_players(isAdmin)
    return {"players": result}

@app.route('/v1/players/<string:player_id>')
def query_player_id(player_id):
    player_service = PlayerService()
    result = player_service.search_by_player(player_id)
    if len(result) == 0:
        return {"error": "No record found with player_id={}".format(player_id)}
    else:
        return {"player": result}

@app.route('/v1/players/player_country/<string:player_country>')
def query_player_country(player_country):
    player_service = PlayerService()
    result = player_service.search_by_player_country(player_country)
    if len(result) == 0:
        return {"error": "No record found with player_country={}".format(player_country)}
    else:
        return {"player": result}    

@app.route('/v1/chat/list-models')
def list_models():
    return jsonify(ollama.list())

@app.route('/v1/chat', methods=['POST'])
def chat():
    # Process the data as needed
    body = request.get_json()
    if body is None: 
        messages = [
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ] 
    else: 
        messages = [body]
    response = ollama.chat(model='tinyllama', messages=messages)
    return jsonify(response), 200

@app.route('/v1/team/generate', methods=['POST'])
def generate_team():
    # Process the data as needed
    try:
        target_url = f"http://localhost:{5000}/team/generate"
        data = request.get_json()
        response = requests.post(target_url, json=data)
        # Return the response from the target server
        return jsonify(response.json()), response.status_code
    except Exception as e:
        # Handle errors and return an appropriate response
        return jsonify({"error": str(e)}), 500 
    
    
@app.route('/v1/players/nickname/<string:player_country>', methods=['GET'])
def generate_nickname(player_country):
    """
    Generate a nickname for a player based on their country using their first and last name.
    """
    try:
        # Query the database to find players from the specified country
        player_service = PlayerService()
        result = player_service.search_by_player_country(player_country)
        
        if len(result)==0:
            return jsonify({"error": f"No players found for country={player_country}"}), 404
        
        # Extract the first and last name
        name_first, name_last = result[0]["nameFirst"], result[0]["nameLast"]
        
        # Use Ollama to generate a nickname
        system_prompt = (
            "You are a creative assistant. Generate a fun and unique nickname "
            "using the given first and last name."
        )
        user_prompt = f"Generate a nickname for {name_first} {name_last}."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        response = ollama.chat(model='tinyllama', messages=messages)
        if response.get("message", {}).get("content"):
            return jsonify({
                "country": player_country,
                "player": f"{name_first} {name_last}",
                "nickname": response.get("message", {}).get("content")
            }), 200
        else:
            return jsonify({"error": "Failed to generate a nickname"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
