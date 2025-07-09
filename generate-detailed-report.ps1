# Script PowerShell per generare un report dettagliato come quello di Jenkins
Write-Host "Starting detailed test report generation..." -ForegroundColor Green

# Create reports directory
New-Item -ItemType Directory -Force -Path "detailed-reports" | Out-Null

# Generate build info
$buildReport = @"
===============================================
DETAILED BUILD REPORT
===============================================
Generated: $(Get-Date)
Project: CI_CD_Validation
Branch: local
Commit: local-dev

"@

Write-Host "Running unittest tests..." -ForegroundColor Yellow
$buildReport += @"
===============================================
UNITTEST RESULTS
===============================================
"@

# Run unittest
$unittestOutput = python -m unittest test_app.py -v 2>&1
$unittestExitCode = $LASTEXITCODE

if ($unittestExitCode -eq 0) {
    $buildReport += "UNITTEST: ALL TESTS PASSED`n"
    Write-Host "Unittest tests: PASSED" -ForegroundColor Green
} else {
    $buildReport += "UNITTEST: SOME TESTS FAILED`n"
    Write-Host "Unittest tests: FAILED" -ForegroundColor Red
}

$buildReport += "`nDetailed unittest output:`n"
$buildReport += $unittestOutput -join "`n"
$buildReport += "`n`n"

Write-Host "Running pytest tests..." -ForegroundColor Yellow
$buildReport += @"
===============================================
PYTEST RESULTS
===============================================
"@

# Run pytest
$pytestOutput = python -m pytest test_app_pytest.py -v --junitxml=detailed-reports/pytest-results.xml --html=detailed-reports/pytest-report.html --self-contained-html --tb=short 2>&1
$pytestExitCode = $LASTEXITCODE

if ($pytestExitCode -eq 0) {
    $buildReport += "PYTEST: ALL TESTS PASSED`n"
    Write-Host "Pytest tests: PASSED" -ForegroundColor Green
} else {
    $buildReport += "PYTEST: SOME TESTS FAILED`n"
    Write-Host "Pytest tests: FAILED" -ForegroundColor Red
}

$buildReport += "`nDetailed pytest output:`n"
$buildReport += $pytestOutput -join "`n"
$buildReport += "`n`n"

Write-Host "Generating coverage report..." -ForegroundColor Yellow
$buildReport += @"
===============================================
CODE COVERAGE ANALYSIS
===============================================
"@

# Generate coverage
python -m coverage run --source=. -m unittest test_app.py | Out-Null
python -m coverage xml -o detailed-reports/coverage.xml | Out-Null
python -m coverage html -d detailed-reports/htmlcov | Out-Null
$coverageOutput = python -m coverage report 2>&1

$buildReport += $coverageOutput -join "`n"
$buildReport += "`n`n"

Write-Host "Running code quality checks..." -ForegroundColor Yellow
$buildReport += @"
===============================================
CODE QUALITY ANALYSIS
===============================================
"@

# Code quality check
python -m flake8 app.py test_app.py --output-file=detailed-reports/flake8-report.txt 2>$null

if (Test-Path "detailed-reports/flake8-report.txt" -and (Get-Content "detailed-reports/flake8-report.txt")) {
    $buildReport += "Code quality issues found:`n"
    $buildReport += Get-Content "detailed-reports/flake8-report.txt" -Raw
} else {
    $buildReport += "No code quality issues found`n"
}
$buildReport += "`n"

# Overall summary
$buildReport += @"
===============================================
OVERALL BUILD SUMMARY
===============================================
"@

$overallStatus = if ($unittestExitCode -eq 0 -and $pytestExitCode -eq 0) { "SUCCESS" } else { "FAILED" }
$unittestStatus = if ($unittestExitCode -eq 0) { "PASSED" } else { "FAILED" }
$pytestStatus = if ($pytestExitCode -eq 0) { "PASSED" } else { "FAILED" }
$qualityStatus = if (Test-Path "detailed-reports/flake8-report.txt" -and (Get-Content "detailed-reports/flake8-report.txt")) { "ISSUES" } else { "CLEAN" }

$buildReport += @"
Overall Status: $overallStatus
Unittest: $unittestStatus
Pytest: $pytestStatus
Code Quality: $qualityStatus

Generated Files:
  • BUILD_REPORT.txt - This comprehensive report
  • pytest-report.html - Interactive HTML test report
  • pytest-results.xml - JUnit XML for CI systems
  • htmlcov/index.html - Interactive coverage report
  • coverage.xml - Coverage XML for CI systems
  • flake8-report.txt - Code quality analysis
"@

# Save the build report
$buildReport | Out-File -FilePath "detailed-reports/BUILD_REPORT.txt" -Encoding UTF8

# Create HTML index
$htmlContent = @"
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CI/CD Test Report</h1>
            <p>Generated on $(Get-Date)</p>
            <p class="$(if ($overallStatus -eq "SUCCESS") { "status-success" } else { "status-failed" })">
                Overall Status: $overallStatus
            </p>
        </div>
        
        <div class="section">
            <h2>Quick Links</h2>
            <div class="links">
                <a href="pytest-report.html" class="link">Test Results (HTML)</a>
                <a href="htmlcov/index.html" class="link">Coverage Report</a>
                <a href="BUILD_REPORT.txt" class="link">Full Text Report</a>
            </div>
        </div>
        
        <div class="section">
            <h2>Test Summary</h2>
            <p><strong>Unittest:</strong> <span class="$(if ($unittestExitCode -eq 0) { "status-success" } else { "status-failed" })">$unittestStatus</span></p>
            <p><strong>Pytest:</strong> <span class="$(if ($pytestExitCode -eq 0) { "status-success" } else { "status-failed" })">$pytestStatus</span></p>
            <p><strong>Code Quality:</strong> <span class="$(if ($qualityStatus -eq "CLEAN") { "status-success" } else { "status-failed" })">$qualityStatus</span></p>
        </div>
        
        <div class="section">
            <h2>Jenkins Simulation</h2>
            <p>This report simulates what you would see in Jenkins:</p>
            <ul>
                <li><strong>pytest-report.html</strong> - Like Jenkins Test Results tab</li>
                <li><strong>htmlcov/index.html</strong> - Like Jenkins Coverage Report</li>
                <li><strong>BUILD_REPORT.txt</strong> - Like Jenkins Console Output</li>
            </ul>
            <p><strong>In Jenkins you would see:</strong></p>
            <ul>
                <li>Red/Green build status indicator</li>
                <li>Test Results tab with pass/fail counts</li>
                <li>Coverage Report link</li>
                <li>Build Artifacts section</li>
                <li>Console Output with full logs</li>
            </ul>
        </div>
    </div>
</body>
</html>
"@

$htmlContent | Out-File -FilePath "detailed-reports/index.html" -Encoding UTF8

# Final output
Write-Host ""
Write-Host "REPORT GENERATION COMPLETE!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Reports generated in: detailed-reports/" -ForegroundColor White
Write-Host "Open detailed-reports/index.html in your browser" -ForegroundColor White
Write-Host "View detailed-reports/BUILD_REPORT.txt for full details" -ForegroundColor White
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "QUICK SUMMARY:" -ForegroundColor Cyan
Write-Host "Overall Status: $overallStatus" -ForegroundColor $(if ($overallStatus -eq "SUCCESS") { "Green" } else { "Red" })
Write-Host "Unittest: $unittestStatus" -ForegroundColor $(if ($unittestExitCode -eq 0) { "Green" } else { "Red" })
Write-Host "Pytest: $pytestStatus" -ForegroundColor $(if ($pytestExitCode -eq 0) { "Green" } else { "Red" })
Write-Host "Code Quality: $qualityStatus" -ForegroundColor $(if ($qualityStatus -eq "CLEAN") { "Green" } else { "Yellow" })

# Open the report
Write-Host ""
Write-Host "Opening report in browser..." -ForegroundColor Green
Start-Process "detailed-reports\index.html"
