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
    ppid: int = Field(primary_key=True)
    description: str = Field(max_length=255)
    url: str = Field(max_length=255)
    type: str = Field(max_length=255)


class PA(SQLModel, table=True):
    __tablename__ = 'PAList'
    ppid: int = Field(primary_key=True)
    Heading: str = Field(max_length=255)
    Summary: str = Field(max_length=255)
    Product: str = Field(max_length=255)
    Solutions: str = Field(max_length=255)
    Vertical: str = Field(max_length=255)
    Image1Url: str = Field(max_length=255)
    ProductType: str = Field(max_length=255)
    DetailPage: str = Field(max_length=255)
    metaDesc: str = Field(max_length=255)
    metaKeyword: str = Field(max_length=255)
    islive: bool = Field(default=True)
    isnew: bool = Field(default=True)


class Product(SQLModel, table=True):
    __tablename__ = 'ProductList'
    pid: int = Field(primary_key=True)
    pname: str = Field(max_length=255)
    plink: str = Field(max_length=255)


class Solution(SQLModel, table=True):
    __tablename__ = 'SolutionList'
    sid: int = Field(primary_key=True)
    sname: str = Field(max_length=255)


class Type(SQLModel, table=True):
    __tablename__ = 'TypeList'
    tid: int = Field(primary_key=True)
    typename: str = Field(max_length=255)


class Vertical(SQLModel, table=True):
    __tablename__ = 'VerticalList'
    vid: int = Field(primary_key=True)
    vname: str = Field(max_length=255)
