import logging
from dotenv import dotenv_values
from fastapi import FastAPI, Request
from pydantic import BaseModel
from db import init_db
from app.api import testapi
from app.api import parameter
from app.api import tortoise_learn
from app.utils.exception import UserException
from fastapi.responses import JSONResponse

config = dotenv_values(".env")
log = logging.getLogger('uvicorn')


def create_application() -> FastAPI:
    _app = FastAPI(title="Test Fast API", version="1.0.0", description="GGWP")
    _app.include_router(testapi.router)
    _app.include_router(parameter.router)
    _app.include_router(tortoise_learn.router)

    return _app


app = create_application()

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



