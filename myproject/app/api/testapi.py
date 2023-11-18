from fastapi import APIRouter, HTTPException
from app.models.table1 import test_table
from app.schemas.test_schema import TestModel


router = APIRouter(prefix="/api/v1")

@router.post("/create", name="Create user", status_code=201)
async def create_user(request: TestModel):
    data = {
        "name":request.name,
        "phone_number": request.phone_number
    }

    await test_table.create(**data)
    return {"message": "Success"}

@router.get("/get-info", name="Get info", status_code=200)
async def get_user():
    data = await test_table.get()
    print(data)
    return {"message": "information", "data": data}

@router.patch("/update-user/{user_id}", name="Update user", status_code=200)
async def update_user(request: TestModel, user_id: int):
    new_data = {
        "name": request.name,
        "phone_number": request.phone_number

    }
    await test_table.update(user_id, new_data)

    return {"message": "successfully updated"}
