from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm.decl_api import registry

# For relationships!
# from sqlalchemy.orm import relationship


mapper_registry = registry()


@mapper_registry.mapped
class Users:

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)


@mapper_registry.mapped
class Cars:

    __tablename__ = "cars"

    car_id = Column(Integer, primary_key=True)
    brand = Column(String)
    model = Column(String)
    is_available = Column(Boolean, default=False)
