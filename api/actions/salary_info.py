from uuid import UUID

from api.schemas import SalaryInfoCreate, ShowSalaryInfo
from db.dals import UserDAL


async def _create_new_salary_info(body: SalaryInfoCreate, db) -> ShowSalaryInfo:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            salary_info = await user_dal.create_salary_info(
                user_id=body.user_id,
                salary=body.salary,
                next_salary_increase=body.next_salary_increase
            )
            return ShowSalaryInfo(
                salary_id=salary_info.salary_id,
                user_id=salary_info.user_id,
                salary=salary_info.salary,
                next_salary_increase=salary_info.next_salary_increase
            )


async def _get_salary_info_by_user_id(user_id, db) -> ShowSalaryInfo | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            salary_info = await user_dal.get_salary_info_by_user_id(user_id=user_id)
            if salary_info is not None:
                return salary_info


async def _get_salary_info_by_salary_id(salary_id, db) -> ShowSalaryInfo | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            salary_info = await user_dal.get_salary_info_by_salary_id(salary_id=salary_id)
            if salary_info is not None:
                return salary_info


async def _update_salary_info(updated_user_params: dict, salary_id: UUID, db) -> UUID | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_salary_id = await user_dal.update_salary_info(
                salary_id=salary_id,
                **updated_user_params
            )
            return updated_salary_id


async def _delete_salary_info(salary_id, db) -> UUID | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_salary_info_id = await user_dal.delete_salary_info(
                salary_id=salary_id,
            )
            return deleted_salary_info_id
