# square_database

## about

database layer for my personal server.

## installation

> pip install square_database

## usage

### to add a new database

- add package in databases package with database name and run main.py file with config variable CREATE_SCHEMA = True.

### to add a new schema

- add package in databases/database_name package with schema name and run main.py file with config variable
  CREATE_SCHEMA = True.

### to add a new table

- create databases/database_name/schema_name/tables.py file if not already created.
- create class corresponding to your new table add in databases/database_name/schema_name/tables.py file and run main.py
  file with config variable CREATE_SCHEMA = True

### to add default data in table

- append row objects containing your default data to the data_to_insert list inside the
  databases/database_name/schema_name/tables.py file and run main.py
  file with config variable CREATE_SCHEMA = True

**do not forget to add new database_names, schema_names and/or table_names to pydantic_models/pydantic_models.py enums
to make it accessible through api calls.**

## configs

1. square_database\data\config.ini (can be created using square_database\data\config.example.ini)
2. square_logger\data\config.ini

## env

- python>=3.12.0

## changelog

### v0.0.1

- initial implementation.
- known bugs
    - creating engines everytime on fastapi route call is creating idle sessions.
    - auto increment constraint is being applied in database.

## Feedback is appreciated. Thank you!
