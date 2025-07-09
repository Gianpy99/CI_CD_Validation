#!/usr/bin/env python3
"""
Generate a custom flake8 HTML report from text output.
This creates a clean, modern HTML report for code quality issues.
"""

import os
import re
import subprocess
import sys
from datetime import datetime


def run_flake8():
    """Run flake8 and capture output."""
    print("🔍 Running flake8 analysis...")
    
    # Run flake8 with detailed output - only on main files
    cmd = [sys.executable, "-m", "flake8", "app.py", "test_app.py", "--show-source", "--statistics"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        print(f"Error running flake8: {e}")
        return "", f"Error: {e}", 1


def parse_flake8_output(output):
    """Parse flake8 output into structured data."""
    issues = []
    statistics = []
    
    lines = output.split('\n')
    in_statistics = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('--'):
            continue
            
        # Check for statistics section
        if 'count' in line.lower() and 'filename' in line.lower():
            in_statistics = True
            continue
            
        if in_statistics:
            if re.match(r'^\d+', line):
                statistics.append(line)
            continue
            
        # Parse issue lines (format: file:line:col: code message)
        match = re.match(r'^([^:]+):(\d+):(\d+):\s*([A-Z]\d+)\s+(.+)$', line)
        if match:
            issues.append({
                'file': match.group(1),
                'line': int(match.group(2)),
                'column': int(match.group(3)),
                'code': match.group(4),
                'message': match.group(5)
            })
    
    return issues, statistics


def get_issue_severity(code):
    """Get severity level and color for issue code."""
    if code.startswith('E9') or code.startswith('F'):
        return 'error', '#dc3545'
    elif code.startswith('E'):
        return 'warning', '#ffc107'
    elif code.startswith('W'):
        return 'info', '#17a2b8'
    else:
        return 'other', '#6c757d'


def generate_flake8_html_report():
    """Generate HTML report for flake8."""
    
    stdout, stderr, returncode = run_flake8()
    
    if returncode != 0 and not stdout:
        # No issues found or flake8 not available
        stdout = "No code quality issues found!" if not stderr else stderr
    
    issues, statistics = parse_flake8_output(stdout)
    
    # Count issues by severity
    error_count = len([i for i in issues if get_issue_severity(i['code'])[0] == 'error'])
    warning_count = len([i for i in issues if get_issue_severity(i['code'])[0] == 'warning'])
    info_count = len([i for i in issues if get_issue_severity(i['code'])[0] == 'info'])
    total_count = len(issues)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Quality Report (Flake8)</title>
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
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            text-align: center;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #6c757d;
        }}
        .stat-card.error {{ border-left-color: #dc3545; background: #f8d7da; }}
        .stat-card.warning {{ border-left-color: #ffc107; background: #fff3cd; }}
        .stat-card.info {{ border-left-color: #17a2b8; background: #d1ecf1; }}
        .stat-card.total {{ border-left-color: #007bff; background: #d1ecf1; }}
        .stat-number {{
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            font-size: 0.9rem;
            color: #666;
        }}
        .issues-section {{
            margin-top: 30px;
        }}
        .issue-item {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            margin-bottom: 10px;
            padding: 15px;
        }}
        .issue-header {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        .issue-badge {{
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-right: 10px;
            color: white;
        }}
        .issue-location {{
            font-family: monospace;
            color: #666;
            font-size: 0.9rem;
        }}
        .issue-message {{
            color: #333;
            margin-top: 5px;
        }}
        .no-issues {{
            text-align: center;
            padding: 40px;
            color: #28a745;
            font-size: 1.2rem;
        }}
        .filter-section {{
            margin-bottom: 20px;
        }}
        .filter-section input {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-right: 10px;
            width: 200px;
        }}
        .filter-section label {{
            margin-right: 15px;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Code Quality Report</h1>
            <p>Generated by flake8 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="stat-card total">
                <div class="stat-number">{total_count}</div>
                <div class="stat-label">Total Issues</div>
            </div>
            <div class="stat-card error">
                <div class="stat-number">{error_count}</div>
                <div class="stat-label">Errors</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-number">{warning_count}</div>
                <div class="stat-label">Warnings</div>
            </div>
            <div class="stat-card info">
                <div class="stat-number">{info_count}</div>
                <div class="stat-label">Style Issues</div>
            </div>
        </div>
"""
    
    if not issues:
        html_content += """
        <div class="no-issues">
            <h2>🎉 No Code Quality Issues Found!</h2>
            <p>Your code follows all the configured style guidelines.</p>
        </div>
"""
    else:
        html_content += """
        <div class="filter-section">
            <input type="text" id="filter" placeholder="Filter by file or message...">
            <label><input type="checkbox" id="hide-info"> Hide style issues</label>
        </div>
        
        <div class="issues-section">
            <h2>Issues Found</h2>
"""
        
        # Group issues by file
        files = {}
        for issue in issues:
            if issue['file'] not in files:
                files[issue['file']] = []
            files[issue['file']].append(issue)
        
        for filename, file_issues in files.items():
            html_content += f"""
            <h3>📄 {filename}</h3>
"""
            
            for issue in file_issues:
                severity, color = get_issue_severity(issue['code'])
                html_content += f"""
            <div class="issue-item" data-severity="{severity}">
                <div class="issue-header">
                    <span class="issue-badge" style="background-color: {color};">{issue['code']}</span>
                    <span class="issue-location">Line {issue['line']}, Column {issue['column']}</span>
                </div>
                <div class="issue-message">{issue['message']}</div>
            </div>
"""
        
        html_content += """
        </div>
"""
    
    # Add statistics if available
    if statistics:
        html_content += """
        <div class="statistics-section" style="margin-top: 30px;">
            <h3>📊 Statistics</h3>
            <pre style="background: #f8f9fa; padding: 15px; border-radius: 4px;">"""
        
        for stat in statistics:
            html_content += f"{stat}\n"
        
        html_content += """</pre>
        </div>
"""
    
    html_content += """
    </div>
    
    <script>
        document.getElementById('filter').addEventListener('input', function() {
            const filterValue = this.value.toLowerCase();
            const issues = document.querySelectorAll('.issue-item');
            
            issues.forEach(issue => {
                const text = issue.textContent.toLowerCase();
                issue.style.display = text.includes(filterValue) ? 'block' : 'none';
            });
        });
        
        document.getElementById('hide-info').addEventListener('change', function() {
            const infoIssues = document.querySelectorAll('.issue-item[data-severity="info"]');
            infoIssues.forEach(issue => {
                issue.style.display = this.checked ? 'none' : 'block';
            });
        });
    </script>
</body>
</html>"""
    
    try:
        with open("flake8-report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ Flake8 HTML report generated: flake8-report.html")
        return True
    except Exception as e:
        print(f"❌ Failed to write flake8 HTML report: {e}")
        return False


if __name__ == "__main__":
    generate_flake8_html_report()
