import logging
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    log_level: str = "DEBUG"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.database_username}:{self.database_password}@{self.database_hostname}:{self.database_port}/{self.database_name}"

    class Config:
        env_file = ".env"

settings: Settings = Settings() # type: ignore

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)