import importlib
import os

from psycopg2.errors import DuplicateDatabase
from sqlalchemy import create_engine, text
from square_logger.main import SquareLogger

from square_database.configuration import config_str_db_ip, config_int_db_port, config_str_db_username, \
    config_str_db_password, config_str_log_file_name, databases_folder_name, module_name

local_object_square_logger = SquareLogger(config_str_log_file_name)


@local_object_square_logger.auto_logger
def create_database_and_tables():
    try:

        local_object_square_logger.logger.info(
            f"Creating databases, schemas and tables at database ip: {config_str_db_ip}:{config_int_db_port}.")

        local_list_database_names = [f for f in os.listdir(databases_folder_name) if
                                     os.path.isdir(os.path.join(databases_folder_name, f)) and f != "__pycache__"]

        for local_str_database_name in local_list_database_names:
            local_str_postgres_url = \
                (f'postgresql://{config_str_db_username}:{config_str_db_password}@'
                 f'{config_str_db_ip}:{str(config_int_db_port)}/')
            postgres_engine = create_engine(local_str_postgres_url)
            try:
                with postgres_engine.connect() as postgres_connection:
                    postgres_connection.execute(text("commit"))
                    postgres_connection.execute(text(f"CREATE DATABASE {local_str_database_name}"))
            except Exception as e:
                if isinstance(e.orig, DuplicateDatabase):
                    local_object_square_logger.logger.info(f"{local_str_database_name} already exists skipping.")
                else:
                    raise
            schema_folder_name = databases_folder_name + os.sep + local_str_database_name
            local_list_schema_names = [f for f in os.listdir(schema_folder_name) if
                                       os.path.isdir(os.path.join(schema_folder_name, f)) and f != "__pycache__"]

            local_str_database_url = \
                (f'postgresql://{config_str_db_username}:{config_str_db_password}@'
                 f'{config_str_db_ip}:{str(config_int_db_port)}/{local_str_database_name}')
            database_engine = create_engine(local_str_database_url)
            with (database_engine.connect() as database_connection):
                for local_str_schema_name in local_list_schema_names:
                    if not database_engine.dialect.has_schema(database_connection, local_str_schema_name):
                        database_connection.execute(text("commit"))
                        database_connection.execute(text(f"CREATE SCHEMA {local_str_schema_name}"))
                    else:
                        local_object_square_logger.logger.info(
                            f"{local_str_database_name}.{local_str_schema_name} already exists skipping.")
                    database_connection.execute(text(f"SET search_path TO {local_str_schema_name}"))
                    table_folder_name = (databases_folder_name + os.sep +
                                         local_str_database_name + os.sep + local_str_schema_name)
                    local_list_table_file_paths = [f for f in os.listdir(table_folder_name) if f != "__init__.py"
                                                   and not os.path.isdir(os.path.join(schema_folder_name, f))]
                    for local_str_table_file_path in local_list_table_file_paths:
                        local_str_table_name = ".".join(local_str_table_file_path.split(".")[0:-1])
                        table_class_name = local_str_table_name.capitalize()
                        table_module_path = \
                            (f'{module_name}.{databases_folder_name}'
                             f'.{local_str_database_name}.{local_str_schema_name}.{local_str_table_name}')
                        table_module = importlib.import_module(table_module_path)
                        table_class = getattr(table_module, table_class_name)

                        if not database_engine.dialect.has_table(database_connection, table_class.__tablename__):
                            table_class.__table__.create(database_connection)
                        else:
                            local_object_square_logger.logger.info(
                                f"{local_str_database_name}.{local_str_schema_name}.{local_str_table_name} "
                                f"already exists, skipping.")
                database_connection.execute(text("commit"))

    except Exception:
        raise
