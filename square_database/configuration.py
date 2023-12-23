import configparser
import os

config = configparser.ConfigParser()
config_file_path = (
        os.path.dirname(os.path.abspath(__file__)) + os.sep + "data" + os.sep + "config.ini"
)
config.read(config_file_path)

module_name = "square_database"
databases_folder_name = "databases"

# get all vars and typecast

config_str_host_ip = config.get("ENVIRONMENT", "HOST_IP")
config_int_host_port = int(config.get("ENVIRONMENT", "HOST_PORT"))
config_str_db_ip = config.get("ENVIRONMENT", "DB_IP")
config_int_db_port = int(config.get("ENVIRONMENT", "DB_PORT"))
config_str_db_username = config.get("ENVIRONMENT", "DB_USERNAME")
config_str_db_password = config.get("ENVIRONMENT", "DB_PASSWORD")
config_str_log_file_name = config.get("ENVIRONMENT", "LOG_FILE_NAME")
config_bool_create_schema = config.get("ENVIRONMENT", "CREATE_SCHEMA")
config_database_module_name = config.get("ENVIRONMENT", "DATABASE_MODULE_NAME")
