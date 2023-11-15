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
