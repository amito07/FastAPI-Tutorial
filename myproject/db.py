from dotenv import dotenv_values
import logging
from fastapi import FastAPI
from tortoise import Tortoise,run_async
from tortoise.contrib.fastapi import register_tortoise

config = dotenv_values(".env")

print(config)

log = logging.getLogger("uvicorn")

TORTOISE_MODELS = ["aerich.models","app.models.table1", "app.models.relationaldb"]

TORTOISE_ORM = {
    "connection":{"default": "postgres://amit:bayxStduOSd8pGu5fVpdJTQF8HW1A0i5@dpg-cls4pb3ip8as73a38bag-a.singapore-postgres.render.com/testdb_mv96?schema=test_db"},
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
        db_url="postgres://amit:bayxStduOSd8pGu5fVpdJTQF8HW1A0i5@dpg-cls4pb3ip8as73a38bag-a.singapore-postgres.render.com/testdb_mv96?schema=test_db",
        modules={"models": TORTOISE_MODELS},
        generate_schemas=False,
        add_exception_handlers=True
    )
