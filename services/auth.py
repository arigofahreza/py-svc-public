from starlette import status
from starlette.responses import JSONResponse

from configs.database import clerk_connection, supabase_connection
import requests

from models.auth import RegisterSchema, LoginSchema


class Auth:
    def __init__(self):
        self._clerk_url, self._clerk_secret_key = clerk_connection()
        self.supabase_client, self._table = supabase_connection()
        self._headers = {"Authorization": f"Bearer {self._clerk_secret_key}"}

    async def register(self, register_schema: RegisterSchema):
        response = requests.post(
            f"{self._clerk_url}/users",
            headers=self._headers,
            json=register_schema.dict()
        )
        if response.status_code == 200:
            res = self.supabase_client.storage.create_bucket(register_schema.username)
            if not res:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={'message': f"error creating storage for user: {register_schema.username}"},
                )
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={'message': f"register success"}
            )
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )

    async def login(self, login_schema: LoginSchema):
        verify_response = requests.post(
            f"{self._clerk_url}/users/{login_schema.user_id}/verify_password",
            headers=self._headers,
            json={'password': login_schema.password}
        )
        json_response = verify_response.json()
        if verify_response.status_code == 200:
            sign_in_response = requests.post(
                f"{self._clerk_url}/sign_in_tokens",
                headers=self._headers,
                json={
                    "user_id": login_schema.user_id,
                    "expires_in_seconds": 3600
                }
            )
            json_sign_in_response = sign_in_response.json()
            response = JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'token': json_sign_in_response.get('token'), 'message': 'login success'},
            )
            response.set_cookie('clrk_tkn', json_sign_in_response.get('token'))
            return response
        if json_response.get('errors'):
            message = json_response.get('errors')[0]['message']
            if message == 'not found':
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={'message': 'user not found'},
                )
            elif message == 'incorrect password':
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={'message': 'incorrect password'},
                )
