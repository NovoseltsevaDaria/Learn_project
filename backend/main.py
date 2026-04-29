from fastapi import FastAPI, HTTPException, status
from database import init_db
from crud import get_all_rooms, get_room_by_id, create_room, update_room, delete_room
from schemas import RoomCreate, RoomUpdate, RoomRead

app = FastAPI(title="Hotel API", description="API для управления номерами отеля")

# При запуске создаём таблицу
@app.on_event("startup")
def startup():
    init_db()

# GET /rooms - список всех номеров
@app.get("/rooms", response_model=list[RoomRead])
def get_rooms():
    '''
    Выводит список комнат
    :return: Список всех комнат
    '''
    return get_all_rooms()

# GET /rooms/{id} - один номер
@app.get("/rooms/{room_id}", response_model=RoomRead)
def get_room(room_id: int):
    room = get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return room

# POST /rooms - создать номер
@app.post("/rooms", status_code=status.HTTP_201_CREATED)
def add_room(room: RoomCreate):
    room_id = create_room(room.model_dump())
    return {"message": "Номер создан", "id": room_id}

# PUT /rooms/{id} - обновить номер
@app.put("/rooms/{room_id}")
def edit_room(room_id: int, room: RoomUpdate):
    existing = get_room_by_id(room_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Номер не найден")
    update_room(room_id, room.model_dump())
    return {"message": "Номер обновлён"}

# DELETE /rooms/{id} - удалить номер
@app.delete("/rooms/{room_id}")
def remove_room(room_id: int):
    existing = get_room_by_id(room_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Номер не найден")
    delete_room(room_id)
    return {"message": "Номер удалён"}