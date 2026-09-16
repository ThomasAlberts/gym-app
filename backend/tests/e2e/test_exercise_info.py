# from starlette.testclient import TestClient
#
# from backend.tests.fixtures.auth_setup_tests import create_user, login_user
#
# ## user setup
# email = "test@test.com"
# password = "test123"
#
# def test_get_all_exercise_definitions(client: TestClient):
#     create_user(client, email, password)
#     login_response = login_user(client, email, password)
#     token = login_response.json()["access_token"]
#
#     exercise_definitions = client.get(
#         "/exercise_info/exercise_defintion/all",
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert exercise_definitions.status_code == 200
#     assert len(exercise_definitions.json()) == 5
#     assert len(exercise_definitions.json()[0]) == 6