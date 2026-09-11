import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.src.adapters.database.database import get_database
from backend.src.adapters.dto.ai_request_dto import SuggestionOut, SuggestRequest
from backend.src.core.config import settings
from backend.src.services import ai_request_service

router = APIRouter(prefix="/exercise_info", tags=["exercise_info"])

llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=settings.GOOGLE_API_KEY)


@router.post("/exercise/suggest", response_model=list[SuggestionOut])
def suggest_exercise(payload: SuggestRequest, session: Session = Depends(get_database)):
    if not payload.current_exercises:
        raise HTTPException(400, "current_exercises must not be empty")

    candidates = ai_request_service.get_suggestion_candidates(session, payload.exclude_definition_ids)
    if not candidates:
        return []

    prompt = ai_request_service.build_suggestion_prompt(payload.current_exercises, candidates)

    try:
        raw_text = llm.invoke(prompt).content
        if isinstance(raw_text, list):
            raw_text = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in raw_text)
        return ai_request_service.parse_suggestion_response(raw_text, candidates)
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        raise HTTPException(502, f"Couldn't parse AI response: {e}")
    except Exception as e:
        raise HTTPException(502, f"Suggestion generation failed: {e}")