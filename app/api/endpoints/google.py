from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.constants import ErrConstants as Econst
from app.core.exceptions import MaxColumnsLimitExceeded, MaxRowsLimitExceeded
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.services.google_api import (
    create_spreadsheet,
    set_user_permissions,
    spreadsheet_update_value,
)

router = APIRouter()


@router.post("/", dependencies=[Depends(current_superuser)])
async def get_charity_projects_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
):
    """Generate report with all closed charity projects to
    a Google spreadsheet.
    Superusers only.
    """
    projects = await charity_crud.get_projects_by_completion_rate(session)
    try:
        spreadsheet_id, spreadsheet_url = await create_spreadsheet(
            wrapper_service, projects
        )
    except (MaxRowsLimitExceeded, MaxColumnsLimitExceeded) as error:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, Econst.PROJECTS_LIMIT_REACHED.format(error)
        )
    await set_user_permissions(spreadsheet_id, wrapper_service)
    await spreadsheet_update_value(spreadsheet_id, wrapper_service, projects)
    return {"Your report at": f"{spreadsheet_url}"}
