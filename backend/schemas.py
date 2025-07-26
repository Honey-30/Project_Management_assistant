"""Pydantic schemas for API request and response models."""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

# Enums for API schemas
class UserRoleSchema(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    VIEWER = "viewer"

class ProjectStatusSchema(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskStatusSchema(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class TaskPrioritySchema(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RiskLevelSchema(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: UserRoleSchema = UserRoleSchema.MEMBER
    is_active: bool = True
    profile_picture: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRoleSchema] = None
    is_active: Optional[bool] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: ProjectStatusSchema = ProjectStatusSchema.PLANNING
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    deadline: Optional[datetime] = None
    budget: Optional[float] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatusSchema] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    deadline: Optional[datetime] = None
    budget: Optional[float] = None
    spent_budget: Optional[float] = None
    progress: Optional[int] = None

class Project(ProjectBase):
    id: int
    spent_budget: float
    progress: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatusSchema = TaskStatusSchema.TODO
    priority: TaskPrioritySchema = TaskPrioritySchema.MEDIUM
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = None
    parent_task_id: Optional[int] = None

class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatusSchema] = None
    priority: Optional[TaskPrioritySchema] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    progress: Optional[int] = None
    assignee_id: Optional[int] = None
    parent_task_id: Optional[int] = None

class Task(TaskBase):
    id: int
    actual_hours: float
    progress: int
    project_id: int
    assignee_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Team schemas
class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    project_id: int

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Team(TeamBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TeamMemberBase(BaseModel):
    role: UserRoleSchema = UserRoleSchema.MEMBER

class TeamMemberCreate(TeamMemberBase):
    team_id: int
    user_id: int

class TeamMember(TeamMemberBase):
    id: int
    team_id: int
    user_id: int
    joined_at: datetime

    class Config:
        from_attributes = True

# AI Interaction schemas
class AIInteractionBase(BaseModel):
    message: str
    project_id: Optional[int] = None

class AIInteractionCreate(AIInteractionBase):
    pass

class AIInteraction(AIInteractionBase):
    id: int
    user_id: int
    response: str
    context: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Report schemas
class ReportBase(BaseModel):
    title: str
    content: str
    report_type: str

class ReportCreate(ReportBase):
    project_id: int
    data: Optional[dict] = None

class Report(ReportBase):
    id: int
    project_id: int
    generated_by: int
    data: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Notification schemas
class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: str
    related_id: Optional[int] = None
    related_type: Optional[str] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseModel):
    status: str

class Notification(NotificationBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Risk schemas
class RiskBase(BaseModel):
    title: str
    description: str
    level: RiskLevelSchema
    probability: float
    impact: float
    mitigation_strategy: Optional[str] = None
    status: str = "identified"

class RiskCreate(RiskBase):
    project_id: int

class RiskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    level: Optional[RiskLevelSchema] = None
    probability: Optional[float] = None
    impact: Optional[float] = None
    mitigation_strategy: Optional[str] = None
    status: Optional[str] = None

class Risk(RiskBase):
    id: int
    project_id: int
    identified_by: int
    identified_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True