import pytest
from routers.Firebase import app
from fastapi.testclient import TestClient

client = TestClient(app)

'''
General test to ensure the health of the API
'''
def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

''' 
Tests getting a user from the DB
'''
def test_get_user():
    response = client.get("/users/xxx")
    assert response.status_code == 200
    assert response.json() is not None

''' 
Tests getting a user that doesn't exist in the DB (Error expected)
'''
def test_get_user_not_found():
    response = client.get("/users/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

''' 
Tests adding a user to the DB
'''
def test_add_user():
    user_data = {
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "password123",
        "email": "john@example.com"
    }
    response = client.post("/users/", params=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User added to database"}

''' 
Tests adding an existing user to the DB (Error expected)
'''
def test_add_existing_user():
    user_data = {
        "full_name": "John Doe",
        "username": "john",
        "password": "password123",
        "email": "john@example.com"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 422

    error_detail = response.json().get("detail")
    assert error_detail is not None
    assert error_detail == [
        {
            "loc": ["query", "full_name"],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": ["query", "username"],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": ["query", "password"],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": ["query", "email"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]

''' 
Tests login to the DB with valid credentials
'''
def test_login_valid_credentials():
    username = 'xxx'
    password = 'xxxx'

    response = client.get(f"/login?username={username}&password={password}")
    assert response.status_code == 200
    assert response.json() == {'message': 'Login successful'}

''' 
Tests login to the DB with invalid credentials (Error expected)
'''
def test_login_invalid_credentials():
    username = 'invalid_user'
    password = 'invalid_password'

    response = client.get(f"/login?username={username}&password={password}")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid credentials'}

if __name__ == "__main__":
    pytest.main()
