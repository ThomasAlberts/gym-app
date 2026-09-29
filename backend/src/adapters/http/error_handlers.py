from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.src.domain.errors import (
    InvalidAiResponse,
    InvalidWorkout,
    UnknownExerciseDefinition,
)


def register_error_handlers(app: FastAPI) -> None:
    """Domain errors -> HTTP. Call once in main.py after creating the app."""

    @app.exception_handler(UnknownExerciseDefinition)
    async def _unknown_definition(_: Request, exc: UnknownExerciseDefinition):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(InvalidWorkout)
    async def _invalid_workout(_: Request, exc: InvalidWorkout):
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(InvalidAiResponse)
    async def _invalid_ai_response(_: Request, exc: InvalidAiResponse):
        return JSONResponse(status_code=502, content={"detail": "AI returned an unusable response"})
