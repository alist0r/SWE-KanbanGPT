from fastapi.testclient import TestClient

from main import app

# for testing user/task functionality
from models.models import User, Task, AITaskDirection
from utils.database import SessionLocal
from typing import Optional

client = TestClient(app)

# Utility function for getting specific user
def get_user_id_by_email(email: str) -> Optional[int]:
    db = SessionLocal()
    try:
        db.expire_all()  # optional, ensures DB freshness
        user = db.query(User).filter(User.email == email).first()
        return user.UserID if user else None
    finally:
        db.close()

# Utility function for getting jwt token associated with user
def get_jwt_token(username: str, password: str) -> str:
    response = client.post(
        "/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# Utility functions for clearing DB after tests
def clear_db():
    db = SessionLocal()
    db.query(AITaskDirection).delete()
    db.query(Task).delete()
    db.query(User).delete()
    db.commit()
    db.close()

# Run clear_db before and after tests
def setup_function():
    clear_db()

def teardown_function():
    clear_db()

# ===============
# Test connection
# ===============

def test_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.text == '"Pong"'

# =====================
# Test Cases for /users
# =====================

# UC1 All fields valid
def test_create_user_success():
    response = client.post(
        "/api/users",
        json={
            "username": "testuser",
            "password": "P@ssword1",
            "email": "testuser@example.com",
            "name": "Test User"
        },
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

# UC2 Email incorrect format
def test_create_user_invalid_email():
    response = client.post(
        "/api/users",
        json={
            "username": "validuser",
            "password": "P@ssword1",
            "email": "invalid-email",
            "name": "User"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format."

# UC3 Username incorrect format (too short)
def test_create_user_invalid_username_short():
    response = client.post(
        "/api/users",
        json={
            "username": "u1",
            "password": "P@ssword1",
            "email": "user@example.com",
            "name": "Invalid User"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username must be between 8 and 32 characters and alphanumeric."

# UC4 Username incorrect format (too long)
def test_create_user_invalid_username_long():
    response = client.post(
        "/api/users",
        json={
            "username": "averyverylongusernamethatexceedslimit",
            "password": "P@ssword1",
            "email": "user@example.com",
            "name": "Invalid User"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username must be between 8 and 32 characters and alphanumeric."

# UC5 Password incorrect format (too short, missing special chars, digit)
def test_create_user_invalid_password_short():
    response = client.post(
        "/api/users",
        json={
            "username": "validuser1",
            "password": "simple",  # No special char, no digit
            "email": "validuser@example.com",
            "name": "Valid User"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be 6–12 characters with at least one letter, number, and special character."

# UC6 Password incorrect format (too long)
def test_create_user_invalid_password_long():
    response = client.post(
        "/api/users",
        json={
            "username": "validuser1",
            "password": "a"*256,  # too long
            "email": "validuser@example.com",
            "name": "Valid User"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be 6–12 characters with at least one letter, number, and special character."

# UC7 Empty fields
def test_create_user_missing_fields():
    response = client.post(
        "/api/users",
        json={
            "username": "missingfieldsuser"
            # Missing password, email, and name
        },
    )
    assert response.status_code == 422

# UC8 Duplicate Email
def test_create_user_duplicate_email():
    client.post(
        "/api/users",
        json={
            "username": "user1test",
            "password": "P@ssword1",
            "email": "duplicate@example.com",
            "name": "User One"
        },
    )
    response = client.post(
        "/api/users",
        json={
            "username": "user2test",
            "password": "P@ssword2",
            "email": "duplicate@example.com",
            "name": "User Two"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered."

# UC9 Duplicate Email
def test_create_user_duplicate_username():
    client.post(
        "/api/users",
        json={
            "username": "duplicateuser",
            "password": "P@ssword1",
            "email": "duplicate1@example.com",
            "name": "User One"
        },
    )
    response = client.post(
        "/api/users",
        json={
            "username": "duplicateuser",
            "password": "P@ssword2",
            "email": "duplicate2@example.com",
            "name": "User Two"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken."

# =====================
# Test Cases for /tasks
# =====================

# TC1 All fields valid
def test_create_task_success():
    # Create a user first
    response = client.post(
        "/api/users",
        json={
            "username": "taskuser",
            "password": "P@ssword1",
            "email": "taskuser@example.com",
            "name": "Task User"
        },
    )
    assert response.status_code == 201

    # Get JWT token
    token = get_jwt_token("taskuser", "P@ssword1")

    # Create project
    response = client.post(
        "/api/projects/",
        json={
            "title": "Project",
            "description": "This is a test project",
            "assigned_users": []
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check the project creation response
    response_data = response.json()
    print(response_data)
    
    # Assert status code for project creation
    assert response.status_code == 200
    assert "message" in response_data
    assert response_data["message"] == "Project created successfully"
    assert "project_id" in response_data

    # Extract project ID
    project_id = response_data["project_id"]

    # Get column ID for the task
    response = client.get(
        f"/api/projects/{project_id}/columns",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    columns = response.json()
    assert len(columns) > 0
    column_id = columns[0]["ColumnID"]

    # Create task
    response = client.post(
        "/api/tasks/",
        json={
            "ColumnID": column_id,
            "title": "My First Task",
            "description": "This is a test task"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Task created successfully"

# TC2 Title is empty
def test_create_task_empty_title():
    # Create a user first
    client.post(
        "/api/users",
        json={
            "username": "taskuser3",
            "password": "P@ssword1",
            "email": "taskuser3@example.com",
            "name": "Task User"
        },
    )

    # Get JWT token
    token = get_jwt_token("taskuser3", "P@ssword1")

    # Create project
    response = client.post(
        "/api/projects/",
        json={
            "title": "Project",
            "description": "This is a test project",
            "assigned_users": []
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check the project creation response
    response_data = response.json()
    print(response_data)
    
    # Assert status code for project creation
    assert response.status_code == 200
    assert "message" in response_data
    assert response_data["message"] == "Project created successfully"
    assert "project_id" in response_data

    # Extract project ID
    project_id = response_data["project_id"]

    # Get column ID for the task
    response = client.get(
        f"/api/projects/{project_id}/columns",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    columns = response.json()
    assert len(columns) > 0
    column_id = columns[0]["ColumnID"]

    # Create task
    response = client.post(
        "/api/tasks/",
        json={
            "ColumnID": column_id,
            "title": "", # Empty title!
            "description": "This is a test task"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid task title (max 40 characters)"

# TC 3-5 Have been revised from the report for sprint 3,
# as there is not priority, deadline, and assignees is a
# use case to be implemented in the future.

# TC3 Invalid Column
def test_create_task_column_not_found():
    # Create a user first
    client.post(
        "/api/users",
        json={
            "username": "taskuser2",
            "password": "P@ssword1",
            "email": "taskuser2@example.com",
            "name": "Task User"
        },
    )

    # Get JWT token
    token = get_jwt_token("taskuser2", "P@ssword1")

    # Create task
    response = client.post(
        "/api/tasks/",
        json={
            "ColumnID": 999,
            "title": "My First Task",
            "description": "This is a test task"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Column does not exist"

# TC4 Invalid Title
def test_create_task_invalid_title():
    # Create a user first
    client.post(
        "/api/users",
        json={
            "username": "taskuser3",
            "password": "P@ssword1",
            "email": "taskuser3@example.com",
            "name": "Task User"
        },
    )

    # Get JWT token
    token = get_jwt_token("taskuser3", "P@ssword1")

    # Create project
    response = client.post(
        "/api/projects/",
        json={
            "title": "Project",
            "description": "This is a test project",
            "assigned_users": []
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check the project creation response
    response_data = response.json()
    print(response_data)
    
    # Assert status code for project creation
    assert response.status_code == 200
    assert "message" in response_data
    assert response_data["message"] == "Project created successfully"
    assert "project_id" in response_data

    # Extract project ID
    project_id = response_data["project_id"]

    # Get column ID for the task
    response = client.get(
        f"/api/projects/{project_id}/columns",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    columns = response.json()
    assert len(columns) > 0
    column_id = columns[0]["ColumnID"]

    # Create task
    response = client.post(
        "/api/tasks/",
        json={
            "ColumnID": column_id,
            "title": "This title is way too long and exceeds 40 characters!",
            "description": "This is a test task"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid task title (max 40 characters)"

# TC5 Missing Fields
def test_create_task_missing_fields():
    # Create a user first
    client.post(
        "/api/users",
        json={
            "username": "taskuser3",
            "password": "P@ssword1",
            "email": "taskuser3@example.com",
            "name": "Task User"
        },
    )

    # Get JWT token
    token = get_jwt_token("taskuser3", "P@ssword1")

# Create project
    response = client.post(
        "/api/projects/",
        json={
            "title": "Project",
            "description": "This is a test project",
            "assigned_users": []
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check the project creation response
    response_data = response.json()
    print(response_data)
    
    # Assert status code for project creation
    assert response.status_code == 200
    assert "message" in response_data
    assert response_data["message"] == "Project created successfully"
    assert "project_id" in response_data

    # Extract project ID
    project_id = response_data["project_id"]

    # Get column ID for the task
    response = client.get(
        f"/api/projects/{project_id}/columns",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    columns = response.json()
    assert len(columns) > 0
    column_id = columns[0]["ColumnID"]

    # Create task
    response = client.post(
        "/api/tasks/",
        json={
            "ColumnID": column_id,
            # This request is missing title/ description fields!
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422

# =====================
# Test Cases for /login
# =====================

# LC1 Login with valid email
def test_login_with_valid_email():
    client.post("/api/users", json={
        "username": "loginuser",
        "password": "P@ssword1",
        "email": "loginuser@example.com",
        "name": "Login User"
    })

    response = client.post("/login", data={
        "username": "loginuser@example.com",
        "password": "P@ssword1"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

# LC2 Login with valid username
def test_login_with_valid_username():
    client.post("/api/users", json={
        "username": "loginuser",
        "password": "P@ssword1",
        "email": "loginuser@example.com",
        "name": "Login User"
    })

    response = client.post("/login", data={
        "username": "loginuser",
        "password": "P@ssword1"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

# LC3 Incorrect password
def test_login_with_incorrect_password():
    client.post("/api/users", json={
        "username": "loginuser",
        "password": "P@ssword1",
        "email": "loginuser@example.com",
        "name": "Login User"
    })

    response = client.post("/login", data={
        "username": "loginuser",
        "password": "WRONG"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}

# LC4 User does not exist
def test_login_with_nonexistant_user():
    response = client.post("/login", data={
        "username": "nonexistantuser",
        "password": "P@ssword1"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# LC5 Missing fields
def test_login_with_missing_fields():
    response = client.post("/login", data={
        "password": "P@ssword1"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 422

# ========================
# Test Cases for /projects
# ========================

# TC1 All fields valid
def test_create_project_success():
    # Create main user
    client.post(
        "/api/users",
        json={
            "username": "projectuser",
            "password": "P@ssword1",
            "email": "projectuser@example.com",
            "name": "Project User"
        },
    )

    # Create assigned user
    response = client.post(
        "/api/users",
        json={
            "username": "projectuser2",
            "password": "P@ssword2",
            "email": "projectuser2@example.com",
            "name": "Project User Two"
        },
    )
    user_id = response.json()["user_id"]

    # Get token for creator
    token = get_jwt_token("projectuser", "P@ssword1")

    # Create project
    response = client.post(
        "/api/projects/",
        json={
            "title": "Project",
            "description": "This is a test project",
            "assigned_users": [user_id]
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check the response
    response_data = response.json()
    print(response_data)
    
    # Assert status code
    assert response.status_code == 200

    # Additional assertion to check response message and user_id
    assert "message" in response_data
    assert response_data["message"] == "Project created successfully"
    assert "project_id" in response_data  # Assuming this is returned in the response

# TC2 Empty title
def test_create_project_empty_title():
    # Create main user
    client.post(
        "/api/users",
        json={
            "username": "projectuser",
            "password": "P@ssword1",
            "email": "projectuser@example.com",
            "name": "Project User"
        },
    )

    # Create assigned user
    response = client.post(
        "/api/users",
        json={
            "username": "projectuser2",
            "password": "P@ssword2",
            "email": "projectuser2@example.com",
            "name": "Project User Two"
        },
    )
    user_id = response.json()["user_id"]

    # Get token for creator
    token = get_jwt_token("projectuser", "P@ssword1")

    # Create project
    response = client.post(
        "/api/projects/",
        json={
            "title": "",
            "description": "This is a test project",
            "assigned_users": [user_id]
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check the response
    response_data = response.json()
    print(response_data)
    
    # Assert status code
    assert response.status_code == 400

# TC3 Title too long
def test_create_project_title_too_long():
    # Create main user
    client.post(
        "/api/users",
        json={
            "username": "projectuser",
            "password": "P@ssword1",
            "email": "projectuser@example.com",
            "name": "Project User"
        },
    )

    # Create assigned user
    response = client.post(
        "/api/users",
        json={
            "username": "projectuser2",
            "password": "P@ssword2",
            "email": "projectuser2@example.com",
            "name": "Project User Two"
        },
    )
    user_id = response.json()["user_id"]

    # Get token for creator
    token = get_jwt_token("projectuser", "P@ssword1")

    # Create project
    response = client.post(
        "/api/projects/",
        json={
            "title": "This Project Title is WAY too long to be entered, there ought to be an error!",
            "description": "This is a test project",
            "assigned_users": [user_id]
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check the response
    response_data = response.json()
    print(response_data)
    
    # Assert status code
    assert response.status_code == 400

# TC4 Missing fields
def test_create_project_missing_fields():
    # Create main user
    client.post(
        "/api/users",
        json={
            "username": "projectuser",
            "password": "P@ssword1",
            "email": "projectuser@example.com",
            "name": "Project User"
        },
    )

    # Create assigned user
    response = client.post(
        "/api/users",
        json={
            "username": "projectuser2",
            "password": "P@ssword2",
            "email": "projectuser2@example.com",
            "name": "Project User Two"
        },
    )
    user_id = response.json()["user_id"]

    # Get token for creator
    token = get_jwt_token("projectuser", "P@ssword1")

    # Create project
    response = client.post(
        "/api/projects/",
        json={
            "title": "Project",
            "assigned_users": [user_id]
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Check the response
    response_data = response.json()
    print(response_data)
    
    # Assert status code
    assert response.status_code == 422
