# from starlette.testclient import TestClient
#
# from backend.tests.fixtures.auth_setup_tests import create_user, login_user
#
# ## user setup
# email = "test@test.com"
# password = "test123"
#
# def test_create_new_workout(client: TestClient):
#     create_user(client, email, password)
#     login_response = login_user(client, email, password)
#     token = login_response.json()["access_token"]
#
#     workout = client.post(
#         "/workout/create_new",
#         headers={"Authorization": f"Bearer {token}"},
#         json={
#             "exercises": [
#                 {
#                     "exercise_definition_id": 1,
#                     "exercise_sets": [
#                         {"reps": 5, "weight": 10, "workTime": 3, "restTime": 1}
#                     ],
#                     "notes": None,
#                 },
#                 {
#                     "exercise_definition_id": 3,
#                     "exercise_sets": [
#                         {"reps": 5, "weight": 20, "workTime": 30, "restTime": 20},
#                         {"reps": 5, "weight": 30, "workTime": 20, "restTime": 10},
#                     ],
#                     "notes": None,
#                 },
#             ],
#             "started_at": "2026-08-25T07:30:44.676Z",
#             "ended_at": "2026-08-25T08:30:44.676Z",
#         },
#     )
#     assert workout.status_code == 201, workout.text
#     assert workout.json()["user_id"] == 1
#     assert workout.json()["id"] == 1
#
#
# def test_unauthorized_create_new_workout(client: TestClient):
#     workout = client.post("/workout/create_new")
#     assert workout.status_code == 401
#
#
# def test_get_workout(client: TestClient):
#     create_user(client, email, password)
#     login_response = login_user(client, email, password)
#     token = login_response.json()["access_token"]
#
#     workout = client.post(
#         "/workout/create_new",
#         headers={"Authorization": f"Bearer {token}"},
#         json={
#             "exercises": [
#                 {
#                     "exercise_definition_id": 1,
#                     "exercise_sets": [
#                         {"reps": 5, "weight": 10, "workTime": 3, "restTime": 1}
#                     ],
#                     "notes": None,
#                 },
#                 {
#                     "exercise_definition_id": 3,
#                     "exercise_sets": [
#                         {"reps": 5, "weight": 20, "workTime": 30, "restTime": 20},
#                         {"reps": 5, "weight": 30, "workTime": 20, "restTime": 10},
#                     ],
#                     "notes": None,
#                 },
#             ],
#             "started_at": "2026-08-25T07:30:44.676Z",
#             "ended_at": "2026-08-25T08:30:44.676Z",
#         },
#     )
#     assert workout.status_code == 201, workout.text
#
#     workout = client.get(
#         f"/workout/{workout.json()["id"]}",
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert workout.status_code == 200, workout.text
#     assert workout.json()["user_id"] == 1
#     assert workout.json()["id"] == 1
