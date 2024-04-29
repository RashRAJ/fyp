import pytest
import requests

@pytest.mark.parametrize('data', [
    {'username': 'test_user', 'email': 'test@example.com', 'password': 'password123'},
    {'username': '', 'email': 'test@example.com', 'password': 'password123'},  # Invalid data
])
def test_create_user(data):
    url = 'http://127.0.0.1:5000/api/user'

    # Send POST request with data
    response = requests.post(url, json=data)

    # Validate response status code
    assert response.status_code == 200

    # Validate response content type
    assert response.headers['Content-Type'] == 'application/json'

    # Validate response body (example)
    if 'error' in response.json():
        assert response.json()['error'] == 'Validation error'
    else:
        assert 'id' in response.json()
