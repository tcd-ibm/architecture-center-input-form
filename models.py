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
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    hashed_password: str = None
    password_version: int = Field(default=0)
    id: UUID = Field(default=None)
    is_active: bool = Field(default=True)
    role: int = Field(default=0)
    projects: List["Project"] = Relationship(back_populates="user")


class UserInfo(UserBase):
    id: UUID
    email: str
    username: Optional[str] = None
    is_active: bool


class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None


class Token(SQLModel):
    access_token: str
    token_type: str


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


class ProjectUpdate(ProjectBase):
    is_live: bool


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
    email: str
    title: str
    link: str
    description: str
    is_live: bool
    date: datetime
    user: UserInfo | None = None
    tags: List["Tag"] = []


class ProjectFull(ProjectWithUserAndTags):
    content: str


ProjectWithUserAndTags.update_forward_refs()
CategoryWithTags.update_forward_refs()
