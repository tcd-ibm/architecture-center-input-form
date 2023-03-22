from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    email: str = Field(nullable=False, max_length=255)
    username: Optional[str] = None


class UserSignup(UserBase):
    password: str = Field(default=None)


# table = True => in database
class User(UserBase, table=True):
    __tablename__ = 'users'
    id: UUID = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    hashed_password: str = None
    password_version: int = Field(default=0)
    is_active: bool = Field(default=True)
    role: int = Field(default=0)
    projects: List["Project"] = Relationship(back_populates="user")


class UserInfo(UserBase):
    id: UUID
    created_at: datetime
    email: str
    username: Optional[str] = None
    is_active: bool
    role: int


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
    tags: List[int]  # tagId


class ProjectUpdate(SQLModel):
    title: Optional[str]
    link: Optional[str]
    description: Optional[str]
    content: Optional[str]
    date: Optional[datetime]
    tags: Optional[List[int]]
    is_live: Optional[bool]


class Project(ProjectBase, table=True):
    __tablename__ = 'projects'
    id: UUID = Field(primary_key=True, nullable=False)
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_live: bool = Field(default=False)
    is_featured: bool = Field(default=False)
    visit_count: int = Field(default=0)
    user_id: UUID = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="projects")
    tags: List["Tag"] = Relationship(back_populates="projects", link_model=project_tags)


class ProjectWithUserAndTags(SQLModel):
    id: UUID
    title: str
    link: str
    description: str
    is_live: bool
    is_featured: bool
    visit_count: int
    date: datetime
    user: Optional[UserInfo] = None
    tags: List["Tag"] = []


class ProjectFull(ProjectWithUserAndTags):
    content: str


ProjectWithUserAndTags.update_forward_refs()
CategoryWithTags.update_forward_refs()
