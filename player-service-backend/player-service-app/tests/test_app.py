import pytest
from flask import Flask
from app import app  # Import the Flask app from your application module
from pytest_mock import mocker

@pytest.fixture
def client():
    """Test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_players(client):
    """Test the GET /v1/players route."""
    response = client.get('/v1/players?limit=10&offset=0')
    assert response.status_code == 200
    data = response.get_json()
    assert "players" in data

def test_query_player_id(client):
    """Test the GET /v1/players/<string:player> route."""
    player_id = "test_player"
    response = client.get(f'/v1/players/{player_id}')
    assert response.status_code == 200
    data = response.get_json()
    if "error" in data:
        assert data["error"] == f"No record found with player={player_id}"
    else:
        assert "player" in data

def test_query_player_fuzzy(client):
    """Test the GET /v1/players/fuzzy_search/<string:text> route."""
    fuzzy_text = "test_text"
    response = client.get(f'/v1/players/fuzzy_search/{fuzzy_text}')
    assert response.status_code == 200
    data = response.get_json()
    if "error" in data:
        assert data["error"] == f"No record found with text={fuzzy_text}"
    else:
        assert "player" in data

def test_update_column(client):
    """Test the PATCH /v1/players/update_column/<string:id> route."""
    player_id = "test_id"
    response = client.patch(
        f'/v1/players/update_column/{player_id}?colName=test_column&value=test_value'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "player" in data

def test_list_models(client, mocker):
    """Test the GET /v1/chat/list-models route."""
    mocker.patch('app.ollama.list', return_value=['model1', 'model2'])
    response = client.get('/v1/chat/list-models')
    assert response.status_code == 200
    data = response.get_json()
    assert "response" in data
    assert "model1" in data["response"]

def test_chat(client, mocker):
    """Test the POST /v1/chat route."""
    mocker.patch(
        'requests.post',
        return_value=mocker.Mock(
            json=lambda: {"result": "Chat response"},
            status_code=200
        )
    )
    payload = {"content": "Hello"}
    response = client.post('/v1/chat', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert data["result"] == "Chat response"

def test_team_generate(client, mocker):
    """Test the POST /team/generate route."""
    mocker.patch(
        'requests.post',
        return_value=mocker.Mock(
            json=lambda: {"team": "Generated Team"},
            status_code=200
        )
    )
    payload = {"input": "team data"}
    response = client.post('/team/generate', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "team" in data
    assert data["team"] == "Generated Team"
