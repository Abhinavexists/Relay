#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Add current user to docker group
echo "Adding $SUDO_USER to docker group..."
usermod 
# Set proper permissions
echo "Setting proper permissions..."
chown -R $SUDO_USER:$SUDO_USER .
chmod -R 755 .

echo "Setup complete! Please:"
echo "1. Edit the .env file with your actual values"
echo "2. Log out and log back in for group changes to take effect"
echo "3. Run 'docker-compose up --build' to start the application" -aG docker $SUDO_USER

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp env-example.txt .env
    echo "Please edit .env file with your actual values"
fi

# Set proper permissions
echo "Setting proper permissions..."
chown -R $SUDO_USER:$SUDO_USER .
chmod -R 755 .

echo "Setup complete! Please:"
echo "1. Edit the .env file with your actual values"
echo "2. Log out and log back in for group changes to take effect"
echo "3. Run 'docker-compose up --build' to start the application" 