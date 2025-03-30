DROP SCHEMA IF EXISTS `taskmanagement` ;
CREATE DATABASE TaskManagement;
USE TaskManagement;

-- Users Table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(32) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,  -- Store hashed password
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL
);

-- Projects Table
CREATE TABLE Projects (
    ProjectID INT AUTO_INCREMENT PRIMARY KEY,
    Creator INT NOT NULL,  -- FK to Users(UserID)
    description TEXT NOT NULL,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(40) NOT NULL,
    FOREIGN KEY (Creator) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Columns Table
CREATE TABLE ProjectColumns (
    ColumnID INT AUTO_INCREMENT PRIMARY KEY,
    ProjectID INT NOT NULL,  -- FK to Projects(ProjectID)
    title VARCHAR(40) NOT NULL,
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID) ON DELETE CASCADE
);

-- Tasks Table
CREATE TABLE Tasks (
    TaskID INT AUTO_INCREMENT PRIMARY KEY,
    ColumnID INT NOT NULL,  -- FK to Columns(ColumnID)
    CreatedBy INT NOT NULL,  -- FK to Users(UserID)
    title VARCHAR(40) NOT NULL,
    description TEXT NOT NULL,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ColumnID) REFERENCES ProjectColumns(ColumnID) ON DELETE CASCADE,
    FOREIGN KEY (CreatedBy) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Assignments Table
CREATE TABLE Assignments (
    AssignmentID INT AUTO_INCREMENT PRIMARY KEY,
    TaskID INT NOT NULL,  -- FK to Tasks(TaskID)
    AssigneeID INT NOT NULL,  -- FK to Users(UserID)
    AssignedBy INT NOT NULL,  -- FK to Users(UserID)
    dateAssigned DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID) ON DELETE CASCADE,
    FOREIGN KEY (AssigneeID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (AssignedBy) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Comments Table
CREATE TABLE Comments (
    CommentID INT AUTO_INCREMENT PRIMARY KEY,
    TaskID INT NOT NULL,  -- FK to Tasks(TaskID)
    UserID INT NOT NULL,  -- FK to Users(UserID)
    dateCommented DATETIME DEFAULT CURRENT_TIMESTAMP,
    text TEXT NOT NULL,
    FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID) ON DELETE CASCADE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);