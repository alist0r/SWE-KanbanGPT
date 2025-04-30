from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from utils.database import Base

# Users Table
class User(Base):
    __tablename__ = 'Users'

    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(50), nullable=False)

    projects = relationship("Project", back_populates="creator")
    tasks_created = relationship("Task", back_populates="creator")
    assignments = relationship(
        "Assignment",
        back_populates="assignee",
        foreign_keys="Assignment.AssigneeID"
    )

    assigned_tasks = relationship(
        "Assignment",
        back_populates="assigned_by_user",
        foreign_keys="Assignment.AssignedBy"
    )

    comments = relationship("Comment", back_populates="user")


# Projects Table
class Project(Base):
    __tablename__ = 'Projects'

    ProjectID = Column(Integer, primary_key=True, autoincrement=True)
    Creator = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    description = Column(String)  # TEXT equivalent
    dateCreated = Column(DateTime(timezone=False), server_default=func.now())
    title = Column(String(40), nullable=False)

    creator = relationship("User", back_populates="projects")
    columns = relationship("ProjectColumn", back_populates="project")
    ai_responses = relationship("AITaskDirection", back_populates="project")


# Columns Table
class ProjectColumn(Base):
    __tablename__ = 'ProjectColumns'

    ColumnID = Column(Integer, primary_key=True, autoincrement=True)
    ProjectID = Column(Integer, ForeignKey('Projects.ProjectID'), nullable=False)
    title = Column(String(40), nullable=False)

    project = relationship("Project", back_populates="columns")
    tasks = relationship("Task", back_populates="column")


# Tasks Table
class Task(Base):
    __tablename__ = 'Tasks'

    TaskID = Column(Integer, primary_key=True, autoincrement=True)
    ColumnID = Column(Integer, ForeignKey('ProjectColumns.ColumnID'), nullable=False)
    CreatedBy = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    title = Column(String(40), nullable=False)
    description = Column(String)
    dateCreated = Column(DateTime(timezone=False), server_default=func.now())

    column = relationship("ProjectColumn", back_populates="tasks")
    creator = relationship("User", back_populates="tasks_created")
    assignments = relationship("Assignment", back_populates="task")
    comments = relationship("Comment", back_populates="task")
    ai_response = relationship("AITaskDirection", back_populates="task")

# Assignments Table
class Assignment(Base):
    __tablename__ = 'assignments'

    AssignmentID = Column(Integer, primary_key=True, autoincrement=True)
    TaskID = Column(Integer, ForeignKey('Tasks.TaskID'), nullable=False)
    AssigneeID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    AssignedBy = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    dateAssigned = Column(DateTime(timezone=False), server_default=func.now())

    task = relationship("Task", back_populates="assignments")
    assignee = relationship(
        "User",
        foreign_keys=[AssigneeID],
        back_populates="assignments"
    )

    assigned_by_user = relationship(
        "User",
        foreign_keys=[AssignedBy],
        back_populates="assigned_tasks"
    )


# Comments Table
class Comment(Base):
    __tablename__ = 'Comments'

    CommentID = Column(Integer, primary_key=True, autoincrement=True)
    TaskID = Column(Integer, ForeignKey('Tasks.TaskID'), nullable=False)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    dateCommented = Column(DateTime(timezone=False), server_default=func.now())
    text = Column(String, nullable=False)

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")


class AITaskDirection(Base):
    __tablename__ = 'aiTaskDirections'

    responseID = Column(Integer, primary_key=True, autoincrement=True)
    projectID = Column(Integer, ForeignKey('Projects.ProjectID'), nullable=False)
    taskID = Column(Integer, ForeignKey('Tasks.TaskID'), nullable=False)
    response = Column(Text, nullable=False)
    createdAt = Column(DateTime, server_default=func.now())

    project = relationship("Project", back_populates="ai_responses")
    task = relationship("Task", back_populates="ai_response")


class ProjectHasUsers(Base):
    __tablename__ = 'projectHasUsers'

    ProjectID = Column(Integer, ForeignKey('Projects.ProjectID', ondelete='CASCADE'), primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID', ondelete='CASCADE'), primary_key=True)
    # dateAssigned = Column(DateTime(timezone=False), server_default=func.now())

    project = relationship("Project", backref="project_members")
    user = relationship("User", backref="user_projects")