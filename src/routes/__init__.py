from src.routes.test import router as test_router
from src.routes.openai import router as openai_router
from src.routes.frontend import router as frontend_router

routers = [
    test_router,
    openai_router,
    frontend_router
]