import uuid
import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr
from datetime import date, datetime

VALIDATE_USER_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
date_format = '%Y-%m-%d'


class TunedModel(BaseModel):
    class Config:

        orm_mode = True


class UserCreate(TunedModel):
    login: str
    name: str
    surname: str
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value):
        if not VALIDATE_USER_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Name should contains only letters")
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not VALIDATE_USER_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Surname should contains only letters")
        return value


class SalaryInfoCreate(TunedModel):
    user_id: uuid.UUID
    salary: float | int
    next_salary_increase: str

    @validator("salary")
    def validate_salary(cls, value):
        if type(value) is int:
            salary = float(value)
            return salary
        return value

    @validator("next_salary_increase")
    def validate_next_salary_increase(cls, value):
        try:
            datetime.strptime(value, date_format)
        except ValueError:
            raise HTTPException(status_code=422, detail="Incorrect data format, should be YYYY-MM-DD")
        return value


class UpdateSalaryInfo(BaseModel):
    salary: float | None
    next_salary_increase: Optional[constr(min_length=1)]

    @validator("salary")
    def validate_salary(cls, value):
        if type(value) is int:
            salary = float(value)
            return salary
        return value

    @validator("next_salary_increase")
    def validate_next_salary_increase(cls, value):
        try:
            datetime.strptime(value, date_format)
        except ValueError:
            raise HTTPException(status_code=422, detail="Incorrect data format, should be YYYY-MM-DD")
        return value


class UpdateUser(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]

    @validator("name")
    def validate_name(cls, value):
        if not VALIDATE_USER_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Name should contains only letters")
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not VALIDATE_USER_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Surname should contains only letters")
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class ShowUser(TunedModel):
    user_id: uuid.UUID
    login: str
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class ShowSalaryInfo(TunedModel):
    salary_id: uuid.UUID
    user_id: uuid.UUID
    salary: float
    next_salary_increase: str


class UpdatedSalaryInfoResponse(BaseModel):
    updated_salary_id: uuid.UUID

class DeleteSalaryInfoResponse(BaseModel):
    deleted_salary_id: uuid.UUID
