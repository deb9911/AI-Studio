from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from sqlalchemy.dialects.sqlite import JSON as SQLITE_JSON

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(default="user")  # "user" | "admin" | "superuser"

    config: "UserConfig" = Relationship(back_populates="user")

class UserConfig(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    data: dict = Field(sa_column=Column(SQLITE_JSON), default={})

    user: User = Relationship(back_populates="config")
    