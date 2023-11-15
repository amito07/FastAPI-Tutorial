from pydantic import BaseModel

class TestModel(BaseModel):
    name: str
    phone_number: int

