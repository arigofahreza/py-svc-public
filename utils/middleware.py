import binascii

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from utils.helpers import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if request.cookies.get('clrk_tkn'):
                token = request.cookies.get('clrk_tkn')
                try:
                    authorized, error = self.verify_jwt(token)
                    if not authorized:
                        raise HTTPException(status_code=403, detail=error)
                    return credentials.credentials
                except binascii.Error:
                    raise HTTPException(status_code=403, detail="Invalid authorization code.")
            else:
                raise HTTPException(status_code=404, detail={
                    "status": 404,
                    "message": "token not found"
                })
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(token: str) -> (bool, str):
        valid = decode_jwt(token)
        if valid:
            return True, ""
        return False, "token expired"
