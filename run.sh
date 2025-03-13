#!/bin/bash

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run the application
echo "Starting the application..."
# Start the FastAPI backend
uvicorn backend.main:app --host $(grep API_HOST .env | cut -d '=' -f2) --port $(grep API_PORT .env | cut -d '=' -f2) &
BACKEND_PID=$!

# Wait a moment for the backend to start
sleep 2

# Start the Telegram bot
python -m telegram_bot.bot &
BOT_PID=$!

# Function to handle termination
function cleanup {
    echo "Stopping services..."
    kill $BACKEND_PID
    kill $BOT_PID
    exit 0
}

# Register the cleanup function for the SIGINT signal
trap cleanup SIGINT

# Wait for termination
wait
