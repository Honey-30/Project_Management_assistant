"""Database models for the Project Management Assistant."""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base

class ProjectStatus(enum.Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RiskLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationStatus(enum.Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"

class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    VIEWER = "viewer"

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="member", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    profile_picture = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    projects_owned = relationship("Project", back_populates="owner", foreign_keys="Project.owner_id")
    tasks_assigned = relationship("Task", back_populates="assignee", foreign_keys="Task.assignee_id")
    team_memberships = relationship("TeamMember", back_populates="user")
    ai_interactions = relationship("AIInteraction", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

# Project model
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="planning", nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)
    budget = Column(Float, nullable=True)
    spent_budget = Column(Float, default=0.0, nullable=False)
    progress = Column(Integer, default=0, nullable=False)  # Percentage 0-100
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="projects_owned", foreign_keys=[owner_id])
    tasks = relationship("Task", back_populates="project")
    teams = relationship("Team", back_populates="project")
    reports = relationship("Report", back_populates="project")
    risks = relationship("Risk", back_populates="project")

# Team model
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="teams")
    members = relationship("TeamMember", back_populates="team")

# Team membership model
class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), default="member", nullable=False)
    joined_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")

# Task model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="todo", nullable=False)
    priority = Column(String(50), default="medium", nullable=False)
    start_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    estimated_hours = Column(Float, nullable=True)
    actual_hours = Column(Float, default=0.0, nullable=False)
    progress = Column(Integer, default=0, nullable=False)  # Percentage 0-100
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks_assigned", foreign_keys=[assignee_id])
    parent_task = relationship("Task", remote_side=[id])
    subtasks = relationship("Task", remote_side=[parent_task_id])

# AI Interaction model
class AIInteraction(Base):
    __tablename__ = "ai_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    context = Column(JSON, nullable=True)  # Store conversation context
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="ai_interactions")

# Report model
class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    report_type = Column(String(100), nullable=False)  # e.g., 'progress', 'budget', 'risk'
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    data = Column(JSON, nullable=True)  # Store structured report data
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="reports")

# Notification model
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="unread", nullable=False)
    notification_type = Column(String(100), nullable=False)  # e.g., 'task_assigned', 'deadline_approaching'
    related_id = Column(Integer, nullable=True)  # ID of related entity (task, project, etc.)
    related_type = Column(String(100), nullable=True)  # Type of related entity
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="notifications")

# Risk model
class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    level = Column(String(50), nullable=False)
    probability = Column(Float, nullable=False)  # 0.0 to 1.0
    impact = Column(Float, nullable=False)  # 0.0 to 1.0
    mitigation_strategy = Column(Text, nullable=True)
    status = Column(String(100), default="identified", nullable=False)  # identified, mitigated, realized
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    identified_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    identified_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="risks")