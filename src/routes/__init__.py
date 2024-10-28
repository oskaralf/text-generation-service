from src.routes.test import router as test_router
from src.routes.openai import router as openai_router
from src.routes.words import router as words_router

routers = [
    test_router,
    openai_router,
    words_router
]