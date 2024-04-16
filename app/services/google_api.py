from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import ConfigConstants


async def create_spreadsheet(wrapper_service: Aiogoogle) -> str:
    service = await wrapper_service.discover(
        "sheets", settings.google_sheets_api_version
    )
    spreadsheet_body = {
        "properties": {
            "title": settings.report_title.format(
                datetime.now().strftime(settings.spreadsheet_dt_format)
            )},
        "sheets": [{"properties": {"sheetType": "GRID",
                                   "sheetId": 0,
                                   "title": "Лист1",
                                   "gridProperties": {"rowCount": 100,
                                                      "columnCount": 11}
                                   }}]

    }
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_service: Aiogoogle
) -> None:
    permissions_body = {
        "role": "writer",
        "type": "user",
        "emailAddress": settings.email
    }
    service = await wrapper_service.discover(
        "drive", settings.google_drive_api_version
    )
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        )
    )


async def spreadsheet_update_value(
        spreadsheet_id: str,
        wrapper_service: Aiogoogle,
        charity_projects: list
) -> None:
    service = await wrapper_service.discover(
        "sheets", settings.google_sheets_api_version
    )
    table_values = [
        ["Отчёт от", datetime.now().strftime(
            ConfigConstants.SPREADSHEET_DT_FORMAT
        )],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"]
    ]
    for project in charity_projects:
        row = list(project)
        row[1] = str(timedelta(days=project[1]))
        table_values.append(row)
    update_body = {
        "values": table_values,
        "majorDimension": "ROWS"
    }
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=settings.spreadsheet_range,
            valueInputOption="USER_ENTERED",
            json=update_body
        )
    )
