#!/bin/bash
trap 'status=$?; if [ $status -ne 0 ]; then sleep 1; echo "❌ Script failed with status $status. Press Enter to close."; else echo "✅ Script completed successfully. Press Enter to close."; fi; read' EXIT




# ========== FILE CHECK ==========
REQUIRED_FILES=(
  "backend/src/KanbanGPT-BackEnd/.env"
  "backend/src/KanbanGPT-BackEnd/kanbanDDLv4.sql"
  "backend/src/KanbanGPT-BackEnd/kanbanDDMv2.sql"
  "backend/src/KanbanGPT-BackEnd/requirements.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "ERROR: Required file missing: $file"
    sleep 5.0
    exit 1
  fi
done

# ========== DOCKER CHECK ==========
if ! command -v docker &> /dev/null; then
  echo "ERROR: 'docker' command not found. Is Docker Desktop installed?"
  sleep 5.0
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker is not running or Docker Desktop is not started."
  echo "Please launch Docker Desktop and try again."
  # flush buffer before exiting
  sleep 5.0
  exit 1
fi

# ========== START BACKEND AND DATABASE ==========
echo "Starting Docker containers..."
docker-compose up --build -d

# ========== WAIT FOR MYSQL ==========
echo "Waiting for MySQL to be ready..."
until docker exec kanban-db mysqladmin ping -h"localhost" --silent &>/dev/null; do
  sleep 2
done
echo "MySQL is ready."

# ========== WAIT FOR BACKEND ==========
echo "Waiting for FastAPI backend to respond..."
until curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/ping | grep -q "200"; do
  sleep 2
done
echo "Backend is ready."

# ========== START FRONTEND ==========
cd frontend || exit 1

if [[ ! -d "node_modules" ]]; then
  echo "Installing frontend dependencies..."
  npm install
fi

echo "Starting frontend dev server..."
npm run dev -- --open --port 3000


