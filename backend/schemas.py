from pydantic import BaseModel
from typing import Optional

class ClothingItemBase(BaseModel):
    name: str
    category: str
    color: Optional[str] = None
    style: Optional[str] = None

class ClothingItemCreate(ClothingItemBase):
    pass

class ClothingItem(ClothingItemBase):
    id: int
    image_path: Optional[str] = None
    embedding_path: Optional[str] = None

    class Config:
        orm_mode = True
