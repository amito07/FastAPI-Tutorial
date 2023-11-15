from dotenv import dotenv_values
import logging
from fastapi import FastAPI
from tortoise import Tortoise,run_async
from tortoise.contrib.fastapi import register_tortoise

config = dotenv_values(".env")

log = logging.getLogger("uvicorn")

TORTOISE_MODELS = ["aerich.models","app.models.table1"]

TORTOISE_ORM = {
    "connection":{"default": "postgres://postgres:123@127.0.0.1/nest?schema=fastapi"},
    "apps":{
        "models":{
            "models": TORTOISE_MODELS,
            "default_connection": "default"
        }
    }
}

def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url="postgres://postgres:123@127.0.0.1/nest?schema=fastapi",
        modules={"models": TORTOISE_MODELS},
        generate_schemas=False,
        add_exception_handlers=True
    )
