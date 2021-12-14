from typing import Tuple

import pytest
from fastapi.testclient import TestClient
from psycopg2.errors import DuplicateDatabase
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session

from .configure_db import create_test_database
from .configure_db import drop_test_database
from .configure_db import run_sql_from_file
from ..lib.db import DBUser
from ..lib.db import get_db_user
from ..lib.db import get_session
from ..main import app


# @pytest.fixture(scope='session', autouse=True, name='db_user')
# def create_and_drop_db():
#     db_user = get_db_user(test=True)
#     try:
#         create_test_database()
#     except ProgrammingError as e:
#         if isinstance(e.orig, DuplicateDatabase):
#             pass
#     yield db_user
#     drop_test_database()


@pytest.fixture
def session_and_db_user() -> Tuple[Session, DBUser]:
    db_user = get_db_user(test=True)

    try:
        create_test_database()
        DATABASE_URI = (
            'postgresql+psycopg2://'
            f'{db_user.db_username}:'
            f'{db_user.db_password}@'
            f'{db_user.db_host}:'
            f'{db_user.db_port}/'
            f'{db_user.db_name}'
        )

        engine = create_engine(DATABASE_URI)

        with Session(engine) as session:
            session.connection(execution_options={
                "schema_translate_map": {None: db_user.schema}})

            run_sql_from_file("../test_scripts/prepare.sql", session)


            yield session, db_user
    except ProgrammingError as e:
        if isinstance(e.orig, DuplicateDatabase):
            # if test db already exists, pass
            pass
    finally:
        drop_test_database()


@pytest.fixture
def client(session_and_db_user):
    def override_get_session() -> Tuple[Session, DBUser]:
        yield session_and_db_user

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()
