import logging
from dotenv import dotenv_values
from fastapi import FastAPI
from pydantic import BaseModel
from db import init_db
from app.api import testapi

config = dotenv_values(".env")
log = logging.getLogger('uvicorn')


def create_application() -> FastAPI:
    _app = FastAPI(title="Test Fast API", version="1.0.0", description="GGWP")
    _app.include_router(testapi.router)

    return _app


app = create_application()

@app.on_event("startup")
async def startup_event():
    log.info("Starting up....")
    init_db(app)
@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")


