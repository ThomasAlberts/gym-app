import json

from sqlmodel import Session

from backend.src.adapters.dto.ai_request_dto import ExerciseIn, SuggestionOut
from backend.src.domain.exercise_definition import ExerciseDefinition


def get_suggestion_candidates(session: Session, exclude_ids: list[int]) -> list[ExerciseDefinition]:
    return (
        session.query(ExerciseDefinition)
        .filter(ExerciseDefinition.id.notin_(exclude_ids))
        .all()
    )


def _format_exercise(ex: ExerciseIn) -> str:
    sets = ", ".join(
        f"{s.reps or '?'} reps @ {s.weight if s.weight is not None else '?'}"
        for s in ex.exercise_sets
    ) or "no sets logged yet"
    grip = f" ({ex.grip_type})" if ex.grip_type not in (None, "none") else ""
    return f"- {ex.name} [{ex.equipment_type}{grip}]: {sets}"


def _format_candidates(defs: list[ExerciseDefinition]) -> str:
    return "\n".join(
        f'- id={d.id}, name="{d.name}", equipment_type={d.equipment_type}, grip_type={d.grip_type or "none"}'
        for d in defs
    )


def build_suggestion_prompt(current_exercises: list[ExerciseIn], candidates: list[ExerciseDefinition]) -> str:
    return f"""You are a strength training assistant helping someone mid-workout.

Here is what they've done so far in this session:
{chr(10).join(_format_exercise(e) for e in current_exercises)}

Here are the exercises available to suggest from (you MUST only pick from this list, using the exact id):
{_format_candidates(candidates)}

Pick 1 to 3 exercises from the candidate list that would logically come next \
(consider muscle group balance, fatigue, equipment already in use, and reasonable session length). \
Respond with ONLY a JSON array, no markdown, no prose, in this exact shape:
[{{"id": <int>, "reason": "<one short sentence>"}}]"""


def parse_suggestion_response(raw_text: str, candidates: list[ExerciseDefinition]) -> list[SuggestionOut]:
    by_id = {c.id: c for c in candidates}
    cleaned = raw_text.strip().strip("```json").strip("```").strip()
    picked = json.loads(cleaned)

    results = []
    for item in picked:
        definition = by_id.get(item.get("id"))
        if not definition:
            continue
        results.append(SuggestionOut(
            id=definition.id,
            name=definition.name,
            equipment_type=definition.equipment_type,
            grip_type=definition.grip_type or "none",
            reason=item.get("reason", ""),
        ))
    return results