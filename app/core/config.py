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
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    spreadsheet_dt_format: str = ConfigConst.SPREADSHEET_DT_FORMAT
    spreadsheet_range: str = ConfigConst.SPREADSHEET_RANGE
    report_title: str = ConfigConst.SPREADSHEET_REPORT_NAME
    google_drive_api_version: str = ConfigConst.GOOGLE_DRIVE_API_VERSION
    google_sheets_api_version: str = ConfigConst.GOOGLE_SHEETS_API_VERSION
    google_sheets_base_uri: str = ConfigConst.GOOGLE_SHEETS_BASE_URI

    class Config:
        env_file = ".env"


settings = Settings()
