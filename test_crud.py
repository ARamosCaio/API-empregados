import json
import pytest
import base64
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_employee(client):
    username = 'caio_ramos'
    password = 'jose123'

    auth_str = f'{username}:{password}'

    encoded_auth_str = base64.b64encode(auth_str.encode()).decode()

    auth_header = {'Authorization': f'Basic {encoded_auth_str}'}

    response = client.post(
        '/api/employees',
        json={"name": "John", "age": 30},
        headers=auth_header
        )

    assert response.status_code == 201
    assert response.json['message'] == 'Successfully added employee'

def test_get_employees(client):
    response = client.get('/api/employees')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_auth_required(client):
    response = client.post('/api/employees', json={"name": "John", "age": 30})
    assert response.status_code == 401
    assert response.json['message'] == 'Authentication Failed. Please provide a valid username and password'

    response = client.get('/api/employees')
    assert response.status_code == 200
    assert isinstance(response.json, list)
