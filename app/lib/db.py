import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .db_user import DBUser, get_db_user

# password = os.environ["password"]

# DATABASE_URI = f"postgresql://postgres:{password}@localhost/fastapi_utils"

# engine = create_engine(DATABASE_URI)
# CreateSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = automap_base()
# Base.prepare(engine, reflect=True)


def get_session():

    db_user = get_db_user()

    DATABASE_URI = f"postgresql://{db_user.db_username}:{db_user.db_password}@{db_user.db_host}/{db_user.db_name}"

    engine = create_engine(DATABASE_URI)
    CreateSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = CreateSession()

    try:
        session.execute(f"SET search_path TO {db_user.schema}, public;")
        yield session, db_user
    finally:
        session.close()


def get_raw_connection():

    db_user = get_db_user()

    DATABASE_URI = f"postgresql://{db_user.db_username}:{db_user.db_password}@{db_user.db_host}/{db_user.db_name}"

    engine = create_engine(DATABASE_URI)
    connection = engine.raw_connection()

    try:
        yield connection, db_user

        connection.commit()
    except:
        connection.rollback()

    connection.close()
