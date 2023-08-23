import json
import uuid
from uuid import uuid4

import pytest

from db.dals import PortalRole
from tests.conftest import create_user_auth_headers_for_user


@pytest.mark.asyncio
async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "login": "test1",
        "name": "testuser",
        "surname": "testuser",
        "email": "testuser@gmail.com",
        "hashed_password": "hashed_pass",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER, ],
    }

    updated_user_data = {
        "name": "testuserupdated",
        "surname": "testuserupdated",
        "email": "testuserupdated@gmail.com",
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(updated_user_data),
        headers=create_user_auth_headers_for_user(user_data["login"]),
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == updated_user_data["name"]
    assert user_from_db["surname"] == updated_user_data["surname"]
    assert user_from_db["email"] == updated_user_data["email"]
    assert user_from_db["is_active"] == user_data["is_active"]
    assert str(user_from_db["user_id"]) == str(user_data["user_id"])

