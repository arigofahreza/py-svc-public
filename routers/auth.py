from fastapi import APIRouter, Response

from models.auth import RegisterSchema, LoginSchema
from services.auth import Auth

router = APIRouter()


@router.post(
    '/register',
    description='register account to clerk platform',
    name='register account',
)
async def register(schema: RegisterSchema):
    auth = Auth()
    return await auth.register(schema)


@router.post(
    '/login',
    description='login account from user clerk platform',
    name='login account',
)
async def register(schema: LoginSchema):
    auth = Auth()
    return await auth.login(schema)
