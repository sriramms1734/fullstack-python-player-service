# ⚾ Player Service
<p align="center">
Player Service is a lightweight and efficient microservice built using Spring Boot framework. It serves as a simple way to access player information stored in a `Player.csv` file and makes this data available through a RESTful APIs.
</p>

<p align="center">
<a href="#introduction">Introduction</a> &nbsp;&bull;&nbsp;
<a href="#%EF%B8%8F-setup-instructions">Installation</a> &nbsp;&bull;&nbsp;
<a href="#documentation">Documentation</a>
</p>

# Introduction
This <b>Player Service</b> app provides simple APIs that serve the contents of `Player.csv`. It contains information regarding Baseball players.
The contest of `Player.csv` is integrated in in-memory H2 database.

You can:

- `GET /v1/players` - Fetch a list of all players
- `GET /v1/players/{id}` - Fetch a Player object based on `playerId`

In addition to serving the contents of `Player.csv`. Player service integrates with Ollama, which allows us to run LLMs locally. This app runs [`tinyllama`](https://ollama.com/library/tinyllama) model.
- `GET /v1/chat/list-models` -  List available LLM models
- `POST /v1/chat` - Chat with `tinyllama` model

## Technology Stack

- Java 17
- Maven
- Spring Boot 3.3.4 (with Spring Web MVC, Spring Data JPA)
- H2 Database
- Docker
- [Ollama4j SDK](https://ollama4j.github.io/ollama4j/intro)

## Project Structure

- `/collection` folder contains sample requests for player service.
- `/src`: Source code
    - `/config`: Configuration for Ollama4j library
    - `/controller`: API controllers
    - `/model`: Data models
    - `/repository`: Data repositories
    - `/service`: Service layer implementations
- `/player-service-model` folder contains a dummy AI model for `Player.csv` data. Additional information for this model can be found [here](player-service-model/README.md).

## Schema for PLAYERS table
The database connected to this service is `in-memory H2 Database`. On application start-up, `PLAYERS` table is created.

Here is the schema for `PLAYERS` table -

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

1. **Java 17**
    - Verify installation: `java --version`

2. **Maven**
    - Download and install from [maven.apache.org](https://maven.apache.org/install.html)
    - Verify installation: `mvn --version`

3. **Docker**
    - Download and install from [docker.com](https://www.docker.com/)
    - Verify installation: `docker --version`


### Application setup

1. Clone this repository or Download the code as zip

3. Install dependencies:
   ```
   cd player-service-java
   mvn clean install -DskipTests
   ```

4. Start the server:
   ```
   mvn spring-boot:run
   ```

5. Open your browser and visit `http://localhost:8080` or `http://127.0.0.1:8080/` to test the application.

6. Test `GET /v1/players/{id}`
```shell
curl --location 'http://localhost:8080/v1/players/milleri01'
```
Response
```json
{
    "playerId": "milleri01",
    "birthYear": "1948",
    "birthMonth": "4",
    "birthDay": "19",
    "birthCountry": "USA",
    "birthState": "MI",
    "birthCity": "Grand Rapids",
    "deathYear": null,
    "deathMonth": null,
    "deathDay": null,
    "deathCountry": null,
    "deathState": null,
    "deathCity": null,
    "firstName": "Rick",
    "lastName": "Miller",
    "givenName": "Richard Alan",
    "weight": "175",
    "height": "72",
    "bats": "L",
    "throwStats": "L",
    "debut": "1971-09-04",
    "finalGame": "1985-10-04",
    "retroId": "millr001",
    "bbrefId": "milleri01"
}
```

7. Run tests:
```
mvn clean install
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

3. Run Player Service app
```shell
mvn spring-boot:run
```
Call `GET /v1/chat/list-models`
```curl
curl --location 'http://localhost:8080/v1/chat/list-models'
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
- [Ollama4J SDK](https://ollama4j.github.io/ollama4j/intro)