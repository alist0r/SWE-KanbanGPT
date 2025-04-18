from sqlalchemy.orm import Session
from models.models import User, ProjectColumn

import re



def is_valid_username(username: str) -> bool:
    """Must be >= 8 characters and only contain letters and numbers."""
    return bool(re.fullmatch(r'[a-zA-Z0-9]{8,32}', username))

def is_valid_password(password: str) -> bool:
    """6-12 chars, at least one letter, one number, and one special character."""
    if not 6 <= len(password) <= 255:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[^A-Za-z0-9]', password):
        return False
    return True

def is_valid_name(name: str) -> bool:
    """Check if name contains only letters and spaces and is not empty."""
    return bool(re.fullmatch(r'[A-Za-z ]+', name))

def is_valid_email_format(email: str) -> bool:
    """Basic format check."""
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

def validate_user_exists(db: Session, user_id: int):
    return db.query(User).filter(User.UserID == user_id).first() is not None

def validate_column_exists(db: Session, column_id: int):
    return db.query(ProjectColumn).filter(ProjectColumn.ColumnID == column_id).first() is not None

def validate_task_title(title: str):
    return isinstance(title, str) and 0 < len(title) <= 40

def validate_description(description: str):
    return isinstance(description, str) and len(description.strip()) > 0