from src.routes.test import router as test_router
from src.routes.openai import router as openai_router

routers = [
    test_router,
    openai_router
]