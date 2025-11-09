
#!/bin/bash
# Hindi Typing Master - Startup Script

echo "======================================"
echo "Hindi Typing Master"
echo "हिंदी टाइपिंग मास्टर"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if dependencies are installed
if ! python3 -c "import flask" 2> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

echo "✓ Dependencies installed"
echo ""

# Run the application
echo "🚀 Starting application..."
echo ""
echo "Application will be available at:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "======================================"
echo ""

python3 app.py
