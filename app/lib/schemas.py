from pydantic import Field, BaseModel


class CarSchema(BaseModel):

    brand: str
    model: str
    is_available: bool

    class Config:
        orm_mode = True
