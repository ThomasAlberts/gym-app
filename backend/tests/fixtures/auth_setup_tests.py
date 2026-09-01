from starlette.testclient import TestClient

def create_user(client: TestClient, email: str, password: str):
    return client.post("/auth/register", json={  # ← Correct pad!
        "email": email,
        "password": password,
        "first_name": "Test",
        "last_name": "User"
    })

def login_user(client: TestClient, email, password):
    return client.post("/auth/login", json={
        "email": email,
        "password": password,
    })