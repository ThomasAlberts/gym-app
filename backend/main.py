from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session

from backend.src.adapters.database.database import engine
from backend.src.adapters.database.seed import seed_domain_data
from backend.src.adapters.http import ai_request_router
from backend.src.core.config import settings

from backend.src.adapters.http.workout_router import router as workout_router
from backend.src.adapters.http.exercise_info_router import router as exercise_info_router
from backend.src.adapters.http.ai_request_router import router as ai_request_router
from backend.src.adapters.auth.auth_router import router as auth_router

# Domain models
from backend.src.domain.exercise_definition import ExerciseDefinition
from backend.src.domain.exercise_muscle_link import ExerciseMuscleLink
from backend.src.domain.movement import Movement

# Models
from backend.src.models.user import User
from backend.src.models.exercise import Exercise
from backend.src.models.exercise_set import ExerciseSet
from backend.src.models.workout_session import WorkoutSession

#todo: fake db later weg na dev?

#todo: fake db later weg na dev?

app = FastAPI(
    title="TA Gym",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
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

# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(bind=engine)

# todo: fix later dit reset en hermaakt db bij elke opstart
@app.on_event("startup")
def reset_db():
    # Drop all tables first
    SQLModel.metadata.drop_all(engine)
    # Recreate tables
    SQLModel.metadata.create_all(engine)

    # Seed reference data (movements, exercise definitions, muscle links)
    with Session(engine) as session:
        seed_domain_data(session)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

