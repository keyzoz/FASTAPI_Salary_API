import json
import pytest

from tests.conftest import create_user_auth_headers_for_user



@pytest.mark.asyncio
async def test_create_user(client, get_user_from_database):
    user_data = {
        "name": "testcreateuser",
        "login": "test1",
        "surname": "testcreateuser",
        "email": "testcreateuser@gmail.com",
        "password": "password",
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


@pytest.mark.asyncio
async def test_create_salary_info(client, get_user_from_database, get_salary_info_from_database):
    user_data = {
        "name": "testcreateuser",
        "login": "test1",
        "surname": "testcreateuser",
        "email": "testcreateuser@gmail.com",
        "password": "password",
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()

    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])

    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]

    salary_info = {
        "user_id": data_from_resp["user_id"],
        "salary": 300,
        "next_salary_increase": "2022-12-12"
    }
    resp = client.post(
        "/user/salary", data=json.dumps(salary_info),
        headers=create_user_auth_headers_for_user(user_data["login"])
    )
    data_from_resp = resp.json()

    assert resp.status_code == 200
    assert data_from_resp["salary"] == salary_info["salary"]
    assert data_from_resp["next_salary_increase"] == salary_info["next_salary_increase"]
    assert str(data_from_resp["user_id"]) == salary_info["user_id"]
    salary_infos_from_db = await get_salary_info_from_database(data_from_resp["salary_id"])

    assert len(salary_infos_from_db) == 1
    salary_info_from_db = dict(salary_infos_from_db[0])
    assert salary_info_from_db["salary"] == str(salary_info["salary"])
    assert salary_info_from_db["next_salary_increase"] == salary_info["next_salary_increase"]
    assert str(salary_info_from_db["user_id"]) == salary_info["user_id"]
    assert str(salary_info_from_db["salary_id"]) == data_from_resp["salary_id"]
