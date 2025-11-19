#!/bin/bash

# MedIntel Quick Start Script
# This script sets up and runs MedIntel

echo "=================================================="
echo "🏥 MedIntel - Quick Start Setup"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python --version)"
echo ""

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/Scripts/activate

# Check if requirements are installed
if [ ! -f "venv/.installed" ]; then
    echo ""
    echo "📥 Installing dependencies (this may take 5-10 minutes)..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.installed
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "⚙️ Creating configuration file..."
    cp .env.example .env
    echo "✅ Configuration file created"
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "🚀 Starting MedIntel server..."
echo ""
echo "📍 Server will be available at:"
echo "   - Main API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=================================================="
echo ""

# Start the server
python main.py
