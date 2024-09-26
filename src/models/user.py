from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    created_at: datetime
