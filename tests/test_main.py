import sys
import os

# Fix path issue: Ensure `main.py` is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app  # Now it should correctly import `main.py`
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_user():
    response = client.post("/api/users", json={"name": "John Doe", "email": "john@example.com", "password": "securepass"})
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_get_user():
    user = client.post("/api/users", json={"name": "Jane Doe", "email": "jane@example.com", "password": "securepass"}).json()
    user_id = user["user_id"]

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"


def test_create_house():
    user = client.post("/api/users", json={"name": "Alice", "email": "alice@example.com", "password": "securepass"}).json()
    user_id = user["user_id"]

    response = client.post("/api/houses", json={"user_id": user_id, "name": "My Smart Home", "address": "123 Main St"})
    assert response.status_code == 200
    assert "house_id" in response.json()


def test_create_room():
    user = client.post("/api/users", json={"name": "Bob", "email": "bob@example.com", "password": "securepass"}).json()
    user_id = user["user_id"]
    house = client.post("/api/houses", json={"user_id": user_id, "name": "Bob's House", "address": "456 Elm St"}).json()
    house_id = house["house_id"]

    response = client.post(f"/api/houses/{house_id}/rooms", json={"house_id": house_id, "name": "Living Room", "room_type": "General"})
    assert response.status_code == 200
    assert "room_id" in response.json()


def test_control_device():
    user = client.post("/api/users", json={"name": "Eve", "email": "eve@example.com", "password": "securepass"}).json()
    user_id = user["user_id"]
    house = client.post("/api/houses", json={"user_id": user_id, "name": "Eve's Home", "address": "101 Birch St"}).json()
    house_id = house["house_id"]
    room = client.post(f"/api/houses/{house_id}/rooms", json={"house_id": house_id, "name": "Kitchen", "room_type": "Cooking"}).json()
    room_id = room["room_id"]
    device = client.post(f"/api/rooms/{room_id}/devices", json={"room_id": room_id, "device_name": "Smart Thermostat", "device_type": "Thermostat", "status": "off"}).json()
    device_id = device["device_id"]

    response = client.post(f"/api/devices/{device_id}/control", json={"status": "on"})
    print(response.json())  # Debugging print to check API response in test logs
    assert response.status_code == 200
    assert response.json()["message"] == f"Device {device_id} turned on"
