#!/bin/bash

# FloodML Dashboard Launcher for Linux/Mac
# This script runs the FloodML Streamlit dashboard

echo ""
echo "============================================"
echo "   FloodML Dashboard Launcher"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    echo "Please install Python 3.8+ using:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "[INFO] Python detected"
python3 --version
echo ""

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "[WARNING] Streamlit not found. Installing dependencies..."
    echo ""
    pip3 install -r requirements-dashboard.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        echo "Please run: pip3 install -r requirements-dashboard.txt"
        exit 1
    fi
fi

echo "[INFO] Starting FloodML Dashboard..."
echo "[INFO] Opening browser to http://localhost:8501"
echo "[INFO] Press Ctrl+C to stop the server"
echo ""

python3 -m streamlit run app.py