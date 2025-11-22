#!/bin/bash
set -e

# validate env file
if [ ! -f .env ]; then
    echo ".env missing"
    exit 1
fi

API_HOST=$(grep '^API_HOST=' .env | cut -d '=' -f2-)
API_PORT=$(grep '^API_PORT=' .env | cut -d '=' -f2-)

if [ -z "$API_HOST" ] || [ -z "$API_PORT" ]; then
    echo "API_HOST or API_PORT missing"
    exit 1
fi

# create venv if absent
if [ ! -d "venv" ]; then
    if command -v uv >/dev/null 2>&1; then
        echo "Creating venv with uv..."
        uv venv venv
    else
        echo "Creating venv with python..."
        python -m venv venv
    fi
fi

# activate
source venv/bin/activate

# install deps
if command -v uv >/dev/null 2>&1; then
    echo "Installing dependencies with uv..."
    uv pip install -r requirements.txt
else
    echo "Installing dependencies with pip..."
    pip install -r requirements.txt
fi

# start backend
uvicorn backend.main:app --host "$API_HOST" --port "$API_PORT" &
BACKEND_PID=$!

# wait for backend port to open
for _ in {1..30}; do
    if nc -z "$API_HOST" "$API_PORT" 2>/dev/null; then
        echo "Backend is up!"
        break
    fi
    echo "Waiting for backend to start..."
    sleep 0.2
done

# start bot
python -m telegram_bot.bot &
BOT_PID=$!

cleanup() {
    kill "$BACKEND_PID" 2>/dev/null || true
    kill "$BOT_PID" 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT

wait
