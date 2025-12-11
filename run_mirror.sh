#!/bin/bash

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if venv exists
if [ -d "venv" ]; then
    echo "Starting Smart Mirror..."
    # Activate venv and run
    ./venv/bin/python main.py
else
    echo "Virtual environment not found!"
    echo "Please run the installation first."
    exit 1
fi
