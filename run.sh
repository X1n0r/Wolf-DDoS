#!/bin/bash

# DDoS Tool Runner Script
# Can be used on Linux, macOS, and GitHub Actions

echo "=========================================="
echo "       DDoS Tool - Quick Runner"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Run the main script
python3 main.py
