import logging
from dotenv import dotenv_values
from fastapi import FastAPI, Request
from pydantic import BaseModel
from db import init_db
from app.api import testapi
from app.api import parameter
from app.api import tortoise_learn
from app.utils.exception import UserException, NormalException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time

config = dotenv_values(".env")
log = logging.getLogger('uvicorn')


def create_application() -> FastAPI:
    _app = FastAPI(title="Test Fast API", version="1.0.0", description="GGWP")
    _app.include_router(testapi.router)
    _app.include_router(parameter.router)
    _app.include_router(tortoise_learn.router)

    return _app


app = create_application()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print("GGGG",request)
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/gg")
async def read_root():
    return {"message": "Hello, World!"}

@app.on_event("startup")
async def startup_event():
    log.info("Starting up....")
    init_db(app)
@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")


#custom exception handler
@app.exception_handler(UserException)
def user_exception_handler(request: Request, exception: UserException):
    return JSONResponse(
        status_code = 418,
        content = {'detail': exception.name}
    )

@app.exception_handler(NormalException)
def normal_exception_handler(request: Request, exception: NormalException):
    return JSONResponse(
        status_code = 418,
        content = {'detail': exception.name}
    )



