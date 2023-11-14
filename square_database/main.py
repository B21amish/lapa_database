from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from square_logger.main import SquareLogger
from uvicorn import run

from square_database.configuration import (
    config_int_host_port,
    config_str_host_ip,
    config_str_log_file_name, config_bool_create_schema
)
from square_database.create_database import create_database_and_tables

local_object_square_logger = SquareLogger(config_str_log_file_name)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@local_object_square_logger.async_auto_logger
async def root():
    return {"text": "hello"}


if __name__ == "__main__":
    try:
        if config_bool_create_schema:
            create_database_and_tables()

        run(app, host=config_str_host_ip, port=config_int_host_port)

    except Exception as exc:
        local_object_square_logger.logger.critical(exc, exc_info=True)
