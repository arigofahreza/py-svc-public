from pydantic_settings import BaseSettings
from supabase import create_client


class Config(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_TABLE: str
    CLERK_PUBLISHABLE_KEY: str
    CLERK_SECRET_KEY: str
    CLERK_URL: str
    CLERK_JWT_SECRET: str
    CLERK_JWT_ALG: str
    CLERK_JWKS: str

    class Config:
        env_file = ".env"


def supabase_connection():
    config = Config()
    return create_client(config.SUPABASE_URL, config.SUPABASE_KEY), config.SUPABASE_TABLE


def clerk_connection():
    config = Config()
    return config.CLERK_URL, config.CLERK_SECRET_KEY


def clerk_jwt():
    config = Config()
    return config.CLERK_JWT_SECRET, config.CLERK_JWT_ALG, config.CLERK_JWKS
