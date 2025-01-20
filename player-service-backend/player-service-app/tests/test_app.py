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
        {"nameFirst": "First", "nameLast": "Last"},
        {"nameFirst": "First-2", "nameLast": "Last"}
    ]

    # Call the endpoint
    response = client.get('/v1/players?isAdmin=true')

    assert response.status_code == 200
    assert response.json == {
        "players": [
            {"nameFirst": "First", "nameLast": "Last"},
            {"nameFirst": "First-2", "nameLast": "Last"}
        ]
    }
    mock_player_service.get_all_players.assert_called_once_with('true')

def test_get_all_players_as_non_admin(mock_player_service, client):
    # Mock database response
    mock_player_service.get_all_players.return_value = [
        {"nameFirst": "First"},
        {"nameFirst": "First-2"}
    ]

    response = client.get('/v1/players?isAdmin=false')

    assert response.status_code == 200
    assert response.json == {
        "players": [
        {"nameFirst": "First"},
        {"nameFirst": "First-2"}
        ]
    }
    # Ensure the service method was called with the correct argument
    mock_player_service.get_all_players.assert_called_once_with('false')

def test_get_all_players_invalid_isAdmin(mock_player_service, client):
    # Call the endpoint
    response = client.get('/v1/players?isAdmin=tree')

    # Validate the response
    assert response.status_code == 400
    assert response.json == []

    # Ensure the service method was not called
    mock_player_service.get_all_players.assert_not_called()

def test_generate_nickname_success(client, mock_player_service, mock_ollama_chat):
    mock_player_service.search_by_player_country.return_value = [
        {"nameFirst": "Sri", "nameLast": "ram"}
    ]
    
    # Mock Ollama chat response
    mock_ollama_chat.return_value = {
        "message": {"content": "Sri D"}
    }

    response = client.get('/v1/players/nickname/USA')

    assert response.status_code == 200
    assert response.json == {
        "country": "USA",
        "player": "Sri ram",
        "nickname": "Sri D"
    }

    mock_player_service.search_by_player_country.assert_called_once_with("USA", 1, 0)
    mock_ollama_chat.assert_called_once_with(
        model="tinyllama",
        messages=[
            {"role": "system", "content": "You are creative. Generate a nickname using the given last name, first name"},
            {"role": "user", "content": "Generate a nickname for ram, Sri."},
        ]
    )

def test_generate_nickname_no_players(client, mock_player_service):
    # Mock PlayerService response
    mock_player_service.search_by_player_country.return_value = []

    response = client.get('/v1/players/nickname/Mars')

    assert response.status_code == 404
    assert response.json == {"error": "No players found for country=Mars"}

    mock_player_service.search_by_player_country.assert_called_once_with("Mars", 1, 0)

def test_generate_nickname_ollama_failure(client, mock_player_service, mock_ollama_chat):
    mock_player_service.search_by_player_country.return_value = [
        {"nameFirst": "Sri", "nameLast": "ram"}
    ]
    
    # Mock Ollama chat response
    mock_ollama_chat.return_value = {}

    # Call the endpoint
    response = client.get('/v1/players/nickname/USA')

    # Validate the response
    assert response.status_code == 500
    assert response.json == {"error": "Failed to generate nickname"}

    mock_player_service.search_by_player_country.assert_called_once_with("USA", 1, 0)
    mock_ollama_chat.assert_called_once_with(
        model="tinyllama",
        messages=[
            {"role": "system", "content": "You are creative. Generate a nickname using the given last name, first name"},
            {"role": "user", "content": "Generate a nickname for ram, Sri."},
        ]
    )

def test_generate_nickname_exception(client, mock_player_service):

    mock_player_service.search_by_player_country.side_effect = Exception("Database error")

    response = client.get('/v1/players/nickname/USA')

    assert response.status_code == 500
    assert response.json == {"error": "Database error"}

    # Ensure the service was called correctly
    mock_player_service.search_by_player_country.assert_called_once_with("USA",1, 0)