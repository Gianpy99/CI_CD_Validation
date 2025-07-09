#!/usr/bin/env python3
"""
Coverage-style pytest report generator for Jenkins compatibility.
This creates a pytest report with external CSS/JS files like coverage.py does,
which works better with Jenkins HTML viewer restrictions.
"""

import json
import os
import sys
from datetime import datetime
import subprocess


def run_pytest_with_json():
    """Run pytest and capture results in JSON format."""
    print("🧪 Running pytest to collect test results...")
    
    cmd = [sys.executable, "-m", "pytest", "--tb=short", "-v", "--json-report", "--json-report-file=test-results.json"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Pytest exit code: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running pytest: {e}")
        return False


def create_css_file():
    """Create external CSS file like coverage.py does."""
    css_content = """
/* Coverage-style CSS for pytest report */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f8f9fa;
}

.content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background: #ffffff;
    border-bottom: 2px solid #e9ecef;
    padding: 20px 0;
    margin-bottom: 30px;
}

h1 {
    color: #333;
    margin: 0;
    font-size: 2rem;
    display: inline-block;
}

.summary {
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}

.stat-box {
    text-align: center;
    padding: 15px;
    border-radius: 6px;
    border-left: 4px solid #6c757d;
}

.stat-box.passed { border-left-color: #28a745; background: #d4edda; }
.stat-box.failed { border-left-color: #dc3545; background: #f8d7da; }
.stat-box.skipped { border-left-color: #ffc107; background: #fff3cd; }
.stat-box.total { border-left-color: #007bff; background: #d1ecf1; }

.stat-number {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.9rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.results-table {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

table {
    width: 100%;
    border-collapse: collapse;
}

th {
    background: #f8f9fa;
    padding: 12px;
    text-align: left;
    border-bottom: 2px solid #e9ecef;
    font-weight: 600;
    color: #333;
}

td {
    padding: 12px;
    border-bottom: 1px solid #e9ecef;
}

tr:hover {
    background: #f8f9fa;
}

.status {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
    text-transform: uppercase;
    text-align: center;
}

.status.passed {
    background: #d4edda;
    color: #155724;
}

.status.failed {
    background: #f8d7da;
    color: #721c24;
}

.status.skipped {
    background: #fff3cd;
    color: #856404;
}

.duration {
    text-align: right;
    font-family: monospace;
    color: #666;
}

.test-name {
    font-family: monospace;
    font-size: 0.9rem;
}

.details-toggle {
    background: #007bff;
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
}

.details-toggle:hover {
    background: #0056b3;
}

.test-details {
    display: none;
    background: #f8f9fa;
    padding: 15px;
    margin-top: 10px;
    border-radius: 4px;
    border-left: 4px solid #007bff;
}

.test-details.show {
    display: block;
}

.test-details pre {
    background: white;
    padding: 10px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 0.85rem;
    margin: 0;
}

.filter-section {
    margin-bottom: 20px;
}

.filter-section input[type="text"] {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-right: 10px;
    width: 200px;
}

.filter-section label {
    margin-right: 15px;
    font-size: 0.9rem;
}

.toggle-all {
    background: #28a745;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 15px;
}

.toggle-all:hover {
    background: #218838;
}
"""
    
    with open("pytest-report/style.css", "w") as f:
        f.write(css_content)


def create_js_file():
    """Create external JavaScript file like coverage.py does."""
    js_content = """
// Coverage-style JavaScript for pytest report
document.addEventListener('DOMContentLoaded', function() {
    // Auto-expand failed tests
    const failedRows = document.querySelectorAll('tr[data-status="failed"]');
    failedRows.forEach(row => {
        const details = row.querySelector('.test-details');
        if (details) {
            details.classList.add('show');
        }
    });
    
    // Filter functionality
    const filterInput = document.getElementById('filter');
    if (filterInput) {
        filterInput.addEventListener('input', function() {
            const filterValue = this.value.toLowerCase();
            const rows = document.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const testName = row.querySelector('.test-name').textContent.toLowerCase();
                if (testName.includes(filterValue)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
    
    // Hide passed tests checkbox
    const hidePassedCheckbox = document.getElementById('hide-passed');
    if (hidePassedCheckbox) {
        hidePassedCheckbox.addEventListener('change', function() {
            const passedRows = document.querySelectorAll('tr[data-status="passed"]');
            passedRows.forEach(row => {
                row.style.display = this.checked ? 'none' : '';
            });
        });
    }
});

function toggleDetails(index) {
    const details = document.getElementById('details-' + index);
    if (details) {
        details.classList.toggle('show');
    }
}

function toggleAllDetails() {
    const allDetails = document.querySelectorAll('.test-details');
    const anyVisible = Array.from(allDetails).some(detail => detail.classList.contains('show'));
    
    allDetails.forEach(detail => {
        if (anyVisible) {
            detail.classList.remove('show');
        } else {
            detail.classList.add('show');
        }
    });
}
"""
    
    with open("pytest-report/script.js", "w") as f:
        f.write(js_content)


def generate_coverage_style_report():
    """Generate a coverage-style HTML report with external CSS/JS."""
    
    # Create pytest-report directory
    os.makedirs("pytest-report", exist_ok=True)
    
    # Create external CSS and JS files
    create_css_file()
    create_js_file()
    
    # Check if JSON report exists
    if not os.path.exists("test-results.json"):
        print("❌ test-results.json not found. Running pytest first...")
        if not run_pytest_with_json():
            print("❌ Failed to generate test results")
            return False
    
    # Load test results
    try:
        with open("test-results.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load test results: {e}")
        return False
    
    tests = data.get("tests", [])
    summary = data.get("summary", {})
    
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)
    total = summary.get("total", 0)
    duration = summary.get("duration", 0)
    
    # Calculate pass rate
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    # Generate main HTML file
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Pytest Test Report</title>
    <link rel="stylesheet" href="style.css" type="text/css">
    <script src="script.js" defer></script>
</head>
<body class="indexfile">
<header>
    <div class="content">
        <h1>Pytest Test Report:
            <span class="pc_cov">{pass_rate:.1f}%</span>
        </h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</header>

<main>
    <div class="content">
        <div class="summary">
            <h2>Test Summary</h2>
            <div class="stats">
                <div class="stat-box total">
                    <div class="stat-number">{total}</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                <div class="stat-box passed">
                    <div class="stat-number">{passed}</div>
                    <div class="stat-label">Passed</div>
                </div>
                <div class="stat-box failed">
                    <div class="stat-number">{failed}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-box skipped">
                    <div class="stat-number">{skipped}</div>
                    <div class="stat-label">Skipped</div>
                </div>
            </div>
            <p><strong>Duration:</strong> {duration:.2f} seconds | <strong>Pass Rate:</strong> {pass_rate:.1f}%</p>
        </div>
        
        <div class="filter-section">
            <input type="text" id="filter" placeholder="Filter tests...">
            <label><input type="checkbox" id="hide-passed"> Hide passed tests</label>
            <button class="toggle-all" onclick="toggleAllDetails()">Toggle All Details</button>
        </div>
        
        <div class="results-table">
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add test rows
    for i, test in enumerate(tests):
        test_name = test.get("nodeid", "Unknown Test")
        outcome = test.get("outcome", "unknown")
        duration = test.get("duration", 0)
        
        html_content += f"""
                    <tr data-status="{outcome}">
                        <td class="test-name">{test_name}</td>
                        <td><span class="status {outcome}">{outcome}</span></td>
                        <td class="duration">{duration:.3f}s</td>
                        <td><button class="details-toggle" onclick="toggleDetails({i})">Details</button></td>
                    </tr>
                    <tr>
                        <td colspan="4">
                            <div class="test-details" id="details-{i}">
                                <p><strong>File:</strong> {test.get('file', 'N/A')}</p>
                                <p><strong>Function:</strong> {test.get('function', 'N/A')}</p>
                                <p><strong>Duration:</strong> {duration:.3f} seconds</p>
"""
        
        # Add failure details if test failed
        if outcome == "failed" and "call" in test:
            longrepr = test["call"].get("longrepr", "No details available")
            html_content += f"""
                                <p><strong>Failure Details:</strong></p>
                                <pre>{longrepr}</pre>
"""
        
        html_content += """
                            </div>
                        </td>
                    </tr>
"""
    
    html_content += """
                </tbody>
            </table>
        </div>
    </div>
</main>
</body>
</html>
"""
    
    # Write main HTML file
    try:
        with open("pytest-report/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ Coverage-style pytest report generated in pytest-report/")
        print("   - Main file: pytest-report/index.html")
        print("   - CSS file: pytest-report/style.css")
        print("   - JS file: pytest-report/script.js")
        return True
    except Exception as e:
        print(f"❌ Failed to write HTML report: {e}")
        return False


if __name__ == "__main__":
    # Try to install pytest-json-report if not available
    try:
        import pytest_jsonreport
    except ImportError:
        print("📦 Installing pytest-json-report...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest-json-report"], check=True)
    
    success = generate_coverage_style_report()
    sys.exit(0 if success else 1)
