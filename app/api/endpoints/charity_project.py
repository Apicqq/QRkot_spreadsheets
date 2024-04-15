from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_has_investment,
    check_name_is_busy,
    check_eligible_for_patching,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_crud, donation_crud
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investments import run_investments

router = APIRouter()


@router.get("/", response_model=list[CharityProjectDB])
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
) -> list[CharityProject]:
    """
    Retrieve all charity projects from the database. Available to everyone.
    """
    projects = await charity_crud.get_all(session)
    return projects


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """
    Create a new charity project. Available only to superusers.
    """
    await check_name_is_busy(project.name, session)
    new_project = await charity_crud.create(project, session, skip_commit=True)
    unclosed = await donation_crud.get_unclosed_objects(session)
    if unclosed:
        invested = run_investments(new_project, unclosed)
        session.add_all(invested)
    await charity_crud.push_to_db(new_project, session)
    return new_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """
    Delete a charity project by it's id. Available only to superusers.
    """
    project = await check_has_investment(project_id, session)
    return await charity_crud.delete(project, session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """
    Update a charity project. Available only to superusers.
    """
    project = await check_eligible_for_patching(project_id, obj_in, session)
    project = await charity_crud.patch(
        project, obj_in, session, skip_commit=True
    )
    unclosed = await donation_crud.get_unclosed_objects(session)
    if unclosed:
        invested = run_investments(project, unclosed)
        session.add_all(invested)
    await charity_crud.push_to_db(project, session)
    return project
