from enum import Enum, IntEnum


class ErrConstants(str, Enum):
    NAME_IS_BUSY = "This name is already occupied"
    NOT_FOUND = "Not Found"
    CANNOT_MODIFY_CLOSED_PROJECT = (
        "You cannot modify a project that was closed"
    )
    CANNOT_DELETE_PROJECT_WITH_INVESTMENTS = (
        "You cannot delete a project that has some investments"
    )
    FULL_AMOUNT_LT_INVESTED_AMOUNT = (
        "You cannot set full amount that is less" "than invested amount"
    )
    PASSWORD_TOO_SHORT = "Password should be at least 3 characters"
    EMAIL_IN_PASSWORD = "Password should not contain e-mail"
    PROJECTS_LIMIT_REACHED = ("Your query exceeded technical limit: {} of a "
                              "google spreadsheet, therefore it cannot be "
                              "processed. Please contact administrators.")


class DBConstants(Enum):
    INVESTED_AMOUNT_DEFAULT = 0
    CHARITY_PROJECT_NAME_DEFAULT = 100
    INVESTMENT_CONSTRAINT = "Initial investment value must be greater than 0"
    INVESTMENT_LT_FUL_AMOUNT_CONSTRAINT = (
        "Invested amount must be less than or equal to full amount"
    )
    INVESTED_AMOUNT_GE_ZERO = "Invested amount must not be a negative number"


class ConfigConstants(str, Enum):
    APP_TITLE = "QRKot"
    DESCRIPTION = "API for the Charity application QRKot cat support fund."
    DATABASE_URL = "sqlite+aiosqlite:///./CatCharityFund.db"
    SECRET = "VeryDamnSecretSecret"


class SchemaConstants(IntEnum):
    CHARITY_PROJ_FIELD_MIN_LENGTH = 1
    CHARITY_PROJ_FIELD_MAX_LENGTH = 100


class UtilityConstants(IntEnum):
    GOOGLE_SPREADSHEET_ROWS_LIMIT = 1_000_000_000
    GOOGLE_SPREADSHEET_COLUMNS_LIMIT = 18_278
    HEADER_ROWS_COUNT = 13  # 3 for the header and extra 10 for visual clarity
