# services/workout_service.py
from datetime import datetime, time, timedelta, timezone
from sqlmodel import Session, select

from backend.src.domain.exercise_definition import ExerciseDefinition
from backend.src.domain.exercise_muscle_link import ExerciseMuscleLink  # adjust import path if this lives elsewhere
from backend.src.domain.exercise import Exercise
from backend.src.domain.workout_session import WorkoutSession


class ExerciseInfoService:
    def __init__(self, session: Session):
        self.session = session


    def get_all_exercise_definitions(self):
        return self.session.query(ExerciseDefinition).all()


    def get_all_exercises_for_user(self, user_id: int) -> list[Exercise]:
        statement = (
            select(Exercise)
            .join(WorkoutSession, Exercise.workout_session_id == WorkoutSession.id)
            .where(WorkoutSession.user_id == user_id)
            .order_by(WorkoutSession.started_at.desc())
        )
        return self.session.exec(statement).all()


    def get_exercises_since_monday(
        self,
        user_id: int,
    ) -> list[Exercise]:
        """
        Return all exercises performed from the most recent Monday
        at 00:00 until the current moment.

        If today is Monday, this returns exercises from today at 00:00
        until now.
        """

        now = datetime.now(timezone.utc)

        # weekday(): Monday = 0, Tuesday = 1, ..., Sunday = 6
        monday_date = (
            now.date() - timedelta(days=now.weekday())
        )

        monday_start = datetime.combine(
            monday_date,
            time.min,
            tzinfo=timezone.utc,
        )

        statement = (
            select(Exercise)
            .join(
                WorkoutSession,
                Exercise.workout_session_id == WorkoutSession.id,
            )
            .where(
                WorkoutSession.user_id == user_id,
                WorkoutSession.started_at >= monday_start,
                WorkoutSession.started_at <= now,
            )
            .order_by(
                WorkoutSession.started_at.desc()
            )
        )

        return list(self.session.exec(statement).all())


    def get_muscle_links_by_definition_id(
        self,
        exercises: list[Exercise],
    ) -> dict[int, list[ExerciseMuscleLink]]:
        """
        Return all ExerciseMuscleLink rows for the exercise definitions
        used in `exercises`, grouped by exercise_definition_id.
        """
        definition_ids = {
            exercise.exercise_definition_id
            for exercise in exercises
        }

        if not definition_ids:
            return {}

        statement = select(ExerciseMuscleLink).where(
            ExerciseMuscleLink.exercise_definition_id.in_(definition_ids)
        )
        links = self.session.exec(statement).all()

        grouped: dict[int, list[ExerciseMuscleLink]] = {}
        for link in links:
            grouped.setdefault(link.exercise_definition_id, []).append(link)

        return grouped


    def compute_muscle_strain(
        self,
        exercises: list[Exercise],
        muscle_links_by_definition: dict[int, list[ExerciseMuscleLink]],
    ) -> dict[str, float]:
        """
        Sum set_count * emphasis across `exercises`, grouped by leaf muscle
        (the raw Muscle enum value on each ExerciseMuscleLink).

        Falls back to an emphasis of 1 if a link's emphasis is missing,
        so a null value doesn't drop that muscle out of the sum.
        """
        strain: dict[str, float] = {}

        for exercise in exercises:
            set_count = len(exercise.exercise_sets or [])
            if not set_count:
                continue

            links = muscle_links_by_definition.get(
                exercise.exercise_definition_id, []
            )
            for link in links:
                emphasis = link.emphasis if link.emphasis is not None else 1
                strain[link.muscle] = (
                    strain.get(link.muscle, 0) + set_count * emphasis
                )

        return strain


    def get_last_exercises_for_definition(
        self,
        user_id: int,
        exercise_definition_id: int,
        limit: int = 3,
        exclude_workout_session_id: int | None = None,
    ) -> list[Exercise]:
        """
        Return the latest exercises for one exercise definition,
        from the most recent Monday until now.

        If today is Monday, the range is:
            today at 00:00 <= started_at <= now
        """

        if limit < 1:
            raise ValueError("limit must be at least 1")

        now = datetime.now(timezone.utc)

        monday_date = (
            now.date() - timedelta(days=now.weekday())
        )

        monday_start = datetime.combine(
            monday_date,
            time.min,
            tzinfo=timezone.utc,
        )

        statement = (
            select(Exercise)
            .join(
                WorkoutSession,
                Exercise.workout_session_id == WorkoutSession.id,
            )
            .where(
                WorkoutSession.user_id == user_id,
                Exercise.exercise_definition_id == exercise_definition_id,
                WorkoutSession.started_at >= monday_start,
                WorkoutSession.started_at <= now,
            )
        )

        if exclude_workout_session_id is not None:
            statement = statement.where(
                Exercise.workout_session_id
                != exclude_workout_session_id
            )

        statement = (
            statement
            .order_by(WorkoutSession.started_at.desc())
            .limit(limit)
        )

        return list(self.session.exec(statement).all())
