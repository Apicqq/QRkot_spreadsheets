from typing import Optional

from pydantic import BaseSettings, EmailStr

from app.core.constants import ConfigConstants as ConfigConst


class Settings(BaseSettings):
    app_title: str = ConfigConst.APP_TITLE
    description: str = ConfigConst.DESCRIPTION
    database_url: str = ConfigConst.DATABASE_URL
    secret: str = ConfigConst.SECRET
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
