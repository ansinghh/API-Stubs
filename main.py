from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import Dict

app = FastAPI()

# Data Storage (Mock)
users: Dict[str, dict] = {}
houses: Dict[str, dict] = {}
rooms: Dict[str, dict] = {}
devices: Dict[str, dict] = {}

# User Model
class User(BaseModel):
    name: str
    email: str
    password: str

# House Model
class House(BaseModel):
    user_id: str
    name: str
    address: str

# Room Model
class Room(BaseModel):
    house_id: str
    name: str
    room_type: str

# Device Model
class Device(BaseModel):
    room_id: str
    device_name: str
    device_type: str
    status: str = "off"

# Device Control Request Model
class DeviceControlRequest(BaseModel):
    status: str

### User Endpoints ###
@app.post("/api/users")
def create_user(user: User):
    user_id = str(uuid4())
    users[user_id] = user.model_dump()  # ✅ Fixed Pydantic dict() deprecation
    return {"user_id": user_id, **users[user_id]}


@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, **users[user_id]}


### House Endpoints ###
@app.post("/api/houses")
def create_house(house: House):
    if house.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    house_id = str(uuid4())
    houses[house_id] = house.model_dump()
    return {"house_id": house_id, **houses[house_id]}


@app.get("/api/houses/{house_id}")
def get_house(house_id: str):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    return {"house_id": house_id, **houses[house_id]}


### Room Endpoints ###
@app.post("/api/houses/{house_id}/rooms")
def add_room(house_id: str, room: Room):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    room_id = str(uuid4())
    rooms[room_id] = room.model_dump()
    return {"room_id": room_id, **rooms[room_id]}


@app.get("/api/houses/{house_id}/rooms")
def get_rooms(house_id: str):
    return {"rooms": [room for room in rooms.values() if room["house_id"] == house_id]}


### Device Endpoints ###
@app.post("/api/rooms/{room_id}/devices")
def add_device(room_id: str, device: Device):
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    device_id = str(uuid4())
    devices[device_id] = device.model_dump()
    return {"device_id": device_id, **devices[device_id]}


@app.get("/api/rooms/{room_id}/devices")
def get_devices(room_id: str):
    return {"devices": [device for device in devices.values() if device["room_id"] == room_id]}


@app.post("/api/devices/{device_id}/control")
def control_device(device_id: str, request: DeviceControlRequest):
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")

    print(f"Received request: {request.model_dump()}")  # Debugging print
    devices[device_id]["status"] = request.status
    return {"message": f"Device {device_id} turned {request.status}"}
