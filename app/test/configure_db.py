import os
import sqlalchemy
from sqlalchemy.orm import Session

password = os.environ["password"]

TEST_DB_NAME = "pytest_database"
PG_ENGINE = f"postgresql://postgres:{password}@localhost"


def create_test_database():

    engine = sqlalchemy.create_engine(PG_ENGINE)

    with engine.connect() as conn:
        conn.execute("commit")
        conn.execute(f"CREATE DATABASE {TEST_DB_NAME}")


def drop_test_database():

    engine = sqlalchemy.create_engine(PG_ENGINE)

    with engine.connect() as conn:

        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute("DROP DATABASE pytest_database WITH (FORCE)")


def run_sql_from_file(file_path: str, session: Session) -> None:

    with open(file_path, "r") as sql:
        sql_content = sqlalchemy.text(sql.read())
        session.execute(sql_content)
