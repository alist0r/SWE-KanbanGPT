@echo off
setlocal enabledelayedexpansion

REM =======================
REM Check required files
REM =======================
set "FILES=backend\src\KanbanGPT-BackEnd\.env backend\src\KanbanGPT-BackEnd\kanbanDDLv4.sql backend\src\KanbanGPT-BackEnd\kanbanDDMv2.sql backend\src\KanbanGPT-BackEnd\requirements.txt"

for %%F in (%FILES%) do (
    if not exist "%%F" (
        echo ERROR: Missing required file: %%F
        exit /b 1
    )
)

REM =======================
REM Check Docker Desktop is running
REM =======================
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Desktop does not appear to be running.
    echo Please start Docker Desktop and try again.
    exit /b 1
)

REM =======================
REM Start Docker services
REM =======================
echo Starting Docker containers...
docker-compose up --build -d

REM =======================
REM Wait for MySQL to be ready
REM =======================
echo Waiting for MySQL database to be ready...
:wait_for_mysql
docker exec kanban-db mysqladmin ping -h "localhost" --silent >nul 2>&1
if errorlevel 1 (
    timeout /t 2 >nul
    goto wait_for_mysql
)
echo MySQL is ready.

REM =======================
REM Wait for FastAPI backend to be ready
REM =======================
echo Waiting for FastAPI backend to respond...
:wait_for_backend
powershell -Command "try { if ((Invoke-WebRequest -Uri http://127.0.0.1:8000/ping -UseBasicParsing -TimeoutSec 2).StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"

if errorlevel 1 (
    timeout /t 2 >nul
    goto wait_for_backend
)
echo Backend is ready.

REM =======================
REM Start frontend
REM =======================
cd frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
)

echo Starting frontend dev server...
start "" cmd /c "npm run dev -- --open --port 3000"