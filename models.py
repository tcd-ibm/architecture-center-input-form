from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    email: str = Field(primary_key=True, nullable=False, max_length=255)
    username: Optional[str] = None


class UserSignup(UserBase):
    password: str = Field(default=None)


# table = True => in database
class User(UserBase, table=True):
    __tablename__ = 'users'
    hashed_password: str = None
    id: UUID = Field(default=None)
    is_active: bool = Field(default=True)
    role: int = Field(default=0)
    projects: List["Project"] = Relationship(back_populates="user")


class UserInfo(UserBase):
    email: str
    username: Optional[str] = None
    is_active: bool


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


class CategoryBase(SQLModel):
    categoryId: int = Field(primary_key=True, nullable=False)
    categoryName: str


class Category(CategoryBase, table=True):
    __tablename__ = 'categories'

    tags: List["Tag"] = Relationship(back_populates="category")


class CategoryWithTags(CategoryBase):
    tags: List["Tag"] = []


class project_tags(SQLModel, table=True):
    project_id: UUID = Field(foreign_key="projects.id", primary_key=True, nullable=False)
    tag_id: int = Field(foreign_key="tags.tagId", primary_key=True, nullable=False)


class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    tagId: int = Field(primary_key=True, nullable=False)
    tagName: str
    tagNameShort: str
    categoryId: int = Field(default=None, foreign_key="categories.categoryId")
    projects: List["Project"] = Relationship(back_populates="tags", link_model=project_tags)
    category: Category = Relationship(back_populates="tags")


class ProjectBase(SQLModel):
    title: str
    link: str
    description: str
    content: str
    date: datetime
    tags: List[int]  # tagId


class Project(ProjectBase, table=True):
    __tablename__ = 'projects'
    id: UUID = Field(primary_key=True, nullable=False)
    email: str = Field(foreign_key="users.email")
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_live: bool = Field(default=False)
    user: User = Relationship(back_populates="projects")
    tags: List["Tag"] = Relationship(back_populates="projects", link_model=project_tags)


class ProjectWithUserAndTags(SQLModel):
    id: UUID
    title: str
    link: str
    description: str
    is_live: bool
    date: datetime
    user: UserInfo | None = None
    tags: List["Tag"] = []


ProjectWithUserAndTags.update_forward_refs()
CategoryWithTags.update_forward_refs()
