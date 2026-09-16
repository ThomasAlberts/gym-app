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

## andere login faal testen