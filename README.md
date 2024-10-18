# Player Servuce

Player service is a spring boot based microservice which serves the contents of Player.csv through a REST API. The app contains `player-service-model` which is a traditional AI model trained with `Player.csv` data. 

## APIs implemented:
- GET `/v1/players` - returns the list of all players.
- GET `/v1/players/{player_id}` - returns a single player by ID.
- GET `/v1/players/country/{birth_country}` - returns the list of all players by `birth_country`

## Technology
- Python 3.9+
- Flask
- Docker

## Installation

### Local setup
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

### Run with Gitpod


This app can also be run in Gitpod. We recommend running using Gitpod to build and run this app on the browser. To run this app in Gitpod you will need - 
- Github account
- Gitpod Classic account

We recommend creating a Gitpod **Classic** account 

- Click on the below link to open this repository in Gitpod

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Intuit-A4A/player-service-python)
