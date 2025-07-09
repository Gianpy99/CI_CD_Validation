# Script PowerShell per eseguire tutti i controlli localmente prima del commit
Write-Host "🚀 Starting local CI/CD validation..." -ForegroundColor Green

# 1. Controllo qualità del codice
Write-Host "📋 Running code quality checks..." -ForegroundColor Yellow
python -m flake8 app.py test_app.py --output-file=flake8-report.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Code quality checks passed" -ForegroundColor Green
} else {
    Write-Host "⚠️ Code quality issues found, check flake8-report.txt" -ForegroundColor Yellow
}

# 2. Esecuzione test unittest
Write-Host "🧪 Running unittest tests..." -ForegroundColor Yellow
python -m unittest test_app.py -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Unittest tests failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Unittest tests passed" -ForegroundColor Green

# 3. Esecuzione test pytest con coverage
Write-Host "📊 Running pytest tests with coverage..." -ForegroundColor Yellow
python -m pytest test_app_pytest.py -v --cov=app --cov-report=term-missing --cov-report=html:htmlcov --junitxml=test-results.xml

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Pytest tests failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Pytest tests passed" -ForegroundColor Green

# 4. Mostra coverage report
Write-Host "📈 Coverage Summary:" -ForegroundColor Cyan
python -m coverage report

# 5. Simulazione build artifact
Write-Host "📦 Creating build artifact..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path dist | Out-Null
Copy-Item app.py dist/
$buildInfo = @"
Build completed on $(Get-Date)
Local test build
"@
$buildInfo | Out-File -FilePath dist/build-info.txt

Write-Host "🎉 All local checks passed! Ready to commit." -ForegroundColor Green
Write-Host "📁 Generated files:" -ForegroundColor Cyan
Write-Host "  - htmlcov/index.html (Coverage report)"
Write-Host "  - test-results.xml (Test results)"
Write-Host "  - flake8-report.txt (Code quality)"
Write-Host "  - dist/ (Build artifacts)"
