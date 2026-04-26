from pydantic import BaseModel, Field
from typing import Optional

# Для создания нового номера
class RoomCreate(BaseModel):
    room_number: int = Field(..., gt=0, description="Номер комнаты (положительное число)")
    type: str = Field(..., pattern="^(single|double|suite)$")
    price_per_night: float = Field(..., gt=0)
    is_available: bool
    capacity: int = Field(..., ge=1, le=6)
    description: Optional[str] = None

# Для полного обновления
class RoomUpdate(BaseModel):
    room_number: int = Field(..., gt=0)
    type: str = Field(..., pattern="^(single|double|suite)$")
    price_per_night: float = Field(..., gt=0)
    is_available: bool
    capacity: int = Field(..., ge=1, le=6)
    description: Optional[str] = None

# Для чтения (с id)
class RoomRead(BaseModel):
    id: int
    room_number: int
    type: str
    price_per_night: float
    is_available: bool
    capacity: int
    description: Optional[str] = None