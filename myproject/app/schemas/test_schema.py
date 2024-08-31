from pydantic import BaseModel

class TestModel(BaseModel):
    name: str
    phone_number: int

class TournamentModel(BaseModel):
    tournament_name: str
    event_name: str

