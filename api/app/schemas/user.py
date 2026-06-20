from pydantic import Basemodel

class UserBase(Basemodel):
    username: str
    email: str

class UserCreate(UserBase):
    hashed_password: str

class UserResponse(UserBase):
    user_id: int

    class Config:
        from_attributes = True