#!/bin/bash

# Setup script for Literature Review RAG System
# Makes it easy for beginners to get started

set -e  # Exit on error

echo "================================"
echo "ResearcherRAG Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.9+ required (found $python_version)"
    exit 1
fi

echo "✓ Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install requirements
echo "Installing dependencies..."
echo "(This may take 2-3 minutes...)"
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Create directories
echo "Creating data directories..."
mkdir -p data/raw_pdfs
mkdir -p data/processed
mkdir -p data/vector_db
echo "✓ Directories created"
echo ""

# Setup environment file
if [ ! -f ".env" ]; then
    echo "Setting up environment file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API key!"
    echo ""
    echo "Run: nano .env"
    echo "Add: ANTHROPIC_API_KEY=your_key_here"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Create directories
echo "================================"
echo "Setup Complete! 🎉"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Add your API key:"
echo "   nano .env"
echo "   (Add: ANTHROPIC_API_KEY=your_key_here)"
echo ""
echo "2. Run the application:"
echo "   python app.py"
echo ""
echo "3. Open browser:"
echo "   http://localhost:7860"
echo ""
echo "4. Upload papers and start asking questions!"
echo ""
echo "Documentation: ../QUICK_START.md"
echo "================================"
