# backend/tests/conftest.py

import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from starlette.testclient import TestClient

# Domain models
from backend.src.domain.exercise_definition import ExerciseDefinition
from backend.src.domain.exercise_muscle_link import ExerciseMuscleLink
from backend.src.domain.movement import Movement

# Models
from backend.src.models.user import User
from backend.src.models.exercise import Exercise
from backend.src.models.exercise_set import ExerciseSet
from backend.src.models.workout_session import WorkoutSession

from backend.src.adapters.database.database import get_database
from backend.main import app


# ── 1. In-memory SQLite engine ─────────────────────────────
@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


# ── 2. Per-test session ────────────────────────────────────
@pytest.fixture
def db(test_engine):
    session = Session(test_engine)
    yield session
    session.close()


# ── 3. Client met DB override ──────────────────────────────
@pytest.fixture
def client(db):
    def override_get_database():
        yield db

    app.dependency_overrides[get_database] = override_get_database
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── 4. Seed domain data ────────────────────────────────────
@pytest.fixture(scope="function", autouse=True)
def seed_domain_data(db: Session):
    from backend.tests.fixtures.domain_setup_tests import (
        _movements,
        _exercise_definitions,
        _exercise_muscle_links,
    )

    db.add_all(_movements())
    db.add_all(_exercise_definitions())
    db.add_all(_exercise_muscle_links())
    db.commit()