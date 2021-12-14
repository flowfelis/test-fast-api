from typing import Tuple

from fastapi.testclient import TestClient

from app.lib.db_user import DBUser
from .configure_db import run_sql_from_file
from sqlalchemy.orm import Session


def test_root(client: TestClient):

    response = client.get("/sql_alchemy")

    second = client.get("/sql_alchemy")

    assert response.json() == second.json()


def test_list_of_cars_one(client: TestClient):

    response = client.get("/car")

    assert len(response.json()) == 1


def test_add_car(client: TestClient):

    car = {"brand": "BMW", "model": "E39", "is_available": True}

    response = client.post("/car", json=car)

    assert response.status_code == 200


def test_list_of_cars(client: TestClient, session_and_db_user: Tuple[Session, DBUser]):
    """
    there is still one car in db
    although we have just added one
    """
    session, db_user = session_and_db_user

    # insert 5 new cars
    run_sql_from_file("../test_scripts/five_new_cars.sql", session)

    response = client.get("/car")

    assert len(response.json()) == 6
