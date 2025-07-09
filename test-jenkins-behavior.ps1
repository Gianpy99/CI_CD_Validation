# Test locale che simula esattamente Jenkins
Write-Host "=== JENKINS SIMULATION TEST ===" -ForegroundColor Cyan
Write-Host "Testing if build fails correctly when tests fail..." -ForegroundColor Yellow

Write-Host "`nRunning unittest tests..." -ForegroundColor Yellow
python -m unittest test_app.py -v
$unittestResult = $LASTEXITCODE

Write-Host "`nRunning pytest tests..." -ForegroundColor Yellow  
python -m pytest test_app_pytest.py -v --tb=short
$pytestResult = $LASTEXITCODE

Write-Host "`n=== RESULTS ===" -ForegroundColor Cyan
Write-Host "Unittest exit code: $unittestResult" -ForegroundColor White
Write-Host "Pytest exit code: $pytestResult" -ForegroundColor White

if ($unittestResult -ne 0 -or $pytestResult -ne 0) {
    Write-Host "`n🚨🚨🚨 BUILD FAILURE! TESTS FAILED! 🚨🚨🚨" -BackgroundColor Red -ForegroundColor White
    Write-Host "🛑 BLOCKING DEPLOYMENT TO PROTECT PRODUCTION" -ForegroundColor Red
    Write-Host "🔧 Fix the failing tests and commit again" -ForegroundColor Yellow
    Write-Host "`nThis is EXACTLY what Jenkins should do!" -ForegroundColor Green
    exit 1
} else {
    Write-Host "`n✅ ALL TESTS PASSED! BUILD SUCCESS!" -BackgroundColor Green -ForegroundColor White
    Write-Host "🚀 Safe to proceed with deployment" -ForegroundColor Green
}

Write-Host "`nExit code will be: $(if ($unittestResult -ne 0 -or $pytestResult -ne 0) { '1 (FAILURE)' } else { '0 (SUCCESS)' })" -ForegroundColor Cyan
