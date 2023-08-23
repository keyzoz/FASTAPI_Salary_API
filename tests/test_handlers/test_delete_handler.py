from uuid import uuid4

import pytest

from db.dals import PortalRole
from tests.conftest import create_user_auth_headers_for_user


@pytest.mark.asyncio
async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "login": "test1",
        "name": "testdeleteuser",
        "surname": "testdeleteuser",
        "email": "testdeleteuser@gmail.com",
        "hashed_password": "hashed_pass",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER, ],
    }
    await create_user_in_database(**user_data)
    resp = client.delete(
        f"/user/?user_id={user_data['user_id']}",
        headers=create_user_auth_headers_for_user(user_data["login"]),
    )
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


@pytest.mark.parametrize(
    "user_role_list",
    [
        [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_ADMIN],
    ],
)
@pytest.mark.asyncio
async def test_delete_user_by_roles(client, create_user_in_database, get_user_from_database, user_role_list):
    user_data_for_deletion = {
        "user_id": uuid4(),
        "login": "test1",
        "name": "testuser",
        "surname": "testuser",
        "email": "testuser@gmail.com",
        "hashed_password": "hashed_pass",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER, ],
    }
    user_data = {
        "user_id": uuid4(),
        "login": "Admin",
        "name": "Admin",
        "surname": "Admin",
        "email": "admin@gmail.com",
        "hashed_password": "hashed_pass",
        "is_active": True,
        "roles": user_role_list,
    }
    await create_user_in_database(**user_data_for_deletion)
    await create_user_in_database(**user_data)
    resp = client.delete(
        f"/user/?user_id={user_data_for_deletion['user_id']}",
        headers=create_user_auth_headers_for_user(user_data["login"]),
    )
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data_for_deletion["user_id"])}
    users_from_db = await get_user_from_database(user_data_for_deletion["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_for_deletion["name"]
    assert user_from_db["surname"] == user_data_for_deletion["surname"]
    assert user_from_db["email"] == user_data_for_deletion["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data_for_deletion["user_id"]


@pytest.mark.parametrize(
    "user_for_deletion, user_who_delete",
    [
        (
            {
                "user_id": uuid4(),
                "login": "userfordelete",
                "name": "userfordelete",
                "surname": "userfordelete",
                "email": "userfordelete@gmail.com",
                "is_active": True,
                "hashed_password": "hashedpass",
                "roles": [PortalRole.ROLE_PORTAL_USER],
            },
            {
                "user_id": uuid4(),
                "login": "Admin",
                "name": "Admin",
                "surname": "Admin",
                "email": "admin@gmail.com",
                "is_active": True,
                "hashed_password": "hashedpass",
                "roles": [PortalRole.ROLE_PORTAL_USER],
            },
        ),
        (
            {
                "user_id": uuid4(),
                "login": "userfordelete",
                "name": "userfordelete",
                "surname": "userfordelete",
                "email": "userfordelete@gmail.com",
                "is_active": True,
                "hashed_password": "hashedpass",
                "roles": [
                    PortalRole.ROLE_PORTAL_USER,
                    PortalRole.ROLE_PORTAL_SUPERUSER,
                ],
            },
            {
                "user_id": uuid4(),
                "login": "Admin",
                "name": "Admin",
                "surname": "Admin",
                "email": "admin@gmail.com",
                "is_active": True,
                "hashed_password": "hashedpass",
                "roles": [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_ADMIN],
            },
        ),
        (
            {
                "user_id": uuid4(),
                "login": "userfordelete",
                "name": "userfordelete",
                "surname": "userfordelete",
                "email": "userfordelete@gmail.com",
                "is_active": True,
                "hashed_password": "hashedpass",
                "roles": [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_ADMIN],
            },
            {
                "user_id": uuid4(),
                "login": "Admin",
                "name": "Admin",
                "surname": "Admin",
                "email": "admin@gmail.com",
                "is_active": True,
                "hashed_password": "hashedpass",
                "roles": [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_ADMIN],
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_another_user_error(client, create_user_in_database, get_user_from_database,
                                        user_who_delete, user_for_deletion):
    await create_user_in_database(**user_for_deletion)
    await create_user_in_database(**user_who_delete)
    resp = client.delete(
        f"/user/?user_id={user_for_deletion['user_id']}",
        headers=create_user_auth_headers_for_user(user_who_delete["login"]),
    )
    assert resp.status_code == 403




