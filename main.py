from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.v1 import router


def start() -> FastAPI:
    application = FastAPI(title='Protected Public API Data',
                          description='API for retrieving any data',
                          version='1.0.0')
    # application.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )
    application.include_router(router, prefix='/api/v1')
    return application


app = start()
