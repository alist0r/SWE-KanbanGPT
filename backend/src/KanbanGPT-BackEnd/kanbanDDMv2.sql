USE TaskManagement;

-- values for the 10 default users
INSERT INTO Users (username, password, email, name) VALUES ('Benjamin96', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user1@test.com', 'Ben');
INSERT INTO Users (username, password, email, name) VALUES ('Daniel45', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user2@test.com', 'Daniel');
INSERT INTO Users (username, password, email, name) VALUES ('Aaron345', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user3@test.com', 'Aaron');
INSERT INTO Users (username, password, email, name) VALUES ('AzizA3232', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user4@test.com', 'Aziz');
INSERT INTO Users (username, password, email, name) VALUES ('NorrisM9', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user5@test.com', 'Norris');
INSERT INTO Users (username, password, email, name) VALUES ('William8', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user6@test.com', 'William');
INSERT INTO Users (username, password, email, name) VALUES ('BlakeMAC45', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user7@test.com', 'Blake');
INSERT INTO Users (username, password, email, name) VALUES ('BradChicken52', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user8@test.com', 'Brad');
INSERT INTO Users (username, password, email, name) VALUES ('DaveMess12', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user9@test.com', 'Dave');
INSERT INTO Users (username, password, email, name) VALUES ('Craig999', '$2b$12$KarpdqoX6xuO7xp43AX9f.iPSGqJzPO9GmUOpK1sDT7zV9LclkLLq', 'user10@test.com', 'Craig');

-- values for 3 projects
INSERT INTO Projects (Creator, description, title) VALUES (8, 'Description for Alpha', 'Alpha');
INSERT INTO Projects (Creator, description, title) VALUES (7, 'Description for Beta', 'Beta');
INSERT INTO Projects (Creator, description, title) VALUES (6, 'Description for Charlie', 'Charlie');

-- values for the default project columns
INSERT INTO ProjectColumns (ProjectID, title) VALUES (1, 'Backlog');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (1, 'Assigned');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (1, 'In-Progress');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (1, 'Ready For Review');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (1, 'Complete');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (2, 'Backlog');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (2, 'Assigned');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (2, 'In-Progress');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (2, 'Ready For Review');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (2, 'Complete');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (3, 'Backlog');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (3, 'Assigned');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (3, 'In-Progress');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (3, 'Ready For Review');
INSERT INTO ProjectColumns (ProjectID, title) VALUES (3, 'Complete');

-- values for random tasks for the 3 projects. project 1 has 5 tasks, proj 2 has 3 tasks, and proj 3 has 5 tasks
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (2, 4, 'Task 1', 'Test description for task 1');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (2, 4, 'Task 2', 'Test description for task 2');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (4, 3, 'Task 3', 'Test description for task 3');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (4, 6, 'Task 4', 'Test description for task 4');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (3, 6, 'Task 5', 'Test description for task 5');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (7, 7, 'Task 6', 'Test description for task 6');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (10, 10, 'Task 7', 'Test description for task 7');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (7, 10, 'Task 8', 'Test description for task 8');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (11, 7, 'Task 9', 'Test description for task 9');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (13, 1, 'Task 10', 'Test description for task 10');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (12, 7, 'Task 11', 'Test description for task 11');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (12, 5, 'Task 12', 'Test description for task 12');
INSERT INTO Tasks (ColumnID, CreatedBy, title, description) VALUES (15, 7, 'Task 13', 'Test description for task 13');

-- defualt values for data responses representing the ai response from the project. we can make these actual responses if we need to for the project demo
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (1, 1, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (1, 2, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (1, 3, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (1, 4, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (1, 5, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (2, 6, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (2, 7, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (2, 8, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (3, 9, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (3, 10, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (3, 11, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (3, 12, 'This is test data response');
INSERT INTO aiTaskDirections (projectID, taskID, response) VALUES (3, 13, 'This is test data response');

-- default values for assigning tasks to a user.  We could add some more to this if we wanted one task to be assigned to multiple users
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (1, 1, 2);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (2, 4, 5);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (3, 4, 8);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (4, 6, 4);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (5, 6, 8);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (6, 1, 8);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (7, 6, 10);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (8, 10, 1);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (9, 7, 6);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (10, 9, 2);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (11, 3, 9);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (12, 10, 1);
INSERT INTO Assignments (TaskID, AssigneeID, AssignedBy) VALUES (13, 8, 1);

-- default comments on the tasks.  
INSERT INTO Comments (TaskID, UserID, text) VALUES (1, 1, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (2, 1, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (3, 4, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (4, 9, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (5, 6, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (6, 2, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (7, 3, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (8, 8, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (9, 5, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (10, 8, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (11, 2, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (12, 10, 'Default comment for test purposes.');
INSERT INTO Comments (TaskID, UserID, text) VALUES (13, 7, 'Default comment for test purposes.');

-- default values for projecthasusers
INSERT INTO projectHasUsers (ProjectID, UserID) VALUES (1, 6), (1, 9), (1, 1), (1, 5), (1, 2), (1, 4), (1, 8);
INSERT INTO projectHasUsers (ProjectID, UserID) VALUES (2, 4), (2, 10), (2, 1), (2, 8), (2, 5), (2, 3);
INSERT INTO projectHasUsers (ProjectID, UserID) VALUES (3, 2), (3, 9), (3, 6), (3, 4), (3, 3), (3, 5), (3, 7);
