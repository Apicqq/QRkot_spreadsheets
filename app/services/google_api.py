from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (
    UtilityConstants as Uconst,
    ErrConstants as Errconst,
)
from app.core.exceptions import MaxColumnsLimitExceeded, MaxRowsLimitExceeded

SPREADSHEET_DT_FORMAT = "%Y/%m/%d %H:%M:%S"


def get_spreadsheet_header(_datetime: str) -> list:
    return [
        ["Отчёт от", _datetime],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]


def get_spreadsheet_body(_datetime: str, rows: int, columns: int = 3) -> dict:
    return dict(
        properties=dict(
            title=f"Charity projects report from {_datetime}",
            locale="ru_RU",
        ),
        sheets=[
            dict(
                properties=dict(
                    sheetType="GRID",
                    sheetId=0,
                    title="Лист1",
                    gridProperties=dict(rowCount=rows, columnCount=columns),
                )
            )
        ],
    )


async def create_spreadsheet(
        wrapper_service: Aiogoogle, projects: list
) -> tuple[str, str]:
    service = await wrapper_service.discover("sheets", "v4")
    spreadsheet_body = get_spreadsheet_body(
        datetime.now().strftime(SPREADSHEET_DT_FORMAT),
        rows=len(projects) + len(get_spreadsheet_header("")),
        columns=max(map(len, get_spreadsheet_header(""))),
    )
    grid_properties = spreadsheet_body["sheets"][0]["properties"][
        "gridProperties"
    ]
    if grid_properties["rowCount"] >= Uconst.GOOGLE_SPREADSHEET_ROWS_LIMIT:
        raise MaxRowsLimitExceeded(
            Errconst.EXCEEDED_ROWS_AMOUNT.format(
                grid_properties["rowCount"],
            )
        )
    if (
            grid_properties["columnCount"] >=
            Uconst.GOOGLE_SPREADSHEET_COLUMNS_LIMIT
    ):
        raise MaxColumnsLimitExceeded(
            Errconst.EXCEEDED_COLUMNS_AMOUNT.format(
                grid_properties["columnCount"],
            )
        )
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response["spreadsheetId"], response["spreadsheetUrl"]


async def set_user_permissions(
        spreadsheet_id: str, wrapper_service: Aiogoogle
) -> None:
    permissions_body = {
        "role": "writer",
        "type": "user",
        "emailAddress": settings.email,
    }
    service = await wrapper_service.discover("drive", "v3")
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields="id"
        )
    )


async def spreadsheet_update_value(
        spreadsheet_id: str, wrapper_service: Aiogoogle, projects: list
) -> None:
    service = await wrapper_service.discover("sheets", "v4")
    table_values = [
        *get_spreadsheet_header(
            datetime.now().strftime(SPREADSHEET_DT_FORMAT)
        ),
        *[
            list(map(str, [title, timedelta(days=rate), description]))
            for title, rate, description in projects
        ],
    ]
    update_body = {"values": table_values, "majorDimension": "ROWS"}
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f"R1C1:"
                  f"R{len(table_values)}"
                  f"C{max(map(len, table_values))}",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
