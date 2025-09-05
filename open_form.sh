#!/bin/bash

echo "Opening Invesco Form with Extracted Data..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed or not in PATH"
        echo "Please install Python and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if client_automation.py exists
if [ ! -f "client_automation.py" ]; then
    echo "Error: client_automation.py not found"
    echo "Please ensure the file is in the same directory"
    exit 1
fi

# Run the client automation
$PYTHON_CMD client_automation.py

echo "Press Enter to continue..."
read
