#!/usr/bin/env python3
"""
Custom pytest report generator for Jenkins compatibility.
This creates a fully functional HTML report with inline CSS and JavaScript
that works around Jenkins CSP restrictions.
"""

import json
import os
import sys
from datetime import datetime
import subprocess


def run_pytest_with_json():
    """Run pytest and capture results in JSON format."""
    print("🧪 Running pytest to collect test results...")
    
    # Run pytest with JSON report
    cmd = [sys.executable, "-m", "pytest", "--tb=short", "-v", "--json-report", "--json-report-file=test-results.json"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Pytest exit code: {result.returncode}")
        if result.stdout:
            print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running pytest: {e}")
        return False


def generate_jenkins_compatible_report():
    """Generate a Jenkins-compatible HTML report from JSON results."""
    
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
    
    # Extract test information
    tests = data.get("tests", [])
    summary = data.get("summary", {})
    
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)
    total = summary.get("total", 0)
    duration = summary.get("duration", 0)
    
    # Generate HTML report
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jenkins Pytest Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #6c757d;
        }}
        .stat-card.passed {{ border-left-color: #28a745; }}
        .stat-card.failed {{ border-left-color: #dc3545; }}
        .stat-card.skipped {{ border-left-color: #ffc107; }}
        .stat-card.total {{ border-left-color: #007bff; }}
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #6c757d;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .tests-section {{
            margin-top: 30px;
        }}
        .test-item {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            margin-bottom: 10px;
            overflow: hidden;
        }}
        .test-header {{
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            cursor: pointer;
            display: flex;
            justify-content: between;
            align-items: center;
            transition: background-color 0.2s;
        }}
        .test-header:hover {{
            background: #e9ecef;
        }}
        .test-name {{
            flex: 1;
            font-weight: 500;
        }}
        .test-status {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .status-passed {{
            background: #d4edda;
            color: #155724;
        }}
        .status-failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        .status-skipped {{
            background: #fff3cd;
            color: #856404;
        }}
        .test-details {{
            display: none;
            padding: 20px;
            background: #ffffff;
            border-top: 1px solid #e9ecef;
        }}
        .test-details.show {{
            display: block;
        }}
        .toggle-btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
            margin: 20px 0;
        }}
        .toggle-btn:hover {{
            background: #0056b3;
        }}
        .duration {{
            color: #6c757d;
            font-size: 0.9rem;
            margin-left: 15px;
        }}
        pre {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Jenkins Pytest Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="stat-card total">
                <div class="stat-number">{total}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card passed">
                <div class="stat-number">{passed}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card failed">
                <div class="stat-number">{failed}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card skipped">
                <div class="stat-number">{skipped}</div>
                <div class="stat-label">Skipped</div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <p><strong>Duration:</strong> {duration:.2f} seconds</p>
            <button class="toggle-btn" onclick="toggleAllDetails()">Show/Hide All Details</button>
        </div>
        
        <div class="tests-section">
            <h2>Test Results</h2>
"""
    
    # Add individual test results
    for i, test in enumerate(tests):
        test_name = test.get("nodeid", "Unknown Test")
        outcome = test.get("outcome", "unknown")
        duration = test.get("duration", 0)
        
        status_class = f"status-{outcome}"
        
        html_content += f"""
            <div class="test-item">
                <div class="test-header" onclick="toggleDetails({i})">
                    <span class="test-name">{test_name}</span>
                    <span class="duration">{duration:.3f}s</span>
                    <span class="test-status {status_class}">{outcome}</span>
                </div>
                <div class="test-details" id="details-{i}">
                    <h4>Test Details:</h4>
                    <p><strong>File:</strong> {test.get('file', 'N/A')}</p>
                    <p><strong>Function:</strong> {test.get('function', 'N/A')}</p>
                    <p><strong>Duration:</strong> {duration:.3f} seconds</p>
"""
        
        # Add failure information if test failed
        if outcome == "failed" and "call" in test:
            longrepr = test["call"].get("longrepr", "No details available")
            html_content += f"""
                    <h4>Failure Details:</h4>
                    <pre>{longrepr}</pre>
"""
        
        html_content += """
                </div>
            </div>
"""
    
    # Add JavaScript for interactivity
    html_content += """
        </div>
    </div>
    
    <script>
        function toggleDetails(index) {
            const details = document.getElementById('details-' + index);
            if (details.classList.contains('show')) {
                details.classList.remove('show');
            } else {
                details.classList.add('show');
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
        
        // Auto-expand failed tests
        document.addEventListener('DOMContentLoaded', function() {
            const failedTests = document.querySelectorAll('.status-failed');
            failedTests.forEach((status, index) => {
                const testItem = status.closest('.test-item');
                const details = testItem.querySelector('.test-details');
                if (details) {
                    details.classList.add('show');
                }
            });
        });
    </script>
</body>
</html>
"""
    
    # Write the HTML report
    try:
        with open("jenkins-pytest-report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ Jenkins-compatible HTML report generated: jenkins-pytest-report.html")
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
    
    success = generate_jenkins_compatible_report()
    sys.exit(0 if success else 1)
