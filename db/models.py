from enum import Enum

from sqlalchemy import Column, Boolean, String, ForeignKey, ARRAY, FLOAT
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID

import uuid

Base = declarative_base()


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER",
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN",
    ROLE_PORTAL_SUPERUSER = "ROLE_PORTAL_SUPERUSER"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(String), nullable=False)

    salary_info = relationship("SalaryInfo", back_populates="user")

    @property
    def is_superuser(self) -> bool:
        return PortalRole.ROLE_PORTAL_SUPERUSER in self.roles

    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles

    def add_admin_privileges_for_user(self):
        if not self.is_admin:
            return {*self.roles, PortalRole.ROLE_PORTAL_ADMIN}


class SalaryInfo(Base):
    __tablename__ = "salary_info"

    salary_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), unique=True)
    salary = Column(FLOAT, nullable=False)
    next_salary_increase = Column(String, nullable=False)

    user = relationship("User", back_populates="salary_info")









