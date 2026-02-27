# This file is a rulebook. It defines data validation models.
from pydantic import BaseModel

# Rule for CREATEing a user (no id yet)
class UserCreate(BaseModel):
    name: str
    email: str

# Rule for DEALing with an existing uder (with ID)
class User(UserCreate):
    id: int