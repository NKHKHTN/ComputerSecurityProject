#!/bin/bash

# Computer Security Project Setup Script
# This script sets up the development environment for the RSA Key Management System

echo "Computer Security Project - Setup Script"
echo "============================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3."
    exit 1
fi

echo "pip3 found"

# Install system dependencies for Debian/Ubuntu or Fedora
if command -v apt &> /dev/null; then
    echo "Installing system dependencies (tkinter and Pillow build deps)..."
    sudo apt update
    sudo apt install -y python3-tk libjpeg-dev zlib1g-dev libtiff-dev libfreetype-dev liblcms2-dev
    echo "System dependencies installed"
elif command -v dnf &> /dev/null; then
    echo "Installing system dependencies (tkinter and Pillow build deps)..."
    sudo dnf install -y python3-tkinter python3-devel libjpeg-turbo-devel zlib-devel libtiff-devel freetype-devel lcms2-devel
    echo "System dependencies installed"
fi

# Remove existing virtual environment if it exists
echo "Checking for existing virtual environment..."
if [ -d "venv" ]; then
    echo "Existing virtual environment found. Removing..."
    rm -rf venv
    echo "Old virtual environment removed"
fi

# Create virtual environment
echo "Creating virtual environment with the correct Python interpreter..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Failed to upgrade pip"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install Python dependencies"
    exit 1
fi

echo ""
echo "Setup completed successfully!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python3 main.py"
echo ""
echo "To run tests:"
echo "python3 test_rsa.py"
echo ""
echo "To deactivate virtual environment:"
echo "deactivate"
