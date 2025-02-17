from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import Dict, List

app = FastAPI()

users: Dict[str, dict] = {}
houses: Dict[str, dict] = {}
rooms: Dict[str, dict] = {}
devices: Dict[str, dict] = {}

class User(BaseModel):
    name: str
    email: str
    password: str

class House(BaseModel):
    user_id: str
    name: str
    address: str

class Room(BaseModel):
    house_id: str
    name: str
    room_type: str

class Device(BaseModel):
    room_id: str
    device_name: str
    device_type: str
    status: str = "off"


@app.post("/api/users")
def create_user(user: User):
    user_id = str(uuid4())
    users[user_id] = user.dict()
    return {"user_id": user_id, **users[user_id]}


@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, **users[user_id]}


@app.post("/api/houses")
def create_house(house: House):
    if house.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    house_id = str(uuid4())
    houses[house_id] = house.dict()
    return {"house_id": house_id, **houses[house_id]}


@app.get("/api/houses/{house_id}")
def get_house(house_id: str):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    return {"house_id": house_id, **houses[house_id]}


@app.post("/api/houses/{house_id}/rooms")
def add_room(house_id: str, room: Room):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    room_id = str(uuid4())
    rooms[room_id] = room.dict()
    return {"room_id": room_id, **rooms[room_id]}


@app.get("/api/houses/{house_id}/rooms")
def get_rooms(house_id: str):
    return {"rooms": [room for room in rooms.values() if room["house_id"] == house_id]}


@app.post("/api/rooms/{room_id}/devices")
def add_device(room_id: str, device: Device):
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    device_id = str(uuid4())
    devices[device_id] = device.dict()
    return {"device_id": device_id, **devices[device_id]}


@app.get("/api/rooms/{room_id}/devices")
def get_devices(room_id: str):
    return {"devices": [device for device in devices.values() if device["room_id"] == room_id]}


@app.post("/api/devices/{device_id}/control")
def control_device(device_id: str, status: str):
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    devices[device_id]["status"] = status
    return {"message": f"Device {device_id} turned {status}"}
