# services/workout_service.py
from fastapi import HTTPException
from sqlmodel import Session, select

from backend.src.domain.exercise_definition import ExerciseDefinition
from backend.src.domain.workout_session import WorkoutSession
from backend.src.domain.exercise import Exercise
from backend.src.domain.exercise_set import ExerciseSet
from backend.src.adapters.dto.workout_dto import WorkoutCreate, WorkoutUpdate


class WorkoutService:
    def __init__(self, session: Session):
        self.session = session

    def create_workout(self, user_id: int, dto: WorkoutCreate) -> WorkoutSession:
        workout = WorkoutSession(
            user_id=user_id,
            name=dto.name,
            started_at=dto.started_at,
            ended_at=dto.ended_at,
        )

        _check_exercise_definition_ids(self, dto.exercises)

        workout.exercises = [
            Exercise(
                exercise_definition_id=ex.exercise_definition_id,
                notes=ex.notes,
                exercise_sets=[
                    ExerciseSet(
                        reps=s.reps,
                        weight=s.weight,
                        work_time=s.work_time,
                        rest_time=s.rest_time,
                    )
                    for s in ex.exercise_sets
                ],
            )
            for ex in dto.exercises
        ]

        self.session.add(workout)
        self.session.commit()
        self.session.refresh(workout)
        return workout


    def update_workout(self, workout_id: int, dto: WorkoutUpdate) -> WorkoutSession | None:
        workout = self.session.get(WorkoutSession, workout_id)
        if workout is None:
            return None

        update_data = dto.model_dump(exclude_unset=True, exclude={"exercises"})
        for field, value in update_data.items():
            setattr(workout, field, value)

        if dto.exercises is not None:
            _check_exercise_definition_ids(self, dto.exercises)

            workout.exercises = [
                Exercise(
                    exercise_definition_id=ex.exercise_definition_id,
                    notes=ex.notes,
                    exercise_sets=[
                        ExerciseSet(
                            reps=s.reps,
                            weight=s.weight,
                            work_time=s.work_time,
                            rest_time=s.rest_time,
                        )
                        for s in ex.exercise_sets
                    ],
                )
                for ex in dto.exercises
            ]

        self.session.add(workout)
        self.session.commit()
        self.session.refresh(workout)
        return workout


    def delete_workout(self, workout_id: int, user_id: int) -> bool:
        workout = self.session.get(WorkoutSession, workout_id)
        if workout is None or workout.user_id != user_id:
            return False
        self.session.delete(workout)
        self.session.commit()
        return True


    def get_workout(self, workout_id: int) -> WorkoutSession | None:
        return self.session.get(WorkoutSession, workout_id)


    def get_all_workouts(self, user_id: int) -> list[WorkoutSession]:
        statement = (
            select(WorkoutSession)
            .where(WorkoutSession.user_id == user_id)
            .order_by(WorkoutSession.started_at.desc())
        )
        return self.session.exec(statement).all()


## private functions

def _check_exercise_definition_ids(self, exercises):
    for ex in exercises:
        _check_exercise_definition_id(self, ex.exercise_definition_id)


def _check_exercise_definition_id(self, exercise_definition_id):
    definition = self.session.get(ExerciseDefinition, exercise_definition_id)
    if definition is None:
        raise HTTPException(
            status_code=400,
            detail=f"exercise_definition_id {exercise_definition_id} does not exist",
        )