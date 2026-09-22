from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session

from backend.src.adapters.database.database import engine
from backend.src.adapters.database.seed import seed_domain_data
from backend.src.core.config import settings

from backend.src.adapters.http.workout_router import router as workout_router
from backend.src.adapters.http.exercise_info_router import router as exercise_info_router
from backend.src.adapters.http.ai_request_router import router as ai_request_router
from backend.src.adapters.auth.auth_router import router as auth_router

# Domain models

# Models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once on startup, before the app accepts requests
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_domain_data(session)

    yield

app = FastAPI(
    title="TA Gym",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(workout_router)
app.include_router(exercise_info_router)
app.include_router(auth_router)
app.include_router(ai_request_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)