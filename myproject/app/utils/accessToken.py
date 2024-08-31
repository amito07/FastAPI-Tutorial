from fastapi import APIRouter, HTTPException, Query, Path, Body, File, UploadFile, Depends, Header, FastAPI, status
from datetime import datetime, timedelta
from jose import  jwt
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithm="HS256")
    return encoded_jwt

def middleware_validation(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithms=["HS256"])
        if payload:
            return True
        else:
            raise credentials_exception
    except Exception as e:
        raise credentials_exception

