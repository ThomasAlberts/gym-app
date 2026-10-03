from fastapi import APIRouter, Depends, HTTPException
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.src.adapters.dto.ai_request_dto import SuggestionOut, SuggestRequest
from backend.src.adapters.http.dependencies import get_exercise_definition_repository, get_ai_suggestion_service
from backend.src.adapters.http.mappers import logged_exercises_from_dto, suggestion_to_dto
from backend.src.core.config import settings
from backend.src.domain.errors import InvalidAiResponse, EmptyCurrentExercises, AiGenerationFailed
from backend.src.services.ai_suggestion_service import (
    build_suggestion_prompt,
    get_suggestion_candidates,
    parse_suggestion_response, AiSuggestionService,
)

router = APIRouter(prefix="/exercise_info", tags=["exercise_info"])


@router.post("/exercise/suggest", response_model=list[SuggestionOut])
def suggest_exercise(
    payload: SuggestRequest,
    service: AiSuggestionService = Depends(get_ai_suggestion_service),
):
    try:
        suggestions = service.suggest(
            logged_exercises_from_dto(payload.current_exercises),
            payload.exclude_definition_ids,
        )
    except EmptyCurrentExercises as e:
        raise HTTPException(400, str(e))
    except (AiGenerationFailed, InvalidAiResponse) as e:
        raise HTTPException(502, "Suggestion generation failed")
    return [suggestion_to_dto(s) for s in suggestions]