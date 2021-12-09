import os

password = os.environ["password"]


def get_db_user(test: bool = False):

    db_user = DBUser()

    if test:
        db_user.db_name = "pytest_database"

    return db_user


class DBUser:

    schema: str = "dummy"
    db_username: str = "postgres"
    db_password: str = password
    db_host = "localhost"
    db_name = "fastapi_utils"
    username: str = "username@xxx.com"
    id: int = 1
    company_id: int = 1
