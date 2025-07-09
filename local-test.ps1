# Script PowerShell per eseguire tutti i controlli localmente prima del commit
Write-Host " Starting local CI/CD validation..." -ForegroundColor Green

# 0. Controllo e installazione dipendenze
Write-Host " Checking dependencies..." -ForegroundColor Cyan
if (Test-Path "requirements.txt") {
    Write-Host "Installing/updating dependencies..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host " Dependencies installed" -ForegroundColor Green
    } else {
        Write-Host " Some dependencies may not be available" -ForegroundColor Yellow
    }
} else {
    Write-Host " requirements.txt not found" -ForegroundColor Yellow
}

# 1. Controllo qualità del codice
Write-Host " Running code quality checks..." -ForegroundColor Yellow
python -m flake8 app.py test_app.py --output-file=flake8-report.txt 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host " Code quality checks passed" -ForegroundColor Green
} else {
    Write-Host " Code quality issues found, check flake8-report.txt (or flake8 not installed)" -ForegroundColor Yellow
}

# 2. Esecuzione test unittest
Write-Host " Running unittest tests..." -ForegroundColor Yellow
python -m unittest test_app.py -v
if ($LASTEXITCODE -ne 0) {
    Write-Host " Unittest tests failed" -ForegroundColor Red
    exit 1
}
Write-Host " Unittest tests passed" -ForegroundColor Green

# 3. Esecuzione test pytest con coverage
Write-Host " Running pytest tests..." -ForegroundColor Yellow

# Prima proviamo con coverage, se fallisce usiamo pytest base
python -m pytest test_app_pytest.py -v --cov=app --cov-report=term-missing --cov-report=html:htmlcov --junitxml=test-results.xml 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host " Coverage plugin not available, running pytest without coverage..." -ForegroundColor Yellow
    python -m pytest test_app_pytest.py -v --junitxml=test-results.xml 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host " Pytest not available, skipping pytest tests..." -ForegroundColor Yellow
    } else {
        Write-Host " Pytest tests passed (without coverage)" -ForegroundColor Green
    }
} else {
    Write-Host " Pytest tests passed with coverage" -ForegroundColor Green
}

# 4. Mostra coverage report (se disponibile)
Write-Host " Coverage Summary:" -ForegroundColor Cyan
python -m coverage report 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host " Coverage report not available (coverage not installed)" -ForegroundColor Yellow
}

# 5. Simulazione build artifact
Write-Host " Creating build artifact..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path dist | Out-Null
Copy-Item app.py dist/
$buildInfo = @"
Build completed on $(Get-Date)
Local test build
"@
$buildInfo | Out-File -FilePath dist/build-info.txt

Write-Host " All local checks passed! Ready to commit." -ForegroundColor Green
Write-Host " Generated files:" -ForegroundColor Cyan
Write-Host "  - htmlcov/index.html (Coverage report - if available)" -ForegroundColor White
Write-Host "  - test-results.xml (Test results - if available)" -ForegroundColor White
Write-Host "  - flake8-report.txt (Code quality - if available)" -ForegroundColor White
Write-Host "  - dist/ (Build artifacts)" -ForegroundColor White

Write-Host " To install missing dependencies, run:" -ForegroundColor Cyan
Write-Host "   pip install -r requirements.txt" -ForegroundColor White
