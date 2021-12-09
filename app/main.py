import logging
from typing import List, Tuple

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from .lib.db import get_raw_connection, get_session
from .lib.db_schemas import Cars, Users
from .lib.db_user import DBUser
from .lib.schemas import CarSchema

app = FastAPI()
logger = logging.getLogger("uvicorn.info")


@app.get("/sql_alchemy")
async def root(s_and_u: Tuple[Session, DBUser] = Depends(get_session)) -> JSONResponse:

    # maybe there is some method to unpack tuple before (?), idk
    session, db_user = s_and_u

    users = session.query(Users).all()
    cars = session.query(Cars).all()

    return {"users": users, "cars": cars}


@app.post("/car", response_model=CarSchema)
async def create_car(
    car_data: CarSchema, s_and_u: Tuple[Session, DBUser] = Depends(get_session)
) -> JSONResponse:

    session, db_user = s_and_u

    session.execute("SET search_path TO dummy, public;")

    car = Cars(**car_data.dict())
    session.add(car)

    session.commit()

    return car


@app.get("/car", response_model=List[CarSchema])
async def get_list_of_cars(
    s_and_u: Tuple[Session, DBUser] = Depends(get_session)
) -> JSONResponse:

    session, db_user = s_and_u

    cars = session.query(Cars).all()

    return cars
