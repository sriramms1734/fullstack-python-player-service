import pytest
from app import app
from unittest.mock import MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_player_service(monkeypatch):
    mock_player_service = MagicMock()
    monkeypatch.setattr("app.PlayerService", lambda: mock_player_service)
    return mock_player_service

@pytest.fixture
def mock_ollama_chat(monkeypatch):
    mock_chat = MagicMock()
    monkeypatch.setattr("app.ollama.chat", mock_chat)
    return mock_chat

def test_get_all_players_as_admin(mock_player_service, client):
    mock_player_service.get_all_players.return_value = [
        {"nameFirst": "Sriram", "nameLast": "Mano"},
        {"nameFirst": "Papa", "nameLast": "John"}
    ]

    response = client.get('/v1/players?isAdmin=true')

    assert response.status_code == 200
    assert response.json == {
        "players": [
            {"nameFirst": "Sriram", "nameLast": "Mano"},
            {"nameFirst": "Papa", "nameLast": "John"}
        ]
    }
    mock_player_service.get_all_players.assert_called_once_with('true')

def test_get_all_players_as_non_admin(mock_player_service, client):
    mock_player_service.get_all_players.return_value = [
        {"nameFirst": "Sriram"},
        {"nameFirst": "Papa"}
    ]

    response = client.get('/v1/players?isAdmin=false')

    assert response.status_code == 200
    assert response.json == {
        "players": [
            {"nameFirst": "Sriram"},
            {"nameFirst": "Papa"}
        ]
    }
    mock_player_service.get_all_players.assert_called_once_with('false')

def test_get_all_players_invalid_isAdmin(mock_player_service, client):
    response = client.get('/v1/players?isAdmin=tree')

    assert response.status_code == 400
    assert response.json == []

    mock_player_service.get_all_players.assert_not_called()

def test_generate_nickname_success(client, mock_player_service, mock_ollama_chat):
    mock_player_service.search_by_player_country.return_value = [
        {"nameFirst": "Sriram", "nameLast": "Mano"}
    ]
    
    mock_ollama_chat.return_value = {
        "message": {"content": "The Maestro"}
    }

    response = client.get('/v1/players/nickname/India')

    assert response.status_code == 200
    assert response.json == {
        "country": "India",
        "player": "Sriram Mano",
        "nickname": "The Maestro"
    }

    mock_player_service.search_by_player_country.assert_called_once_with("India")
    mock_ollama_chat.assert_called_once_with(
        model="tinyllama",
        messages=[
            {"role": "system", "content": "You are a creative assistant. Generate a fun and unique nickname using the given first and last name."},
            {"role": "user", "content": "Generate a nickname for Sriram Mano."},
        ]
    )

def test_generate_nickname_no_players(client, mock_player_service):
    mock_player_service.search_by_player_country.return_value = []

    response = client.get('/v1/players/nickname/Mars')

    assert response.status_code == 404
    assert response.json == {"error": "No players found for country=Mars"}

    mock_player_service.search_by_player_country.assert_called_once_with("Mars")

def test_generate_nickname_ollama_failure(client, mock_player_service, mock_ollama_chat):
    mock_player_service.search_by_player_country.return_value = [
        {"nameFirst": "Papa", "nameLast": "John"}
    ]
    
    mock_ollama_chat.return_value = {}

    response = client.get('/v1/players/nickname/USA')

    assert response.status_code == 500
    assert response.json == {"error": "Failed to generate a nickname"}

    mock_player_service.search_by_player_country.assert_called_once_with("USA")
    mock_ollama_chat.assert_called_once_with(
        model="tinyllama",
        messages=[
            {"role": "system", "content": "You are a creative assistant. Generate a fun and unique nickname using the given first and last name."},
            {"role": "user", "content": "Generate a nickname for Papa John."},
        ]
    )

def test_generate_nickname_exception(client, mock_player_service):
    mock_player_service.search_by_player_country.side_effect = Exception("Database error")

    response = client.get('/v1/players/nickname/USA')

    assert response.status_code == 500
    assert response.json == {"error": "Database error"}

    mock_player_service.search_by_player_country.assert_called_once_with("USA")
