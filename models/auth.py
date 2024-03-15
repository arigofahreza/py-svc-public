from typing import List

from pydantic import BaseModel


class LoginSchema(BaseModel):
    user_id: str
    password: str


class RegisterSchema(BaseModel):
    email_address: List[str]
    password: str
    username: str
