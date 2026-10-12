import pytest
from app import app, get_db, init_db

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.DATABASE",
        str(tmp_path / "test_hospital.db")
    )

    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CarePoint" in response.data
    assert b"Meet our doctors" in response.data

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_appointments_page(client):
    response = client.get("/appointments")
    assert response.status_code == 200
    assert b"Appointment requests" in response.data

def test_successful_appointment_booking(client):
    response = client.post("/book", data={
        "patient_name": "Test Patient",
        "email": "test@example.com",
        "phone": "9876543210",
        "doctor_id": "1",
        "appointment_date": "2099-12-31",
        "reason": "Routine checkup"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Appointment request submitted successfully!" in response.data
    assert b"Test Patient" in response.data

def test_invalid_email_is_rejected(client):
    response = client.post("/book", data={
        "patient_name": "Test Patient",
        "email": "invalid-email",
        "phone": "9876543210",
        "doctor_id": "1",
        "appointment_date": "2099-12-31",
        "reason": "Routine checkup"
    }, follow_redirects=True)

    assert b"Please enter a valid email address." in response.data

def test_invalid_doctor_is_rejected(client):
    response = client.post("/book", data={
        "patient_name": "Test Patient",
        "email": "test@example.com",
        "phone": "9876543210",
        "doctor_id": "999",
        "appointment_date": "2099-12-31",
        "reason": "Routine checkup"
    }, follow_redirects=True)

    assert b"Please select a valid doctor." in response.data
