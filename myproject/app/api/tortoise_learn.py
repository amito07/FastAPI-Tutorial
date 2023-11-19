from fastapi import APIRouter, HTTPException, Query, Body, Path
from app.models.table1 import test_table
from app.schemas.test_schema import TestModel

router = APIRouter(prefix="/api/v1/parameter", tags=["tortoise_orm"])


# get request
@router.get("/new/get-query")
async def get_query():
    data = await test_table.get_or_create(name="Supriti", phone_number=1412662716)
    return data

#single create request

@router.post("/single-create")
async def single_create(request: TestModel):
    data = {
        "name":request.name,
        "phone_number": request.phone_number
    }
    await test_table.create(**data)
    return {"message": "Created successfully"}

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



