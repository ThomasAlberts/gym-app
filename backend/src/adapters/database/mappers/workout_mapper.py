from typing import Optional

from backend.src.domain.entities.workout_session import WorkoutSession as DomainWorkoutSession
from backend.src.domain.entities.exercise import Exercise as DomainExercise
from backend.src.domain.entities.exercise_set import ExerciseSet as DomainExerciseSet

from backend.src.adapters.database.models.workout_session import WorkoutSession as ORMWorkoutSession
from backend.src.adapters.database.models.exercise import Exercise as ORMExercise
from backend.src.adapters.database.models.exercise_set import ExerciseSet as ORMExerciseSet


def _exercise_set_to_domain(orm: ORMExerciseSet) -> DomainExerciseSet:
    return DomainExerciseSet(
        id=orm.id,
        exercise_id=orm.exercise_id,
        reps=orm.reps,
        weight=orm.weight,
        work_time=orm.work_time,
        rest_time=orm.rest_time,
    )


def _exercise_to_domain(orm: ORMExercise) -> DomainExercise:
    return DomainExercise(
        id=orm.id,
        workout_session_id=orm.workout_session_id,
        exercise_definition_id=orm.exercise_definition_id,
        notes=orm.notes,
        exercise_sets=[_exercise_set_to_domain(s) for s in orm.exercise_sets],
    )


def workout_session_to_domain(orm: ORMWorkoutSession) -> DomainWorkoutSession:
    return DomainWorkoutSession(
        id=orm.id,
        user_id=orm.user_id,
        name=orm.name,
        started_at=orm.started_at,
        ended_at=orm.ended_at,
        exercises=[_exercise_to_domain(e) for e in orm.exercises],
    )


def workout_session_to_orm(
    session: DomainWorkoutSession, existing: Optional[ORMWorkoutSession] = None
) -> ORMWorkoutSession:
    orm = existing or ORMWorkoutSession()
    orm.id = session.id
    orm.user_id = session.user_id
    orm.name = session.name
    orm.started_at = session.started_at
    orm.ended_at = session.ended_at

    existing_exercises_by_id = {e.id: e for e in orm.exercises if e.id is not None}
    rebuilt_exercises = []
    for exercise in session.exercises:
        orm_exercise = existing_exercises_by_id.get(exercise.id) or ORMExercise()
        orm_exercise.id = exercise.id
        orm_exercise.exercise_definition_id = exercise.exercise_definition_id
        orm_exercise.notes = exercise.notes

        existing_sets_by_id = {s.id: s for s in orm_exercise.exercise_sets if s.id is not None}
        rebuilt_sets = []
        for exercise_set in exercise.exercise_sets:
            orm_set = existing_sets_by_id.get(exercise_set.id) or ORMExerciseSet()
            orm_set.id = exercise_set.id
            orm_set.reps = exercise_set.reps
            orm_set.weight = exercise_set.weight
            orm_set.work_time = exercise_set.work_time
            orm_set.rest_time = exercise_set.rest_time
            rebuilt_sets.append(orm_set)
        orm_exercise.exercise_sets = rebuilt_sets
        rebuilt_exercises.append(orm_exercise)

    orm.exercises = rebuilt_exercises
    return orm
