#!/bin/bash

# Script per eseguire tutti i controlli localmente prima del commit
echo " Starting local CI/CD validation..."

# 1. Controllo qualità del codice
echo " Running code quality checks..."
python -m flake8 app.py test_app.py --output-file=flake8-report.txt
if [ $? -eq 0 ]; then
    echo " Code quality checks passed"
else
    echo "  Code quality issues found, check flake8-report.txt"
fi

# 2. Esecuzione test unittest
echo " Running unittest tests..."
python -m unittest test_app.py -v
if [ $? -eq 0 ]; then
    echo " Unittest tests passed"
else
    echo " Unittest tests failed"
    exit 1
fi

# 3. Esecuzione test pytest con coverage
echo " Running pytest tests with coverage..."
python -m pytest test_app_pytest.py -v \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --junitxml=test-results.xml

if [ $? -eq 0 ]; then
    echo " Pytest tests passed"
else
    echo " Pytest tests failed"
    exit 1
fi

# 4. Mostra coverage report
echo " Coverage Summary:"
python -m coverage report

# 5. Simulazione build artifact
echo " Creating build artifact..."
mkdir -p dist
cp app.py dist/
echo "Build completed on $(date)" > dist/build-info.txt
echo "Local test build" >> dist/build-info.txt

echo " All local checks passed! Ready to commit."
echo " Generated files:"
echo "  - htmlcov/index.html (Coverage report)"
echo "  - test-results.xml (Test results)"
echo "  - flake8-report.txt (Code quality)"
echo "  - dist/ (Build artifacts)"
