from src.routes.test import router as test_router
from src.routes.openai import router as openai_router
from src.routes.words import router as words_router
from src.routes.frontend import router as frontend_router
from src.routes.user import router as user_router
from src.routes.score import router as score_router

routers = [
    test_router,
    openai_router,
    words_router,
    frontend_router,
    user_router,
    score_router
]
