from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    email: str = Field(nullable=False, max_length=255, regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    #username: Optional[str] = None


class UserSignup(UserBase):
    password: str = Field(default=None, min_length=8, max_length=255)


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
    projects: List["Project"] = Relationship(
        back_populates="user", )

class UserResponse(UserBase):
    role: int = Field(default=0)

class ProjectCount(SQLModel):
    live_count: Optional[int] = None
    draft_count: Optional[int] = None
    total_count: Optional[int] = None


class UserInfo(UserBase):
    id: UUID
    created_at: datetime
    email: Optional[str] = None
    #username: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[int] = None
    projects_counts: Optional[ProjectCount] = None


class UserInfoInProject(SQLModel):
    username: Optional[str] = None


class UserUpdate(SQLModel):
    #email: Optional[str] = None
    password: str | None = Field(min_length=8, max_length=255)
    role: int | None = None


class Token(SQLModel):
    access_token: str
    token_type: str
    email: str
    role: int
    expires_at: datetime


class CategoryCreate(SQLModel):
    categoryName: str = Field(min_length=1)


class CategoryBase(SQLModel):
    categoryId: int = Field(primary_key=True, nullable=False)
    categoryName: str


class CategoryUpdate(CategoryBase):
    CategoryId: Optional[int] = None
    categoryName: Optional[str] = None


class Category(CategoryBase, table=True):
    __tablename__ = 'categories'

    tags: List["Tag"] = Relationship(
        back_populates="category")


class CategoryWithTags(CategoryBase):
    tags: List["Tag"] = []


class project_tags(SQLModel, table=True):
    project_id: UUID = Field(foreign_key="projects.id",
                             primary_key=True,
                             nullable=False)
    tag_id: int = Field(foreign_key="tags.tagId",
                        primary_key=True,
                        nullable=False)


class TagCreate(SQLModel):
    tagName: str = Field(min_length=1)
    tagNameShort: str | None = None
    categoryId: int


class TagBase(SQLModel):
    tagId: int
    tagName: str
    tagNameShort: str
    categoryId: int


class TagUpdate(SQLModel):
    tagName: str | None = Field(min_length=1)
    tagNameShort: str | None = Field(min_length=1)
    categoryId: int | None = None


class Tag(TagBase, table=True):
    __tablename__ = 'tags'
    tagId: int = Field(primary_key=True, nullable=False)
    categoryId: int = Field(default=None, foreign_key="categories.categoryId")
    projects: List["Project"] = Relationship(
        back_populates="tags",
        link_model=project_tags)
    category: Category = Relationship(
        back_populates="tags")


class TagCount(SQLModel):
    tag: Optional[Tag]
    count: int


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
    user: User = Relationship(back_populates="projects"
                              )
    tags: List["Tag"] = Relationship(
        back_populates="projects",
        link_model=project_tags)


class ProjectWithUserAndTags(SQLModel):
    id: UUID
    title: str
    link: str
    description: str
    is_live: bool
    is_featured: bool
    visit_count: int
    date: datetime
    user: Optional[UserInfoInProject] = None
    tags: List["Tag"] = []


class ProjectFull(ProjectWithUserAndTags):
    content: str


class ProjectFeatured(ProjectBase):
    id: UUID
    tags: List["Tag"] = []
    date: datetime

class UserBasicInfo(UserBase):
    id: UUID

class ProjectInfo(BaseModel):
    id: UUID
    title: str
    link: str
    description: str
    date: datetime
    tags: List["Tag"] = []

class ProjectInfoAdditional(ProjectInfo):
    is_live: bool
    is_featured: bool

class ProjectInfoAdditionalAdmin(ProjectInfoAdditional):
    visit_count: int
    user: UserBasicInfo

class ProjectContent(ProjectInfo):
    content: str

class ProjectContentAdditional(ProjectInfoAdditional):
    content: str

class ProjectContentAdditionalAdmin(ProjectInfoAdditionalAdmin):
    content: str

ProjectWithUserAndTags.update_forward_refs()
CategoryWithTags.update_forward_refs()
