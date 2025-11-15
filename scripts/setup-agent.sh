#!/bin/bash

# Navigate to the agent directory
cd "$(dirname "$0")/../agent" || exit 1

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv .venv || python -m venv .venv
  if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment. Please check your Python installation."
    exit 1
  fi
fi

# Activate the virtual environment
if [ -f ".venv/bin/activate" ]; then
  echo "Activating virtual environment..."
  . .venv/bin/activate
else
  echo "Virtual environment activation script not found."
  exit 1
fi


# Install requirements using pip
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo "Failed to install dependencies. Please check your pip installation and requirements.txt."
  exit 1
fi

echo "Agent setup complete."
