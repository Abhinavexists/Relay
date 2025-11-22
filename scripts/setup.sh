#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

TARGET_USER="$SUDO_USER"

echo "Adding $TARGET_USER to docker group..."
usermod -aG docker "$TARGET_USER"

# Create .env file if missing
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo "Setting proper permissions..."
chown -R "$TARGET_USER:$TARGET_USER" .
chmod -R 755 .

echo "Setup complete:"
echo "Edit .env"
echo "Log out and log back in for docker group to apply"
echo "Run: docker-compose up --build"
