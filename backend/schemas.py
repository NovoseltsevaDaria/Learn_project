from pydantic import BaseModel, Field
from typing import Optional

# Для создания нового номера
class RoomCreate(BaseModel):
    room_number: int = Field(..., gt=0, description="Номер комнаты")
    type: str = Field(..., pattern="^(single|double|suite)$", description="Тип: single/double/suite")
    price_per_night: float = Field(..., gt=0, description="Цена за ночь")
    is_available: bool = Field(..., description="Доступен?")
    capacity: int = Field(..., ge=1, le=6, description="Вместимость от 1 до 6")
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
class RoomRead(RoomCreate):
    id: int