# ⚾ Player Service
<p align="center">
Player Service is a lightweight and efficient microservice built using Flask framework. It serves as a simple way to access player information stored in a `Player.csv` file and makes this data available through a RESTful APIs.
</p>

<p align="center">
<a href="#introduction">Introduction</a> &nbsp;&bull;&nbsp;
<a href="#%EF%B8%8F-setup-instructions">Installation</a> &nbsp;&bull;&nbsp;
<a href="#documentation">Documentation</a>
</p>

# Introduction
This <b>Player Service</b> app provides simple APIs that serve the contents of `Player.csv`. It contains information regarding Baseball players.
The contest of `Player.csv` is integrated in in-memory database.

You can:

- `GET /v1/players` - Fetch a list of all players
- `GET /v1/players/{player_id}` - Fetch a Player object based on `playerId`

In addition to serving the contents of `Player.csv`. Player service integrates with Ollama, which allows us to run LLMs locally. This app runs [`tinyllama`](https://ollama.com/library/tinyllama) model.
- `GET /v1/chat/list-models` -  List available LLM models
- `POST /v1/chat` - Chat with `tinyllama` model

## Technology Stack

- Python3.9+
- sqllite3
- Docker
- [Ollama Python SDK](https://github.com/ollama/ollama-python)

## Project Structure

- `/player-service-app`: Source code
    - `app.py` - main application file
    - `player_service.py` service layer implementation
- `/player-service-model` folder contains a dummy AI model for `Player.csv` data.

## Schema for PLAYERS table
The database connected to this service is `in-memory sqllite Database`. On application start-up, `PLAYERS` table is created.

Here is the schema for `players` table -

- `playerID`: A unique identifier for each player.
- `birthYear`,`birthMonth`, `birthDay`: The player’s birth date.
- `birthCountry`, `birthState`, `birthCity`: The location of the player’s birth.
- `deathYear`, `deathMonth`, `deathDay`, `deathCountry`, `deathState`, `deathCity`: The location and date of the player’s death. If this is empty, the player is still alive.
- `nameFirst`, `nameLast`, `nameGiven`: The player’s first name, last name, and given name.
- `weight`: The player’s weight in pounds.
- `height`: The player’s height in inches.
- `bats`: Indicates which hand the player bats with (R for right).
- `throws`: Indicates which hand the player throws with.
- `debut`: The date of the player’s debut game.
- `finalGame`: The date of the player’s final game.
- `retroID` and `bbrefID`: Unique IDs used by baseball reference systems (likely for linking to external player databases).

## 🛠️ Setup Instructions
### Pre requisites
Before you begin, ensure you have the following installed on your development machine:

1. **Python**
    - Verify installation: `python3 --version`

2. **Docker**
    - Download and install from [docker.com](https://www.docker.com/)
    - Verify installation: `docker --version`

3. **Docker**
    - Download and install from [docker.com](https://www.docker.com/)
    - Verify installation: `docker --version`


### Application setup

1. Clone this repository or Download the code as zip


2. [OPTIONAL] Create & activate virtual env then install dependency
    ```shell
    $ python3 -m venv env # use `python -m venv env` on Windows
    $ source env/bin/activate  # use `env\Scripts\activate` on Windows
    ```
3. Install App dependencies
    ```shell
    cd player-service-app
    $ pip install -r requirements.txt
    ```

4. Start the server:
   ```
   python3 app.py
   ```
This will start your flask app on port 8000.

5. Open your browser and visit `http://localhost:8000` or `http://127.0.0.1:8000/` to test the application.


6. Test `GET /v1/players/{id}`
    ```shell
    curl --location 'http://localhost:8080/v1/players/milleri01'
    ```

### Ollama setup 🦙

Player service integrates with Ollama, which allows us to run LLMs locally. This app runs [`tinyllama`](https://ollama.com/library/tinyllama) model.

1. Pull and run Ollama docker image and download `tinyllama` model
- Pull Ollama docker image
    ```shell
    docker pull ollama/ollama
    ```
- Run Ollama docker image on port 11434
    ```shell
    docker run -it -v ~/ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    ```
- Download and run `tinyllama` model
    ```shell
    docker exec -it ollama ollama run tinyllama
    ```

2. Test Ollama API server
    ```curl
    curl -v --location 'http://localhost:11434/api/generate' --header 'Content-Type: application/json' --data '{"model": "tinyllama","prompt": "why is the sky blue?", "stream": false}'
    ```

[Ollama API documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)

3. Start Player Service app
```shell
python3 app.py
```
Call `GET /v1/chat/list-models`
```curl
curl --location 'http://localhost:8000/v1/chat/list-models'
```

Response
```json
[
    {
        "name": "tinyllama:latest",
        "model": "tinyllama:latest",
        "digest": "2644915ede352ea7bdfaff0bfac0be74c719d5d5202acb63a6fb095b52f394a4",
        "size": 637700138,
        "modelName": "tinyllama",
        "modelVersion": "latest",
        "modified_at": "2024-10-04T18:12:54.714314005Z",
        "expires_at": null,
        "details": {
            "format": "gguf",
            "family": "llama",
            "families": [
                "llama"
            ],
            "parameter_size": "1B",
            "quantization_level": "Q4_0"
        }
    }
]
```

## Documentation

Here is a list of documentation that can help you understand this app.
- [Ollama](https://github.com/ollama/ollama)
- [Ollama API doc](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama Python SDK](https://github.com/ollama/ollama-python)