import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Math Olympiad"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in response.json()["message"]
    # Verificar que el participante fue agregado
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_for_activity_already_signed_up():
    email = "emma@mergington.edu"  # Ya está en Programming Class
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    email = "someone@mergington.edu"
    activity = "Nonexistent"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant():
    # Primero registrar
    email = "delete@mergington.edu"
    activity = "Drama Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Ahora eliminar
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert email in response.json()["message"]
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
