#!/bin/bash

# Script per testare localmente la generazione dei report HTML
# Simula quello che fa Jenkins per verificare che tutto funzioni

echo "🧪 Testing HTML Reports Generation Locally..."
echo "============================================="

# Crea cartella test-reports se non existe
mkdir -p test-reports

# Controlla se Python è disponibile
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found!"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

# Test dependencies
echo ""
echo "📦 Checking required packages..."
$PYTHON_CMD -c "import pytest; print('✅ pytest available')" || echo "❌ pytest missing"
$PYTHON_CMD -c "import coverage; print('✅ coverage available')" || echo "❌ coverage missing"
$PYTHON_CMD -c "import pytest_html; print('✅ pytest-html available')" || echo "❌ pytest-html missing"
$PYTHON_CMD -c "import flake8; print('✅ flake8 available')" || echo "❌ flake8 missing"

echo ""
echo "🔍 Generating Code Quality Report..."
$PYTHON_CMD -m flake8 app.py test_app.py --output-file=flake8-report.txt || true
$PYTHON_CMD -m flake8 app.py test_app.py --format=html --output-file=flake8-report.html || true

echo ""
echo "🧪 Running Pytest with HTML Report..."
$PYTHON_CMD -m pytest test_app_pytest.py -v \
    --junitxml=test-reports/pytest-results.xml \
    --html=test-reports/pytest-report.html --self-contained-html \
    --tb=short

echo ""
echo "📊 Generating Coverage Report..."
$PYTHON_CMD -m coverage run --source=. -m unittest test_app.py
$PYTHON_CMD -m coverage xml -o test-reports/coverage.xml
$PYTHON_CMD -m coverage html -d test-reports/htmlcov
$PYTHON_CMD -m coverage report | tee test-reports/coverage-summary.txt

echo ""
echo "📋 Report Generation Summary:"
echo "=============================="

if [ -f "flake8-report.html" ]; then
    echo "✅ flake8-report.html generated"
else
    echo "❌ flake8-report.html NOT generated"
fi

if [ -f "test-reports/pytest-report.html" ]; then
    echo "✅ test-reports/pytest-report.html generated"
else
    echo "❌ test-reports/pytest-report.html NOT generated"
fi

if [ -f "test-reports/htmlcov/index.html" ]; then
    echo "✅ test-reports/htmlcov/index.html generated"
else
    echo "❌ test-reports/htmlcov/index.html NOT generated"
fi

echo ""
echo "🌐 To view reports in browser:"
echo "------------------------------"
echo "• Flake8 Report: file://$(pwd)/flake8-report.html"
echo "• Pytest Report: file://$(pwd)/test-reports/pytest-report.html" 
echo "• Coverage Report: file://$(pwd)/test-reports/htmlcov/index.html"

echo ""
echo "📁 Files that would be archived in Jenkins:"
echo "-------------------------------------------"
find . -name "*.html" -o -path "./test-reports/*" | grep -E "\.(html|xml|txt)$" | head -20

echo ""
echo "✅ Local HTML report generation test completed!"
