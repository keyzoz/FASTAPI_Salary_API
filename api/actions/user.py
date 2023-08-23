from uuid import UUID

from fastapi import HTTPException

from api.schemas import UserCreate, ShowUser
from db.dals import UserDAL, PortalRole
from db.models import User
from hashing import Hasher


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                login=body.login,
                name=body.name,
                surname=body.surname,
                email=body.email,
                hashed_password=Hasher.get_password_hash(body.password),
                roles=[PortalRole.ROLE_PORTAL_USER, ]
            )
            return ShowUser(
                login=body.login,
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


async def _update_user(updated_user_params: dict, user_id: UUID, db) -> UUID | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_user_id = await user_dal.update_user(
                user_id=user_id,
                **updated_user_params
            )
            return updated_user_id


async def _delete_user(user_id, db) -> UUID | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(
                user_id=user_id,
            )
            return deleted_user_id


async def _get_user_by_id(user_id, db) -> User | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id=user_id)
            if user is not None:
                return user


def check_user_permissions(target_user: User, cur_user: User) -> bool:

    if target_user.user_id != cur_user.user_id:
        if not {
            PortalRole.ROLE_PORTAL_ADMIN,
            PortalRole.ROLE_PORTAL_SUPERUSER,
        }.intersection(cur_user.roles):
            return False

        if PortalRole.ROLE_PORTAL_SUPERUSER in target_user.roles and PortalRole.ROLE_PORTAL_ADMIN in cur_user.roles:
            return False

        if PortalRole.ROLE_PORTAL_ADMIN in target_user.roles and PortalRole.ROLE_PORTAL_ADMIN in cur_user.roles:
            return False

    return True
