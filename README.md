## Player service 

## Project Overview
Player service is a Python Flask based microservice which serves the contents of `Player.csv` through a REST API. This service also integrates with Ollama using [Ollama-python](https://github.com/ollama/ollama-python) library.

## Key Features

- Serve the contents of `Player.csv` through a REST API
- In memory SQL database
- Integrate with Ollma using Ollama-python library

### API Endpoints
- `GET /v1/players` - returns the list of all players.
- `GET /v1/players/{player_id}` - returns a single player by ID.
- `GET /v1/players/{birth_country}` - returns a single player by ID.
- `GET /v1/chat/list-models` - returns the list of Ollama models available.
- `POST /v1/chat/` - Endpoint to chat with the available Ollama model

The database connected to this service is `in-memory H2 Database`.

### Project Structure

- `/player-service-app` folder contains sample requests for player service.
  - `app.py`: Main application file
  - `player_service.py`: Service layer implementations
  - `Player.csv`: Players data
  - `requirements.txt`: Python dependencies
- `/player-service-model` Traditional AI model trained using `Player.csv`. You are not expected to edit the model.

## Technology Technology Stack

- Python 3.9+
- Docker

### Prerequisites

Before you begin, ensure you have the following installed on your development machine:

1. **Python**
    - Verify installation: `python3 --version`

2. **Docker**
   - Download and install from [docker.com](https://www.docker.com/)
   - Verify installation: `docker --version`
3. **Git**
    - Download and install from [git-scm.com](https://git-scm.com/)
    - Verify installation: `git --version`

### Installation

#### Local setup
- Clone the repository
```shell
$ git clone https://github.com/Intuit-A4A/player-service-python.git
$ cd player-service-python
```
- Create & activate virtual env then install dependency
```shell
$ python3 -m venv env # use `python -m venv env` on Windows
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ cd player-service-app
$ pip install -r requirements.txt
```
- Run the app
```shell
$ python3 app.py
```

- If you want to run the `player-service-model`
```shell
$ cd player-service-model
$ docker build -t a4a_model .
$ docker run -d -p 5000:5000 a4a_model
```
This will run the `player-service-model` on port 5000.

### GenAI Integration with Ollama

1. Pull and run Ollama docker image and download `tinyllama` model

    - `docker pull ollama/ollama`
    - `docker run -it -v ~/ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`
    - `docker exec -it ollama ollama run tinyllama`

2. Test Ollama API server

    - `curl -v --location 'http://localhost:11434/api/generate' --header 'Content-Type: application/json' --data '{"model": "tinyllama","prompt": "why is the sky blue?", "stream": false}'`

### Run with Gitpod

This app can also be run in Gitpod. We recommend running using Gitpod to build and run this app on the browser. To run this app in Gitpod you will need -
- Github account
- Gitpod Classic account

Click on the below link to open this repository in Gitpod

   [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Intuit-A4A/player-service-python)

- Select the IDE of your choice. We recommend `VSCode IDE in browser`
- Standard Configuration
- Click `Continue`

![Screenshot 2024-10-18 at 10 49 59 AM](https://github.com/user-attachments/assets/cf97589f-e84b-48e3-b691-2248c437d884)  