import importlib
import json

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from square_logger.main import SquareLogger
from uvicorn import run

from square_database.configuration import (
    config_int_host_port,
    config_str_host_ip,
    config_str_log_file_name, config_bool_create_schema, config_int_db_port, config_str_db_ip, config_str_db_username,
    config_str_db_password, databases_folder_name, module_name
)
from square_database.create_database import create_database_and_tables, snake_to_capital_camel
from square_database.pydantic_models.pydantic_models import InsertRows, GetRows

local_object_square_logger = SquareLogger(config_str_log_file_name)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/insert_rows", status_code=status.HTTP_201_CREATED)
@local_object_square_logger.async_auto_logger
async def insert_rows(insert_rows_model: InsertRows):
    try:
        local_str_database_url = \
            (f'postgresql://{config_str_db_username}:{config_str_db_password}@'
             f'{config_str_db_ip}:{str(config_int_db_port)}/{insert_rows_model.database_name.value}')
        database_engine = create_engine(local_str_database_url)
        with (database_engine.connect() as database_connection):
            try:
                database_connection.execute(text(f"SET search_path TO {insert_rows_model.schema_name.value}"))

            except OperationalError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect schema name.")
            try:
                table_class_name = snake_to_capital_camel(insert_rows_model.table_name.value)
                table_module_path = \
                    (f'{module_name}.{databases_folder_name}.{insert_rows_model.database_name.value}'
                     f'.{insert_rows_model.schema_name.value}.{insert_rows_model.table_name.value}')
                table_module = importlib.import_module(table_module_path)
                table_class = getattr(table_module, table_class_name)
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect table name.")
            local_object_session = sessionmaker(bind=database_engine)
            session = local_object_session()
            try:
                return_this = []
                for row_dict in insert_rows_model.data:
                    new_row = table_class(**row_dict)
                    session.add(new_row)
                    session.commit()
                    session.refresh(new_row)
                    return_this.append(
                        {key: value for key, value in new_row.__dict__.items() if not key.startswith('_')})
                session.close()
                return JSONResponse(status_code=status.HTTP_201_CREATED,
                                    content=json.loads(json.dumps(return_this, default=str)))
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect database name.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/get_rows", status_code=status.HTTP_200_OK)
@local_object_square_logger.async_auto_logger
async def get_rows(get_rows_model: GetRows):
    try:
        local_str_database_url = \
            (f'postgresql://{config_str_db_username}:{config_str_db_password}@'
             f'{config_str_db_ip}:{str(config_int_db_port)}/{get_rows_model.database_name.value}')
        database_engine = create_engine(local_str_database_url)
        with (database_engine.connect() as database_connection):
            try:
                database_connection.execute(text(f"SET search_path TO {get_rows_model.schema_name.value}"))

            except OperationalError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect schema name.")
            try:
                table_class_name = snake_to_capital_camel(get_rows_model.table_name.value)
                table_module_path = \
                    (f'{module_name}.{databases_folder_name}.{get_rows_model.database_name.value}'
                     f'.{get_rows_model.schema_name.value}.{get_rows_model.table_name.value}')
                table_module = importlib.import_module(table_module_path)
                table_class = getattr(table_module, table_class_name)
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect table name.")
            local_object_session = sessionmaker(bind=database_engine)
            session = local_object_session()
            try:
                query = session.query(table_class)
                for key, value in get_rows_model.filters.items():
                    query = query.filter(getattr(table_class, key) == value)

                filtered_rows = query.all()
                local_list_filtered_rows = [{key: value for key, value in x.__dict__.items() if not key.startswith('_')}
                                            for x in filtered_rows]
                session.commit()
                session.close()

                return JSONResponse(status_code=status.HTTP_200_OK,
                                    content=json.loads(json.dumps(local_list_filtered_rows, default=str)))
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect database name.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/")
@local_object_square_logger.async_auto_logger
async def root():
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"text": "square_database"})


if __name__ == "__main__":
    try:
        if config_bool_create_schema:
            create_database_and_tables()

        run(app, host=config_str_host_ip, port=config_int_host_port)

    except Exception as exc:
        local_object_square_logger.logger.critical(exc, exc_info=True)
