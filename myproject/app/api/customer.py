from fastapi import APIRouter, HTTPException, Query, Path, Body, File, UploadFile, Depends, Header, FastAPI, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.table1 import customer_table
from app.schemas.customer_schema import Customer_Model_SignUp, Customer_Model_SignIn
from enum import Enum
from typing import Annotated, List
from app.utils.exception import NormalException
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import dotenv_values
from app.utils.hashFunction import hash_function, verify_hash_function
from app.utils.accessToken import create_access_token , middleware_validation

router = APIRouter(prefix="/api/v1", tags=["Customer"])

@router.post("/sign-up/customer")
async def create_customer(payload: Customer_Model_SignUp):
    try:
        data = {
            "name": payload.name,
            "email": payload.email,
            "password": hash_function(payload.password)
        }
        print(data)
        await customer_table.create(**data)
        return {"Message": "Sucessfully Signed Up"}
    except Exception as e:
        print(f'Error {e}')

@router.post("/sign-in")
async def sign_in(payload: Customer_Model_SignIn):
    try: 
        get_user = await customer_table.get(email = payload.email)
        if get_user:
            if not verify_hash_function(payload.password, get_user.password):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            access_token_expires = timedelta(minutes= 30)
            access_token = create_access_token( data={"email": payload.email, "password": payload.password }, expires_delta=access_token_expires)
            print("access_token",access_token)
            return {"message": "success", "additional_info":{"email": payload.email, "token": access_token}}
        else:
            raise HTTPException(status_code=404, message="Wrong user or password")

    except Exception as e:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
    
@router.get("/get-customer/id")
async def get_customer(id:int, Bearer: str):
    try:
        payload = middleware_validation(Bearer)
        if payload:
            get_user_info = await customer_table.filter(id = id).values('name', 'email')
        return {"user-info": get_user_info}

    except Exception as e:
        print(f'Error {e}')




