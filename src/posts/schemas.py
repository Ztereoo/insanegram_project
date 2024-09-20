from pydantic import BaseModel
from typing import List, Optional


class PostCreate(BaseModel):
    id: int
    text: str
    tags: List[str]
    photo: Optional[bytes]
    user_id: int

    class Config:
        orm_mode = True
