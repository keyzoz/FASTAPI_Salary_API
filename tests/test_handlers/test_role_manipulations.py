
from uuid import uuid4

import pytest

from db.models import PortalRole
from tests.conftest import create_user_auth_headers_for_user


@pytest.mark.asyncio
async def test_add_admin_role_to_user_by_superuser(
    client, create_user_in_database, get_user_from_database
):
    user_data_for_updating = {
        "user_id": uuid4(),
        "login": "testuser",
        "name": "testuser",
        "surname": "testuser",
        "email": "testuser@gmail.com",
        "is_active": True,
        "hashed_password": "hashed_pass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    superuser_data = {
        "user_id": uuid4(),
        "login": "superuser",
        "name": "superuser",
        "surname": "superuser",
        "email": "superuser@gmail.com",
        "is_active": True,
        "hashed_password": "hashed_pass",
        "roles": [PortalRole.ROLE_PORTAL_SUPERUSER],
    }
    await create_user_in_database(**superuser_data)
    await create_user_in_database(**user_data_for_updating)
    resp = client.patch(
        f"/user/admin_privilege?user_id={user_data_for_updating['user_id']}",
        headers=create_user_auth_headers_for_user(superuser_data["login"]),
    )
    data_from_resp = resp.json()
    assert resp.status_code == 200
    updated_user_from_db = await get_user_from_database(
        data_from_resp["updated_user_id"]
    )
    assert len(updated_user_from_db) == 1
    updated_user_from_db = dict(updated_user_from_db[0])
    assert updated_user_from_db["user_id"] == user_data_for_updating["user_id"]
    assert PortalRole.ROLE_PORTAL_ADMIN in updated_user_from_db["roles"]

