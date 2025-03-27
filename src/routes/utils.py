## Description: Routes utilities.

from sqlalchemy.orm import Session
from src.database.connect import ConnectDatabase

from src.settings import Settings

def get_session_db() -> Session:
    settings = Settings()
    connection_dabatabase = ConnectDatabase(
        dbms=settings.database.db_dbms,
        username=settings.database.db_username,
        password=settings.database.db_password.get_secret_value(),
        host=settings.database.db_host,
        port=settings.database.db_port,
        database=settings.database.db_database
    )
    return Session(connection_dabatabase.get_engine())
