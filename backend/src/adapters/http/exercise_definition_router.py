from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio import session

from backend.src.adapters.http.dependencies import get_exercise_info_service
from backend.src.adapters.response.exercise_info_response import ExerciseDefinitionResponse
from backend.src.services.exercise_info_service import ExerciseInfoService


router = APIRouter(
    prefix="/exercise_definition",
    tags=["exercise_definition"],
)

@router.get(
    "/all",
    response_model=list[ExerciseDefinitionResponse],
)
def list_exercise_definition(
    service: ExerciseInfoService = Depends(get_exercise_info_service),
):
    return [
        ExerciseDefinitionResponse.model_validate(definition, from_attributes=True)
        for definition in service.list_exercise_definitions()
    ]
