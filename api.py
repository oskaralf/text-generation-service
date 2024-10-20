from fastapi import FastAPI
from src.routes import routers
import uvicorn


class Api:
    def __init__(self):
        self.app = FastAPI()
        for router in routers:
            self.app.include_router(router)

    def run(self):
        uvicorn.run(self.app, host="127.0.0.1", port=8000)
