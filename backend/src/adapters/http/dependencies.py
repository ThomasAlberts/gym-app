"""Wiring: the one place that knows which concrete classes fill the domain ports."""
from fastapi import Depends
from sqlmodel import Session
from functools import lru_cache

from backend.src.adapters.ai.gemini_generator import GeminiTextGenerator
from backend.src.adapters.database.database import get_database
from backend.src.adapters.database.repositories.exercise_definition_repository import (
    SqlExerciseDefinitionRepository,
)
from backend.src.adapters.database.repositories.exercise_repository import SqlExerciseRepository
from backend.src.adapters.database.repositories.workout_session_repository import (
    SqlWorkoutSessionRepository,
)
from backend.src.core.config import settings
from backend.src.services.ai_suggestion_service import AiSuggestionService
from backend.src.services.exercise_info_service import ExerciseInfoService
from backend.src.services.workout_session_service import WorkoutSessionService


def get_exercise_info_service(
    session: Session = Depends(get_database),
) -> ExerciseInfoService:
    return ExerciseInfoService(
        exercise_repository=SqlExerciseRepository(session),
        exercise_definition_repository=SqlExerciseDefinitionRepository(session),
    )

def get_workout_session_service(
    session: Session = Depends(get_database),
) -> WorkoutSessionService:
    return WorkoutSessionService(
        workout_session_repository=SqlWorkoutSessionRepository(session),
        exercise_info_service=get_exercise_info_service(session),
    )



@lru_cache
def get_text_generator() -> GeminiTextGenerator:
    return GeminiTextGenerator(api_key=settings.GOOGLE_API_KEY)


def get_ai_suggestion_service(
    session: Session = Depends(get_database),
    generator: GeminiTextGenerator = Depends(get_text_generator),
) -> AiSuggestionService:
    return AiSuggestionService(definitions=SqlExerciseDefinitionRepository(session), generator=generator)