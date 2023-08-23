from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import update, and_, select, delete

from db.models import User, SalaryInfo
from db.models import PortalRole


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, login: str, name: str, surname: str, email: str, hashed_password: str, roles: list[PortalRole]
    ) -> User:
        new_user = User(
            login=login,
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
            roles=roles
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> UUID | None:
        query = update(User).where(and_(User.user_id == user_id, User.is_active == True)).values(is_active=False). \
            returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_login(self, login: str) -> User | None:
        query = select(User).where(User.login == login)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id=UUID, **kwargs) -> UUID | None:
        query = update(User).where(and_(User.user_id == user_id, User.is_active == True)).values(kwargs) \
            .returning(User.user_id)
        res = await self.db_session.execute(query)
        update_user_row = res.fetchone()
        if update_user_row is not None:
            return update_user_row[0]

    async def create_salary_info(self, user_id: UUID, salary: str, next_salary_increase: str):
        new_salary_info = SalaryInfo(
            user_id=user_id,
            salary=salary,
            next_salary_increase=next_salary_increase,
        )
        self.db_session.add(new_salary_info)
        await self.db_session.flush()
        return new_salary_info

    async def get_salary_info_by_user_id(self, user_id: UUID) -> SalaryInfo | None:
        query = select(SalaryInfo).where(SalaryInfo.user_id == user_id)
        res = await self.db_session.execute(query)
        salary_info_row = res.fetchone()
        if salary_info_row is not None:
            return salary_info_row[0]

    async def get_salary_info_by_salary_id(self, salary_id: UUID) -> SalaryInfo | None:
        query = select(SalaryInfo).where(SalaryInfo.salary_id == salary_id)
        res = await self.db_session.execute(query)
        salary_info_row = res.fetchone()
        if salary_info_row is not None:
            return salary_info_row[0]

    async def update_salary_info(self, salary_id: UUID, **kwargs) -> UUID | None:
        query = update(SalaryInfo).where(SalaryInfo.salary_id == salary_id).values(kwargs) \
            .returning(SalaryInfo.salary_id)
        res = await self.db_session.execute(query)
        update_user_row = res.fetchone()
        if update_user_row is not None:
            return update_user_row[0]

    async def delete_salary_info(self, salary_id: UUID) -> UUID | None:
        query = delete(SalaryInfo).where(SalaryInfo.salary_id == salary_id).returning(SalaryInfo.salary_id)
        res = await self.db_session.execute(query)
        if res is not None:
            return salary_id
