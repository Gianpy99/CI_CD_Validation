#!/bin/bash
# Script per generare un report chiaro e dettagliato come quello di Jenkins

echo "🚀 Generating detailed test report..."

# Create reports directory
mkdir -p detailed-reports

# Generate build info
echo "===============================================" > detailed-reports/BUILD_REPORT.txt
echo "🏗️  DETAILED BUILD REPORT" >> detailed-reports/BUILD_REPORT.txt
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
echo "📅 Generated: $(date)" >> detailed-reports/BUILD_REPORT.txt
echo "📂 Project: CI_CD_Validation" >> detailed-reports/BUILD_REPORT.txt
echo "🌿 Branch: $(git branch --show-current 2>/dev/null || echo 'local')" >> detailed-reports/BUILD_REPORT.txt
echo "💾 Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'local-dev')" >> detailed-reports/BUILD_REPORT.txt
echo "" >> detailed-reports/BUILD_REPORT.txt

# Run unittest with detailed output
echo "🧪 Running unittest tests..." 
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
echo "📋 UNITTEST RESULTS" >> detailed-reports/BUILD_REPORT.txt
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
python -m unittest test_app.py -v > detailed-reports/unittest-output.txt 2>&1
UNITTEST_EXIT_CODE=$?

if [ $UNITTEST_EXIT_CODE -eq 0 ]; then
    echo "✅ UNITTEST: ALL TESTS PASSED" >> detailed-reports/BUILD_REPORT.txt
    echo "✅ Unittest tests: PASSED"
else
    echo "❌ UNITTEST: SOME TESTS FAILED" >> detailed-reports/BUILD_REPORT.txt
    echo "❌ Unittest tests: FAILED"
fi

echo "" >> detailed-reports/BUILD_REPORT.txt
echo "📝 Detailed unittest output:" >> detailed-reports/BUILD_REPORT.txt
cat detailed-reports/unittest-output.txt >> detailed-reports/BUILD_REPORT.txt
echo "" >> detailed-reports/BUILD_REPORT.txt

# Run pytest with detailed output
echo "🔬 Running pytest tests..."
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
echo "🔬 PYTEST RESULTS" >> detailed-reports/BUILD_REPORT.txt  
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
python -m pytest test_app_pytest.py -v \
    --junitxml=detailed-reports/pytest-results.xml \
    --html=detailed-reports/pytest-report.html --self-contained-html \
    --tb=short > detailed-reports/pytest-output.txt 2>&1
PYTEST_EXIT_CODE=$?

if [ $PYTEST_EXIT_CODE -eq 0 ]; then
    echo "✅ PYTEST: ALL TESTS PASSED" >> detailed-reports/BUILD_REPORT.txt
    echo "✅ Pytest tests: PASSED"
else
    echo "❌ PYTEST: SOME TESTS FAILED" >> detailed-reports/BUILD_REPORT.txt
    echo "❌ Pytest tests: FAILED"
fi

echo "" >> detailed-reports/BUILD_REPORT.txt
echo "📝 Detailed pytest output:" >> detailed-reports/BUILD_REPORT.txt
cat detailed-reports/pytest-output.txt >> detailed-reports/BUILD_REPORT.txt
echo "" >> detailed-reports/BUILD_REPORT.txt

# Generate coverage report
echo "📊 Generating coverage report..."
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
echo "📊 CODE COVERAGE ANALYSIS" >> detailed-reports/BUILD_REPORT.txt
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
python -m coverage run --source=. -m unittest test_app.py > /dev/null 2>&1
python -m coverage xml -o detailed-reports/coverage.xml > /dev/null 2>&1
python -m coverage html -d detailed-reports/htmlcov > /dev/null 2>&1
python -m coverage report > detailed-reports/coverage-summary.txt 2>&1

cat detailed-reports/coverage-summary.txt >> detailed-reports/BUILD_REPORT.txt
echo "" >> detailed-reports/BUILD_REPORT.txt

# Code quality check
echo "📋 Running code quality checks..."
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
echo "📋 CODE QUALITY ANALYSIS" >> detailed-reports/BUILD_REPORT.txt
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
python -m flake8 app.py test_app.py --output-file=detailed-reports/flake8-report.txt 2>/dev/null || true

if [ -s detailed-reports/flake8-report.txt ]; then
    echo "⚠️ Code quality issues found:" >> detailed-reports/BUILD_REPORT.txt
    cat detailed-reports/flake8-report.txt >> detailed-reports/BUILD_REPORT.txt
else
    echo "✅ No code quality issues found" >> detailed-reports/BUILD_REPORT.txt
fi
echo "" >> detailed-reports/BUILD_REPORT.txt

# Overall summary
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt
echo "📈 OVERALL BUILD SUMMARY" >> detailed-reports/BUILD_REPORT.txt
echo "===============================================" >> detailed-reports/BUILD_REPORT.txt

OVERALL_STATUS="✅ SUCCESS"
if [ $UNITTEST_EXIT_CODE -ne 0 ] || [ $PYTEST_EXIT_CODE -ne 0 ]; then
    OVERALL_STATUS="❌ FAILED"
fi

echo "🏆 Overall Status: $OVERALL_STATUS" >> detailed-reports/BUILD_REPORT.txt
echo "🧪 Unittest: $([ $UNITTEST_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")" >> detailed-reports/BUILD_REPORT.txt
echo "🔬 Pytest: $([ $PYTEST_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")" >> detailed-reports/BUILD_REPORT.txt
echo "📋 Code Quality: $([ -s detailed-reports/flake8-report.txt ] && echo "⚠️ ISSUES" || echo "✅ CLEAN")" >> detailed-reports/BUILD_REPORT.txt

echo "" >> detailed-reports/BUILD_REPORT.txt
echo "📁 Generated Files:" >> detailed-reports/BUILD_REPORT.txt
echo "  • BUILD_REPORT.txt - This comprehensive report" >> detailed-reports/BUILD_REPORT.txt
echo "  • pytest-report.html - Interactive HTML test report" >> detailed-reports/BUILD_REPORT.txt
echo "  • pytest-results.xml - JUnit XML for CI systems" >> detailed-reports/BUILD_REPORT.txt
echo "  • htmlcov/index.html - Interactive coverage report" >> detailed-reports/BUILD_REPORT.txt
echo "  • coverage.xml - Coverage XML for CI systems" >> detailed-reports/BUILD_REPORT.txt
echo "  • flake8-report.txt - Code quality analysis" >> detailed-reports/BUILD_REPORT.txt

# Create a simple index.html for easy viewing
cat > detailed-reports/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>CI/CD Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #333; border-bottom: 2px solid #007cba; padding-bottom: 10px; }
        .status-success { color: #28a745; font-weight: bold; }
        .status-failed { color: #dc3545; font-weight: bold; }
        .section { margin: 20px 0; padding: 15px; background: #f8f9fa; border-left: 4px solid #007cba; }
        .links { display: flex; gap: 15px; flex-wrap: wrap; }
        .link { display: inline-block; padding: 10px 15px; background: #007cba; color: white; text-decoration: none; border-radius: 5px; }
        .link:hover { background: #0056b3; }
        pre { background: #f1f1f1; padding: 10px; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 CI/CD Test Report</h1>
            <p>Generated on $(date)</p>
            <p class="$([ $UNITTEST_EXIT_CODE -eq 0 ] && [ $PYTEST_EXIT_CODE -eq 0 ] && echo "status-success" || echo "status-failed")">
                Overall Status: $OVERALL_STATUS
            </p>
        </div>
        
        <div class="section">
            <h2>📊 Quick Links</h2>
            <div class="links">
                <a href="pytest-report.html" class="link">📋 Test Results (HTML)</a>
                <a href="htmlcov/index.html" class="link">📈 Coverage Report</a>
                <a href="BUILD_REPORT.txt" class="link">📄 Full Text Report</a>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Test Summary</h2>
            <p><strong>Unittest:</strong> <span class="$([ $UNITTEST_EXIT_CODE -eq 0 ] && echo "status-success" || echo "status-failed")">$([ $UNITTEST_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")</span></p>
            <p><strong>Pytest:</strong> <span class="$([ $PYTEST_EXIT_CODE -eq 0 ] && echo "status-success" || echo "status-failed")">$([ $PYTEST_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")</span></p>
            <p><strong>Code Quality:</strong> <span class="$([ -s detailed-reports/flake8-report.txt ] && echo "status-failed" || echo "status-success")">$([ -s detailed-reports/flake8-report.txt ] && echo "⚠️ ISSUES" || echo "✅ CLEAN")</span></p>
        </div>
        
        <div class="section">
            <h2>📋 Instructions</h2>
            <p>This report simulates what you would see in Jenkins. The key files are:</p>
            <ul>
                <li><strong>pytest-report.html</strong> - Interactive test results (like Jenkins Test Results tab)</li>
                <li><strong>htmlcov/index.html</strong> - Code coverage analysis (like Jenkins Coverage Report)</li>
                <li><strong>BUILD_REPORT.txt</strong> - Complete text report (like Jenkins Console Output)</li>
            </ul>
        </div>
    </div>
</body>
</html>
EOF

# Final console output
echo ""
echo "🎉 REPORT GENERATION COMPLETE!"
echo "==============================================="
echo "📁 Reports generated in: detailed-reports/"
echo "🌐 Open detailed-reports/index.html in your browser"
echo "📋 View detailed-reports/BUILD_REPORT.txt for full details"
echo "==============================================="
echo ""
echo "📊 QUICK SUMMARY:"
echo "Overall Status: $OVERALL_STATUS"
echo "Unittest: $([ $UNITTEST_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")"
echo "Pytest: $([ $PYTEST_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")"
echo "Code Quality: $([ -s detailed-reports/flake8-report.txt ] && echo "⚠️ ISSUES" || echo "✅ CLEAN")"

# Open the report automatically if possible
if command -v start > /dev/null 2>&1; then
    echo ""
    echo "🚀 Opening report in browser..."
    start detailed-reports/index.html
elif command -v open > /dev/null 2>&1; then
    echo ""
    echo "🚀 Opening report in browser..."
    open detailed-reports/index.html
fi
