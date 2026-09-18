import pytest
from sqlmodel import Session

from backend.src.adapters.database.seed import seed_domain_data  # adjust import path to wherever seed.py actually lives


@pytest.fixture(scope="session", autouse=True)
def seed_domain_data_fixture(test_engine):
    with Session(test_engine) as session:
        seed_domain_data(session)