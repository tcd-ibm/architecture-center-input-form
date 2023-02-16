from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    email: str = Field(default=None, primary_key=True)
    username: Optional[str] = None
    phone: Optional[str] = None


class UserSignup(UserBase):
    password: str = Field(default=None)


# table = True => in database
class Users(UserBase, table=True):
    phone: Optional[str] = None
    hashed_password: str = None
    id: UUID = Field(default=None)
    is_active: bool = Field(default=True)


class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None


class Token(SQLModel):
    access_token: str
    token_type: str


class Announcement(SQLModel, table=True):
    __tablename__ = 'AnnouncementList'
    aid: int = Field(primary_key=True, nullable=False)
    title: str = Field(max_length=255)
    titleLink: str = Field(max_length=255)
    date: str = Field(max_length=255)
    announcementType: str = Field(max_length=255)
    desc: str = Field(max_length=255)


class Detail(SQLModel, table=True):
    __tablename__ = 'DetailLink'
    ppid: int = Field(nullable=False)
    description: str = Field(max_length=255)
    url: str = Field(primary_key=True, max_length=255)
    type: str = Field(max_length=255)


class PA(SQLModel, table=True):
    __tablename__ = 'PAList'
    ppid: int = Field(primary_key=True)
    Heading: str = Field(max_length=255)
    Summary: str = Field(default=None)
    Product: str = Field(default=None)
    Solutions: str = Field(default=None)
    Vertical: str = Field(default=None)
    Image1Url: str = Field(default=None)
    ProductType: str = Field(default=None)
    DetailPage: str = Field(default=None)
    islive: bool = Field(default=False)
    isnew: bool = Field(default=True)
    metaDesc: str = Field(default=None)
    metaKeyword: str = Field(default=None)


class Product(SQLModel, table=True):
    __tablename__ = 'ProductList'
    pid: str = Field(primary_key=True)
    pname: str = Field(max_length=255)
    plink: str


class Solution(SQLModel, table=True):
    __tablename__ = 'SolutionList'
    sid: str = Field(primary_key=True)
    sname: str = Field(max_length=255)


class Type(SQLModel, table=True):
    __tablename__ = 'TypeList'
    tid: str = Field(primary_key=True)
    typename: str = Field(max_length=255)


class Vertical(SQLModel, table=True):
    __tablename__ = 'VerticalList'
    vid: str = Field(primary_key=True)
    vname: str = Field(max_length=255)
