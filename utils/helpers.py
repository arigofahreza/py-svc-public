import time

import jwt

from configs.database import clerk_jwt


def get_jwks(token: str):
    secret, alg, url = clerk_jwt()
    jwks_client = jwt.PyJWKClient(url)
    key = jwks_client.get_signing_key(secret).key
    return key, alg


def decode_jwt(token: str) -> bool:
    key, alg = get_jwks(token)
    decoded_token = jwt.decode(token, key, algorithms=[alg], options={"verify_signature": True})
    if decoded_token["exp"] >= time.time():
        return True
    return False
