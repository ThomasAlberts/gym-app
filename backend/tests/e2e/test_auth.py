from starlette.testclient import TestClient

from backend.tests.fixtures.auth_setup_tests import create_user, login_user

email="test@test.com"
password="test123"

def test_register_user_success(client):
    res = create_user(client, email, password)
    assert res.status_code == 201
    assert res.json()["id"] is not None
    assert res.json()["email"] == "test@test.com"
    assert "password" not in res.json()


## andere register testen

def test_login_user_success(client):
    create_user(client, email, password)
    res = login_user(client, email, password)
    assert res.status_code == 200
    assert res.json()["user"]["id"] == 1
    assert res.json()["user"]["email"] == email
    assert res.json()["user"]["role"] == "user"
    assert "access_token" in res.json()


## andere login faal testen