import json
from dataclasses import dataclass, field
from typing import Any, Optional

from backend.src.adapters.database.repositories.exercise_definition_repository import SqlExerciseDefinitionRepository
from backend.src.domain.entities.exercise_definition import ExerciseDefinition
from backend.src.domain.errors import InvalidAiResponse, EmptyCurrentExercises

MAX_SUGGESTIONS = 3


class AiSuggestionService:
    def __init__(self, definitions, generator):
        self._definitions = definitions
        self._generator = generator

    def suggest(self, current_exercises, exclude_definition_ids):
        if not current_exercises:
            raise EmptyCurrentExercises("current_exercises must not be empty")
        candidates = get_suggestion_candidates(self._definitions, exclude_definition_ids)
        if not candidates:
            return []
        prompt = build_suggestion_prompt(current_exercises, candidates)
        raw = self._generator.generate(prompt)
        return parse_suggestion_response(raw, candidates)


@dataclass(frozen=True)
class LoggedSet:
    reps: Optional[int] = None
    weight: Optional[float] = None


@dataclass(frozen=True)
class LoggedExercise:
    name: str
    equipment_type: str
    grip_type: str = "none"
    sets: list[LoggedSet] = field(default_factory=list)


@dataclass(frozen=True)
class Suggestion:
    id: int
    name: str
    equipment_type: str
    grip_type: str
    reason: str


def get_suggestion_candidates(
        exercise_definitions: SqlExerciseDefinitionRepository, exclude_ids: list[int]
) -> list[ExerciseDefinition]:
    return exercise_definitions.list_excluding(exclude_ids)


def _label(value: Any) -> Any:
    return getattr(value, "value", value)


def _format_set(s: LoggedSet) -> str:
    reps = s.reps if s.reps is not None else "?"  # 0 is a real value, not "unknown"
    weight = s.weight if s.weight is not None else "?"
    return f"{reps} reps @ {weight}"


def _format_exercise(ex: LoggedExercise) -> str:
    sets = ", ".join(_format_set(s) for s in ex.sets) or "no sets logged yet"
    grip = _label(ex.grip_type)
    grip_part = f" ({grip})" if grip not in (None, "none") else ""
    return f"- {ex.name} [{_label(ex.equipment_type)}{grip_part}]: {sets}"


def _format_candidates(defs: list[ExerciseDefinition]) -> str:
    return "\n".join(
        f'- id={d.id}, name="{d.name}", equipment_type={_label(d.equipment_type)}, '
        f'grip_type={_label(d.grip_type) if d.grip_type else "none"}'
        for d in defs
    )


def build_suggestion_prompt(
        current_exercises: list[LoggedExercise], candidates: list[ExerciseDefinition]
) -> str:
    done = "\n".join(_format_exercise(e) for e in current_exercises)
    return f"""You are a strength training assistant helping someone mid-workout_session.

    Here is what they've done so far in this session:
    {done}

    Here are the exercises available to suggest from (you MUST only pick from this list, using the exact id):
    {_format_candidates(candidates)}

    Pick 1 to {MAX_SUGGESTIONS} exercises from the candidate list that would logically come next \
    (consider muscle group balance, fatigue, equipment already in use, and reasonable session length). \
    Respond with ONLY a JSON array, no markdown, no prose, in this exact shape:
    [{{"id": <int>, "reason": "<one short sentence>"}}]"""


def _extract_json_array(raw_text: str) -> list:
    start, end = raw_text.find("["), raw_text.rfind("]")
    if start == -1 or end < start:
        raise InvalidAiResponse("no JSON array found in model response")
    try:
        parsed = json.loads(raw_text[start: end + 1])
    except json.JSONDecodeError as exc:
        raise InvalidAiResponse("model response was not valid JSON") from exc
    if not isinstance(parsed, list):
        raise InvalidAiResponse("model response was not a JSON array")
    return parsed


def parse_suggestion_response(
        raw_text: str,
        candidates: list[ExerciseDefinition],
        max_suggestions: int = MAX_SUGGESTIONS,
) -> list[Suggestion]:
    by_id = {c.id: c for c in candidates}
    seen: set[int] = set()
    results: list[Suggestion] = []

    for item in _extract_json_array(raw_text):
        if not isinstance(item, dict):
            continue
        definition_id = item.get("id")
        if not isinstance(definition_id, int) or definition_id in seen:
            continue
        definition = by_id.get(definition_id)
        if definition is None:  # model invented an id, or it was excluded
            continue
        seen.add(definition_id)
        results.append(
            Suggestion(
                id=definition.id,
                name=definition.name,
                equipment_type=_label(definition.equipment_type),
                grip_type=_label(definition.grip_type) if definition.grip_type else "none",
                reason=str(item.get("reason", "")),
            )
        )
        if len(results) == max_suggestions:
            break
    return results