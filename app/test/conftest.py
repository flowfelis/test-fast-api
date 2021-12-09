import pytest

from typing import Tuple
import sqlalchemy
from sqlalchemy import event as sa_event, create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..main import app
from fastapi.testclient import TestClient
from ..lib.db import get_session, DBUser, get_db_user
from .configure_db import create_test_database, drop_test_database, run_sql_from_file


@pytest.fixture
def session_and_db_user() -> Tuple[Session, DBUser]:

    create_test_database()

    db_user = get_db_user(test=True)

    DATABASE_URI = f"postgresql://{db_user.db_username}:{db_user.db_password}@{db_user.db_host}/{db_user.db_name}"

    engine = create_engine(DATABASE_URI)
    CreateSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    connection = engine.connect()
    transaction = connection.begin()

    session = CreateSession()

    run_sql_from_file("./test_scripts/prepare.sql", session)

    nested = connection.begin_nested()

    @sa_event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested

        if not nested.is_active:
            nested = connection.begin_nested()

    session.execute(f"SET search_path TO {db_user.schema}, public;")

    yield session, db_user

    session.close()
    transaction.rollback()
    connection.close()

    drop_test_database()


@pytest.fixture
def client(session_and_db_user):
    def ovveride_get_session() -> Tuple[Session, DBUser]:
        yield session_and_db_user

    app.dependency_overrides[get_session] = ovveride_get_session
    yield TestClient(app)
    del app.dependency_overrides[get_session]
