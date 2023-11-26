from fastapi import APIRouter, HTTPException, Query, Path, Body, File, UploadFile, Depends, Header, FastAPI, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.table1 import test_table, user_table
from app.schemas.test_schema import TestModel
from enum import Enum
from typing import Annotated, List
from app.utils.exception import NormalException
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import dotenv_values



config = dotenv_values(".env")


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

#bulk create 
class Img_Url(BaseModel):
    url:str
    img_type: str
class UserInfo(BaseModel):
    name: str
    age: int
    phone_number: int
    img_url: Img_Url | None = None

@router.post("/create-bulk-user", summary="User can do bulk assignment")
async def bulk_create(payload: List[UserInfo]):
    try:
        user_instances = [user_table(
            name=user.name,
            age=user.age,
            phone_number=user.phone_number,
            img_url=user.img_url.model_dump() if user.img_url else None
        ) for user in payload]

        await user_table.bulk_create(user_instances)
        return {"message": "User created successfully"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=400, message="Something went wrong")


# #Auth Token Protected Route
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2a$12$A6.Qylauo83HPUKXEKK2ouOjNCve5tbp8SUOH6kF9Z.zonTkHzq.i",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2a$12$Z1ctru2aGGqsPACmdFiu3OGeifA9dPA73BPBh18ySiyttMgWO/K9q",
        "disabled": True,
    },
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserInfoV2(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(UserInfoV2):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")

def verify_password(plain_password, hashed_password):
    print("plain_password",plain_password)
    print("hashed_password",hashed_password)
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def fake_hash_password(password: str):
    return "fakehashed" + password 


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithm="HS256")
    return encoded_jwt

# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[UserInfoV2, Depends(get_current_user)]):
    print("current_user",current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes= 30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: Annotated[UserInfoV2, Depends(get_current_active_user)]):
    return current_user


