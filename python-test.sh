#!/bin/bash
echo "=== PYTHON DETECTION TEST ==="
echo "Date: $(date)"
echo ""

echo "🔍 Checking available Python interpreters..."
echo ""

# Check python3
if command -v python3 >/dev/null 2>&1; then
    echo "✅ python3 found: $(which python3)"
    echo "   Version: $(python3 --version)"
    echo "   Executable: $(python3 -c 'import sys; print(sys.executable)')"
else
    echo "❌ python3 not found"
fi

echo ""

# Check python
if command -v python >/dev/null 2>&1; then
    echo "✅ python found: $(which python)"
    echo "   Version: $(python --version)"
    echo "   Executable: $(python -c 'import sys; print(sys.executable)')"
else
    echo "❌ python not found"
fi

echo ""

# Determine which to use
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "💥 CRITICAL: No Python interpreter found!"
    exit 1
fi

echo "🎯 Selected Python command: $PYTHON_CMD"
echo ""

# Test basic functionality
echo "🧪 Testing basic Python functionality..."
$PYTHON_CMD -c "print('✅ Python execution works!')"
echo ""

# Test module imports
echo "🔧 Testing required modules..."
$PYTHON_CMD -c "import unittest; print('✅ unittest available')" 2>/dev/null || echo "❌ unittest not available"
$PYTHON_CMD -c "import sys; print('✅ sys available - path:', sys.path[0])" 2>/dev/null || echo "❌ sys not available"

echo ""
echo "📦 Testing pip..."
$PYTHON_CMD -m pip --version 2>/dev/null || echo "❌ pip not available"

echo ""
echo "=== TEST COMPLETE ==="
