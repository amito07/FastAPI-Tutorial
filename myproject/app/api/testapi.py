from fastapi import APIRouter, HTTPException, Query, Path, Body, File, UploadFile, Depends
from app.models.table1 import test_table
from app.schemas.test_schema import TestModel
from enum import Enum
from typing import Annotated
from app.utils.exception import NormalException
from pydantic import BaseModel


router = APIRouter(prefix="/api/v1", tags=["Test"])

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

#ENUM example
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name.value == 'resnet':
        return {"model_name": model_name, "message": "LeCNN all the images"}
    else:
        return {"model_name": model_name, "message": "Another Model"}
    
#Query parameters example string validation
@router.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@router.get("/items/advance")
async def read_items(q: Annotated[str, Query(min_length=3, max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if len(q) < 3:
        raise NormalException('Word cannot be less than 3 characters')
    else:
        results.update({"q": q})
    return results

#Mix of Path, Query and Request body
@router.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: TestModel | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# Singular values in body
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@router.put("/item/{item_id}")
async def update_item(
    item_id: int, item: Annotated[Item, Body(embed=True)], user: Annotated[User, Body(embed=True)], importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


#description of payload example
class Amit(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }
@router.put("/amit-items/{item_id}")
async def update_item(item_id: int, item: Amit):
    results = {"item_id": item_id, "item": item}
    return results

#files API

@router.post("/files")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file}


#Class dependencies
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@router.post("/class-dependencies")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    response.update({"data":fake_items_db[commons.skip: commons.skip + commons.limit][0]["item_name"]})
    return response






