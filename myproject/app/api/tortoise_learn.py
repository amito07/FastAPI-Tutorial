from fastapi import APIRouter, HTTPException, Query, Body, Path, status
from app.models.table1 import test_table
from app.models.relationaldb import Tournament, Event
from app.schemas.test_schema import TestModel, TournamentModel
from app.utils.exception import UserException
from tortoise.query_utils import Prefetch
from tortoise import connections

router = APIRouter(prefix="/api/v1/parameter", tags=["tortoise_orm"])


# get request
@router.get("/new/get-query")
async def get_query():
    data = await test_table.get_or_create(name="Supriti", phone_number=1412662716)
    return data

#single create request

@router.post("/single-create")
async def single_create(request: TestModel):
    if request.name[0].isupper():
        data = {
            "name":request.name,
            "phone_number": request.phone_number
        }
        await test_table.create(**data)
        return {"message": "Created successfully"}
    else:
        raise UserException('User name cannot start with a lower case')

#update request

@router.patch("/update-value/{id}")
async def update_value(request: TestModel, id: int):
    await test_table.filter(id=id).update(name=request.name, phone_number=request.phone_number)
    return {"message": "Updated successfully"}

#Delete request

@router.delete("/delete-valie/{id}")
async def delete_valie(id: int):
    await test_table.filter(id=id).delete()
    return {"message": "Deleted successfully"}

#Get User by id
@router.get("/get-user/{id}")
async def get_user(id: int):
    user_info = await test_table.filter(id=id)
    if not user_info:
        raise HTTPException(status_code = 404, detail = f'User not found with id {id}')
    return {"user": user_info}


@router.post("/create-tournament")
async def create_tournament(payload: TournamentModel):
    try:
        tournament = await Tournament.create(name = payload.tournament_name)
        if not tournament:
            raise HTTPException (status_code = 500, detail ="Internal server error")
        else:
            await Event.create(name= payload.event_name, tournament=tournament) 
        return {"message": "Tournament created successfully"}
    except Exception as e:
        raise HTTPException (status_code = 500, detail = f"Internal server error {e}")


@router.get('/get-tournament-info')
async def get_tournament_info():
    try:
        tournament_with_filter = await Tournament.all().prefetch_related(Prefetch("events", queryset = Event.filter(name = "Phase 1")))
        for tournament in tournament_with_filter:
            print(f"Tournament ID: {tournament.id}, Tournament Name: {tournament.name}")
            print("Events:")
            for event in tournament.events:
                print(f"  Event ID: {event.id}, Event Name: {event.name}")
            print("-" * 20)
        return {"message": "Fetch Successfully", "data": tournament_with_filter}
    
    except Exception as e:
        raise HTTPException (status_code = 500, detail= f"Internal server error {e}")
    

@router.get("/get-event/id")
async def get_event(id: int):
    conn = connections.get("default") 
    try:
        event = await conn.execute_query_dict(f'select * from event e where e.id = {id}')
        return {"message": "fetched successfully", "data": event}
    except Exception as e:
        raise HTTPException (status_code = 500, detail= f"Internal server {e}")

        
