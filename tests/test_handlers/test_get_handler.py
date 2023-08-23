from uuid import uuid4

import pytest

from db.dals import PortalRole
from tests.conftest import create_user_auth_headers_for_user


@pytest.mark.asyncio
async def test_get_user_by_id(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "testgetuserbyid",
        "surname": "testgetuserbyid",
        "email": "testgetuserbyid@gmail.com",
        "is_active": True,
        "hashed_password": "hashed_pass",
        "login": "test1",
        "roles": [PortalRole.ROLE_PORTAL_USER, ],
    }
    await create_user_in_database(**user_data)
    resp = client.get(
        f"/user/?user_id={user_data['user_id']}",
        headers=create_user_auth_headers_for_user(user_data["login"]),
    )
    assert resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["name"] == user_data["name"]
    assert user_from_response["surname"] == user_data["surname"]
    assert user_from_response["email"] == user_data["email"]
    assert user_from_response["is_active"] is True
    assert user_from_response["user_id"] == str(user_data["user_id"])
