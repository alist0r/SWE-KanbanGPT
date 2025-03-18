from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from utils.database import Base  # Ensure Base is correctly imported

# Users Table
class User(Base):
    __tablename__ = 'Users'

    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed passwords
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(50), nullable=False)

    projects = relationship("Project", back_populates="creator")
    tasks_created = relationship("Task", back_populates="creator")
    assignments = relationship("Assignment", back_populates="assignee")
    comments = relationship("Comment", back_populates="user")


# Projects Table
class Project(Base):
    __tablename__ = 'Projects'

    ProjectID = Column(Integer, primary_key=True, autoincrement=True)
    Creator = Column(Integer, ForeignKey('Users.UserID'), nullable=False)  # ✅ Fixed case
    description = Column(String)  # TEXT equivalent
    dateCreated = Column(DateTime, default=datetime.utcnow)
    title = Column(String(40), nullable=False)

    creator = relationship("User", back_populates="projects")
    columns = relationship("Column", back_populates="project")


# Columns Table
class ProjectColumn(Base):
    __tablename__ = 'ProjectColumns'

    ColumnID = Column(Integer, primary_key=True, autoincrement=True)
    ProjectID = Column(Integer, ForeignKey('Projects.ProjectID'), nullable=False)  # ✅ Fixed case
    title = Column(String(40), nullable=False)

    project = relationship("Project", back_populates="columns")
    tasks = relationship("Task", back_populates="column")


# Tasks Table
class Task(Base):
    __tablename__ = 'Tasks'

    TaskID = Column(Integer, primary_key=True, autoincrement=True)
    ColumnID = Column(Integer, ForeignKey('ProjectColumns.ColumnID'), nullable=False)  # ✅ Fixed case
    CreatedBy = Column(Integer, ForeignKey('Users.UserID'), nullable=False)  # ✅ Fixed case
    title = Column(String(40), nullable=False)
    description = Column(String)  # TEXT equivalent
    dateCreated = Column(DateTime, default=datetime.utcnow)

    column = relationship("Column", back_populates="tasks")
    creator = relationship("User", back_populates="tasks_created")
    assignments = relationship("Assignment", back_populates="task")
    comments = relationship("Comment", back_populates="task")


# Assignments Table
class Assignment(Base):
    __tablename__ = 'Assignments'

    AssignmentID = Column(Integer, primary_key=True, autoincrement=True)
    TaskID = Column(Integer, ForeignKey('Tasks.TaskID'), nullable=False)  # ✅ Fixed case
    AssigneeID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)  # ✅ Fixed case
    AssignedBy = Column(Integer, ForeignKey('Users.UserID'), nullable=False)  # ✅ Fixed case
    dateAssigned = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="assignments")
    assignee = relationship("User", foreign_keys=[AssigneeID], back_populates="assignments")
    assigned_by = relationship("User", foreign_keys=[AssignedBy])


# Comments Table
class Comment(Base):
    __tablename__ = 'Comments'

    CommentID = Column(Integer, primary_key=True, autoincrement=True)
    TaskID = Column(Integer, ForeignKey('Tasks.TaskID'), nullable=False)  # ✅ Fixed case
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)  # ✅ Fixed case
    dateCommented = Column(DateTime, default=datetime.utcnow)
    text = Column(String, nullable=False)  # TEXT equivalent

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")
