from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    expiration_time: int

    class Config:
        env_file = ".env" 

settings = Settings()