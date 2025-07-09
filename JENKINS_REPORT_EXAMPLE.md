# 🔍 Jenkins Report Example - Failed Build

Questo documento mostra come apparirà il report Jenkins quando viene rilevato il bug nella funzione `multiply()`.

## 📊 Jenkins Dashboard Overview

```
🔴 Build #42 - FAILED
├── ⏱️ Duration: 2 min 15 sec
├── 📅 Started: Jul 9, 2025 11:13 AM
├── 🌿 Branch: main
└── 💾 Commit: a1b2c3d "Added error in multiply function for testing"
```

## 🧪 Test Results Summary

```
📊 Test Results
├── 🔢 Total Tests: 25
├── ✅ Passed: 21
├── ❌ Failed: 4  
├── ⏭️ Skipped: 0
└── 🔴 Success Rate: 84%
```

## 📋 Failed Tests Detail

### 1. `test_multiply_positive` 
```
❌ FAILED test_app_pytest.py::TestMultiply::test_multiply_positive
AssertionError: assert 7 == 12
  +  where 7 = multiply(3, 4)
  
Expected: 12 (3 * 4)
Actual: 7 (3 + 4)
File: test_app_pytest.py, line 51
```

### 2. `test_multiply_with_zero`
```
❌ FAILED test_app_pytest.py::TestMultiply::test_multiply_with_zero  
AssertionError: assert 5 == 0
  +  where 5 = multiply(5, 0)
  
Expected: 0 (5 * 0) 
Actual: 5 (5 + 0)
File: test_app_pytest.py, line 56
```

### 3. `test_multiply_negative`
```
❌ FAILED test_app_pytest.py::TestMultiply::test_multiply_negative
AssertionError: assert 1 == -6
  +  where 1 = multiply(-2, 3)
  
Expected: -6 (-2 * 3)
Actual: 1 (-2 + 3)  
File: test_app_pytest.py, line 61
```

### 4. `test_basic_operations`
```
❌ FAILED test_app_pytest.py::TestAllFunctions::test_basic_operations
AssertionError: assert 10 == 21
  +  where 10 = multiply(3, 7)
  
Expected: 21 (3 * 7)
Actual: 10 (3 + 7)
File: test_app_pytest.py, line 71  
```

## 📈 Trend Analysis

```
📊 Test Trend (Last 5 builds)
Build #42: 🔴 84% (21/25) ← Current  
Build #41: ✅ 100% (25/25)
Build #40: ✅ 100% (25/25) 
Build #39: ✅ 100% (25/25)
Build #38: ✅ 100% (25/25)
```

## 🔍 Root Cause Analysis

**Problem Detected**: La funzione `multiply()` in `app.py` ha un bug logico.

**Current Implementation**:
```python
def multiply(a, b):
    return a + b  # ❌ BUG: Should be a * b
```

**Expected Implementation**:
```python  
def multiply(a, b):
    return a * b  # ✅ CORRECT
```

## 📦 Build Artifacts

- ✅ `app-42.tar.gz` - Application package (generated)
- ✅ `test-results.xml` - Test results (4 failures)
- ✅ `coverage.xml` - Code coverage report  
- ✅ `flake8-report.txt` - Code quality report
- ✅ `build-info.txt` - Build metadata

## 🚨 Actions Required

1. **Fix the bug** in `app.py` line 11:
   ```python
   - return a + b  # Remove this
   + return a * b  # Add this
   ```

2. **Run tests locally**:
   ```bash
   .\local-test.ps1
   ```

3. **Commit fix**:
   ```bash
   git add app.py
   git commit -m "Fix multiply function bug"
   git push
   ```

## 📬 Notifications Sent

- 📧 **Email**: Sent to developers  
- 💬 **Slack**: Posted to #ci-cd channel
- 🔔 **Dashboard**: Red indicator visible

## 🎯 Jenkins UI Elements

Nel Jenkins Dashboard vedrai:

1. **🔴 Red Build Status** - Indica fallimento
2. **📊 Test Results Tab** - Mostra 4/25 test falliti  
3. **📈 Test Trend Graph** - Mostra calo dal 100% all'84%
4. **📋 Console Output** - Log completo dell'esecuzione
5. **📦 Artifacts** - File scaricabili della build
6. **📱 Blue Ocean View** - Vista pipeline moderna

Questo è esattamente il tipo di feedback dettagliato che riceverai da Jenkins quando c'è un problema nel codice! 🎯
