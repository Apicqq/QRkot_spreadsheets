from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate
from app.core.constants import ErrConstants as Err


async def check_name_is_busy(name: str, session: AsyncSession) -> None:
    """
    Check if the project with the given name already exists in the database.

    :param name: Incoming project name.
    :param session: The async session for the database.
    :raises HTTPException: if the project with the given name already exists.
    :returns: None
    """
    project_id = await charity_crud.get_project_id_by_name(name, session)
    if project_id is not None:
        raise HTTPException(HTTPStatus.BAD_REQUEST, Err.NAME_IS_BUSY)


async def check_has_investment(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """
    Check if the project has already been invested in.
    :param project_id: ID of the project.
    :param session: The async session for the database.
    :return: CharityProject - The project.
    :raises HTTPException: if the project has already been invested in, or
     if the project does not exist.
    """
    project: CharityProject = await charity_crud.get(project_id, session)
    if project is None:
        raise HTTPException(HTTPStatus.BAD_REQUEST, Err.NOT_FOUND)
    if project.invested_amount:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, Err.CANNOT_DELETE_PROJECT_WITH_INVESTMENTS
        )
    return project


async def check_eligible_for_patching(
    project_id, data_in: CharityProjectUpdate, session: AsyncSession
) -> CharityProject:
    """
    Check if the project can be patched. Return it if it is possible,
     raise HTTPException otherwise.
    :param project_id: ID of the project.
    :param data_in: The data to patch the project with.
    :param session: The async session for the database.
    :return: CharityProject - The project, if it is eligible to patch.
    :raises HTTPException: if the project cannot be patched.
    """
    project: CharityProject = await charity_crud.get(project_id, session)
    if project is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, Err.NOT_FOUND)
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, Err.CANNOT_MODIFY_CLOSED_PROJECT
        )
    if data_in.full_amount and data_in.full_amount < project.invested_amount:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, Err.FULL_AMOUNT_LT_INVESTED_AMOUNT
        )
    if data_in.name != project.name:
        await check_name_is_busy(data_in.name, session)
    return project
