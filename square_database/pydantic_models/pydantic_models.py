from enum import Enum
from typing import List

from pydantic import BaseModel


class DatabasesEnum(str, Enum):
    file_storage = "file_storage"
    game = "game"


class TablesEnum(str, Enum):
    file = "file"
    game = "game"
    game_instance = "game_instance"


class SchemaEnum(str, Enum):
    public = "public"


class InsertRows(BaseModel):
    database_name: DatabasesEnum
    table_name: TablesEnum
    schema_name: SchemaEnum
    data: List[dict]


class GetRows(BaseModel):
    database_name: DatabasesEnum
    table_name: TablesEnum
    schema_name: SchemaEnum
    filters: dict


class EditRows(BaseModel):
    database_name: DatabasesEnum
    table_name: TablesEnum
    schema_name: SchemaEnum
    filters: dict
    data: dict


class DeleteRows(BaseModel):
    database_name: DatabasesEnum
    table_name: TablesEnum
    schema_name: SchemaEnum
    filters: dict
