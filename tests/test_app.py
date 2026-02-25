from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirects_to_index():
    # Arrange
    # (No special setup needed)
    # Act
    response = client.get("/", allow_redirects=False)
    # Assert
    assert response.status_code in (302, 307)
    assert "/static/index.html" in response.headers.get("location", "")

def test_get_activities_returns_all():
    # Arrange
    # (No special setup needed)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    email = "pytest_signup@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json().get("message", "")

def test_signup_already_signed_up():
    # Arrange
    email = "pytest_dupe@mergington.edu"
    client.post(f"/activities/Programming Class/signup?email={email}")
    # Act
    response = client.post(f"/activities/Programming Class/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

def test_signup_activity_not_found():
    # Arrange
    email = "pytest_notfound@mergington.edu"
    # Act
    response = client.post(f"/activities/Nonexistent/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
