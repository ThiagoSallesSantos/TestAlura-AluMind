## Description: This is the settings file for the application.

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, BaseModel, EmailStr

class APPSettings(BaseModel):
    app_host: str
    app_port: int
    app_debug: bool

class DatabaseSettings(BaseModel):
    db_dbms: str 
    db_username: str
    db_password: SecretStr
    db_host:str
    db_port: int
    db_database: str

class EmailSettings(BaseModel):
    email_email: EmailStr
    email_password: SecretStr
    email_model: str
    email_api_key: SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__"
    ) 
    version: str
    application: APPSettings
    database: DatabaseSettings
    email: EmailSettings
