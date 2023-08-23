from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from uuid import UUID

from api.actions.auth import get_current_user_from_token
from api.actions.salary_info import _create_new_salary_info, _get_salary_info_by_user_id, _update_salary_info, \
    _get_salary_info_by_salary_id, _delete_salary_info
from api.actions.user import _create_new_user, _get_user_by_id, check_user_permissions, _delete_user, \
    _update_user
from api.schemas import UserCreate, UpdateUser, ShowUser, DeleteUserResponse, UpdatedUserResponse, ShowSalaryInfo, \
    SalaryInfoCreate, UpdatedSalaryInfoResponse, UpdateSalaryInfo, DeleteSalaryInfoResponse
from db.models import User, PortalRole
from db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}"
        )


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
        user_id: UUID, db: AsyncSession = Depends(get_db), cur_user: User = Depends(get_current_user_from_token),
):
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found."
        )
    if PortalRole.ROLE_PORTAL_SUPERUSER in cur_user.roles:
        raise HTTPException(status_code=406, detail="Superuser can't be deleted using API")
    if not check_user_permissions(target_user=user, cur_user=cur_user):
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )

    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
        user_id: UUID, db: AsyncSession = Depends(get_db), cur_user: User = Depends(get_current_user_from_token),
):
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found."
        )
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID,
        body: UpdateUser, db: AsyncSession = Depends(get_db),
        cur_user: User = Depends(get_current_user_from_token),
):
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail=f"At least one parameter for user update info should be provided"
        )

    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found."
        )

    if user_id != cur_user.user_id:
        if not check_user_permissions(target_user=user, cur_user=cur_user):
            raise HTTPException(
                status_code=403,
                detail="Forbidden."
            )

    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, db=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}"
        )
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.patch("/admin_privilege", response_model=UpdatedUserResponse)
async def give_admin_privilege(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    cur_user: User = Depends(get_current_user_from_token),
):

    if not cur_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )
    if cur_user.user_id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot manage privileges of itself."
        )
    user_for_promotion = await _get_user_by_id(user_id, db)
    if user_for_promotion.is_admin or user_for_promotion.is_superuser:
        raise HTTPException(
            status_code=409,
            detail=f"User with id {user_id} already promoted to admin / superuser.",
        )
    if user_for_promotion is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found."
        )
    updated_user_params = {
        "roles": user_for_promotion.add_admin_privileges_for_user()
    }

    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, db=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}"
        )
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.post("/salary", response_model=ShowSalaryInfo)
async def create_salary_info(
        body: SalaryInfoCreate, cur_user: User = Depends(get_current_user_from_token),
        db: AsyncSession = Depends(get_db)):

    user = await _get_user_by_id(body.user_id, db)
    if not check_user_permissions(target_user=user, cur_user=cur_user):
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )
    if user.is_active is False:
        raise HTTPException(
            status_code=403,
            detail=f"User with id {body.user_id} is deactivated."
        )
    try:
        return await _create_new_salary_info(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}"
        )


@user_router.get("/salary", response_model=ShowSalaryInfo)
async def get_salary_info_of_current_user(
    db: AsyncSession = Depends(get_db), cur_user: User = Depends(get_current_user_from_token),
):
    salary_info = await _get_salary_info_by_user_id(cur_user.user_id, db)
    if salary_info is None:
        raise HTTPException(
            status_code=404,
            detail=f"Your salary info not found ( user_id = {cur_user.user_id} ). "
        )
    return salary_info


@user_router.patch("/salary", response_model=UpdatedSalaryInfoResponse)
async def update_salary_info_by_salary_id(
        salary_id: UUID,
        body: UpdateSalaryInfo, db: AsyncSession = Depends(get_db),
        cur_user: User = Depends(get_current_user_from_token),
):
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail=f"At least one parameter for user update info should be provided"
        )

    salary_info = await _get_salary_info_by_salary_id(salary_id, db)
    if salary_info is None:
        raise HTTPException(
            status_code=404,
            detail=f"Salary info with id {salary_id} not found."
        )

    user = await _get_user_by_id(salary_info.user_id, db)
    if not check_user_permissions(target_user=user, cur_user=cur_user):
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )

    try:
        updated_salary_id = await _update_salary_info(
            updated_user_params=updated_user_params, db=db, salary_id=salary_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}"
        )
    return UpdatedSalaryInfoResponse(updated_salary_id=updated_salary_id)


@user_router.delete("/salary", response_model=DeleteSalaryInfoResponse)
async def delete_salary_info(
        salary_id: UUID, db: AsyncSession = Depends(get_db), cur_user: User = Depends(get_current_user_from_token),
):
    salary_info = await _get_salary_info_by_salary_id(salary_id, db)
    if salary_info is None:
        raise HTTPException(
            status_code=404,
            detail=f"Salary info with id {salary_id} not found."
        )
    user = await _get_user_by_id(salary_info.user_id, db)
    if not check_user_permissions(target_user=user, cur_user=cur_user):
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )

    deleted_salary_id = await _delete_salary_info(salary_id, db)
    if deleted_salary_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"Salary with id {salary_id} not found."
        )
    return DeleteSalaryInfoResponse(deleted_salary_id=deleted_salary_id)
