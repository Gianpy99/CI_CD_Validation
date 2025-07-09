#!/bin/bash
echo "=== JENKINS DEBUG SCRIPT ==="
echo "Date: $(date)"
echo "User: $(whoami)"
echo "PWD: $(pwd)"
echo "Home: $HOME"
echo "Workspace: $WORKSPACE"

echo ""
echo "=== PYTHON ENVIRONMENT ==="
echo "Python3 path: $(which python3 2>/dev/null || echo 'python3 not found')"
echo "Python path: $(which python 2>/dev/null || echo 'python not found')"

if command -v python3 &> /dev/null; then
    echo "Python3 version: $(python3 --version)"
    echo "Python3 executable: $(python3 -c 'import sys; print(sys.executable)')"
else
    echo "❌ python3 command not available"
fi

if command -v python &> /dev/null; then
    echo "Python version: $(python --version)"
    echo "Python executable: $(python -c 'import sys; print(sys.executable)')"
else
    echo "❌ python command not available"
fi

echo ""
echo "=== SYSTEM INFO ==="
echo "OS: $(uname -a)"
echo "Memory: $(free -h 2>/dev/null || echo 'free command not available')"
echo "Disk space: $(df -h . 2>/dev/null || echo 'df command not available')"

echo ""
echo "=== FILES IN WORKSPACE ==="
ls -la

echo ""
echo "=== PYTHON PACKAGES CHECK ==="
if command -v python3 &> /dev/null; then
    echo "Testing pytest availability..."
    python3 -c "import pytest; print(f'pytest version: {pytest.__version__}')" 2>/dev/null || echo "❌ pytest not available"
    
    echo "Testing unittest availability..."
    python3 -c "import unittest; print('unittest available')" 2>/dev/null || echo "❌ unittest not available"
    
    echo "Testing coverage availability..."
    python3 -c "import coverage; print('coverage available')" 2>/dev/null || echo "❌ coverage not available"
else
    echo "❌ Cannot test Python packages - python3 not available"
fi

echo ""
echo "=== TEST FILES CHECK ==="
if [ -f "test_app.py" ]; then
    echo "✅ test_app.py exists"
    echo "Size: $(wc -l test_app.py) lines"
else
    echo "❌ test_app.py missing"
fi

if [ -f "test_app_pytest.py" ]; then
    echo "✅ test_app_pytest.py exists"
    echo "Size: $(wc -l test_app_pytest.py) lines"
else
    echo "❌ test_app_pytest.py missing"
fi

if [ -f "app.py" ]; then
    echo "✅ app.py exists"
    echo "Size: $(wc -l app.py) lines"
    echo "Multiply function:"
    grep -A 2 "def multiply" app.py || echo "multiply function not found"
else
    echo "❌ app.py missing"
fi

echo ""
echo "=== REQUIREMENTS CHECK ==="
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt exists:"
    cat requirements.txt
else
    echo "❌ requirements.txt missing"
fi

echo ""
echo "=== SIMPLE TEST EXECUTION ==="
if command -v python3 &> /dev/null && [ -f "app.py" ]; then
    echo "Testing basic Python import..."
    python3 -c "import app; print('✅ app.py imports successfully')" 2>/dev/null || echo "❌ Failed to import app.py"
    
    echo "Testing multiply function..."
    python3 -c "import app; result = app.multiply(3, 4); print(f'multiply(3, 4) = {result}'); assert result == 12, f'Expected 12, got {result}'" 2>/dev/null || echo "❌ Multiply function test FAILED (this is expected with current bug)"
else
    echo "❌ Cannot run basic tests"
fi

echo ""
echo "=== DEBUG SCRIPT COMPLETED ==="
