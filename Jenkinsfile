pipeline {
    agent any

    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    # Use python3 if available, otherwise python
                    if command -v python3 >/dev/null 2>&1; then
                        PYTHON_CMD="python3"
                    elif command -v python >/dev/null 2>&1; then
                        PYTHON_CMD="python"
                    else
                        echo "❌ Neither python3 nor python found!"
                        exit 1
                    fi
                    
                    echo "✅ Using $PYTHON_CMD"
                    $PYTHON_CMD --version
                    
                    echo "📦 Upgrading pip and installing requirements..."
                    # Try without --break-system-packages first for broader compatibility
                    if ! $PYTHON_CMD -m pip install --upgrade pip; then
                        echo "Retrying pip upgrade with --break-system-packages..."
                        $PYTHON_CMD -m pip install --upgrade pip --break-system-packages
                    fi

                    if ! $PYTHON_CMD -m pip install -r requirements.txt; then
                        echo "Retrying requirements install with --break-system-packages..."
                        $PYTHON_CMD -m pip install -r requirements.txt --break-system-packages
                    fi
                    
                    echo "✅ Dependencies installed successfully."
                '''
                
                // Environment is ready for HTML publishing
                echo "✅ Environment configured for HTML report publishing"
            }
        }

        stage('Code Quality Check') {
            steps {
                echo 'Running code quality checks with flake8...'
                sh '''
                    # Use python3 if available, otherwise python
                    if command -v python3 >/dev/null 2>&1; then
                        PYTHON_CMD="python3"
                    elif command -v python >/dev/null 2>&1; then
                        PYTHON_CMD="python"
                    else
                        echo "❌ Neither python3 nor python found!"
                        exit 1
                    fi

                    echo "Generating flake8 reports..."
                    # Generate text report, continue on error to not block the pipeline
                    $PYTHON_CMD -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --output-file=flake8-report.txt || true
                    # Generate detailed text report for custom HTML conversion
                    $PYTHON_CMD -m flake8 . --show-source --statistics --output-file=flake8-detailed.txt || true
                    
                    echo "🎨 Generating custom flake8 HTML report..."
                    # Generate custom HTML report using our script
                    $PYTHON_CMD generate_flake8_report.py
                '''
                archiveArtifacts artifacts: 'flake8-report.*', allowEmptyArchive: true
            }
        }

        stage('Run Tests and Generate Reports') {
            steps {
                echo 'Running tests with pytest and generating reports...'
                sh '''
                    # Use python3 if available, otherwise python
                    if command -v python3 >/dev/null 2>&1; then
                        PYTHON_CMD="python3"
                    elif command -v python >/dev/null 2>&1; then
                        PYTHON_CMD="python"
                    else
                        echo "❌ Neither python3 nor python found!"
                        exit 1
                    fi

                    echo "🧪 Running pytest with verbose output..."
                    # Generate standard HTML report (may have JS issues in Jenkins)
                    $PYTHON_CMD -m pytest --html=pytest-report.html --self-contained-html --verbose
                    
                    echo "🚀 Generating Jenkins-compatible HTML report..."
                    # Generate Jenkins-compatible report that bypasses CSP issues
                    $PYTHON_CMD generate_jenkins_report.py
                    
                    echo "📊 Generating Coverage-style pytest report..."
                    # Generate coverage-style report with external CSS/JS (like coverage.py)
                    $PYTHON_CMD generate_coverage_style_report.py
                    
                    echo "📋 Generating reports dashboard..."
                    # Generate a dashboard page with links to all reports
                    $PYTHON_CMD generate_reports_dashboard.py
                    
                    # Verify all reports were created
                    if [ -f "pytest-report.html" ]; then
                        echo "✅ Standard pytest-report.html generated successfully"
                        ls -la pytest-report.html
                    else
                        echo "❌ Standard pytest-report.html was not generated!"
                    fi
                    
                    if [ -f "jenkins-pytest-report.html" ]; then
                        echo "✅ Jenkins-compatible report generated successfully"
                        ls -la jenkins-pytest-report.html
                    else
                        echo "❌ Jenkins-compatible report was not generated!"
                    fi
                    
                    if [ -d "pytest-report" ] && [ -f "pytest-report/index.html" ]; then
                        echo "✅ Coverage-style pytest report generated successfully"
                        ls -la pytest-report/
                    else
                        echo "❌ Coverage-style pytest report was not generated!"
                    fi
                    
                    if [ -f "reports-dashboard.html" ]; then
                        echo "✅ Reports dashboard generated successfully"
                        ls -la reports-dashboard.html
                    else
                        echo "❌ Reports dashboard was not generated!"
                    fi
                    
                    # Verify flake8 report was created
                    if [ -f "flake8-report.html" ]; then
                        echo "✅ Custom flake8 HTML report generated successfully"
                        ls -la flake8-report.html
                        echo "Report size: $(wc -c < flake8-report.html) bytes"
                    else
                        echo "❌ Custom flake8 HTML report was not generated!"
                    fi
                    
                    echo "📊 Running coverage analysis..."
                    $PYTHON_CMD -m coverage run -m pytest
                    $PYTHON_CMD -m coverage report
                    $PYTHON_CMD -m coverage html -d coverage-html
                    
                    # Verify coverage report was created
                    if [ -d "coverage-html" ] && [ -f "coverage-html/index.html" ]; then
                        echo "✅ Coverage HTML report generated successfully"
                        ls -la coverage-html/
                    else
                        echo "❌ Coverage HTML report was not generated!"
                    fi
                '''
            }
        }

        stage('Publish Reports') {
            steps {
                echo 'Publishing HTML reports...'
                
                script {
                    try {
                        // Publish Reports Dashboard (MAIN ENTRY POINT)
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: '.',
                            reportFiles: 'reports-dashboard.html',
                            reportName: 'Reports Dashboard',
                            reportTitles: 'All Test Reports'
                        ])
                        echo "✅ Reports dashboard published successfully"
                    } catch (Exception e) {
                        echo "❌ Failed to publish reports dashboard: ${e.getMessage()}"
                    }
                    
                    try {
                        // Publish Coverage-style Pytest report (PRIMARY - RECOMMENDED)
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: 'pytest-report',
                            reportFiles: 'index.html',
                            reportName: 'Pytest Report (Coverage-Style)',
                            reportTitles: 'Coverage-Style Test Results'
                        ])
                        echo "✅ Coverage-style pytest report published successfully"
                    } catch (Exception e) {
                        echo "❌ Failed to publish coverage-style pytest report: ${e.getMessage()}"
                    }
                    
                    try {
                        // Publish Jenkins-compatible Pytest report (backup)
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: '.',
                            reportFiles: 'jenkins-pytest-report.html',
                            reportName: 'Jenkins Pytest Report (Single File)',
                            reportTitles: 'Single File Test Results'
                        ])
                        echo "✅ Jenkins-compatible pytest report published successfully"
                    } catch (Exception e) {
                        echo "❌ Failed to publish Jenkins-compatible pytest report: ${e.getMessage()}"
                    }
                    
                    try {
                        // Publish standard Pytest HTML report (fallback)
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: '.',
                            reportFiles: 'pytest-report.html',
                            reportName: 'Pytest HTML Report (Standard)',
                            reportTitles: 'Standard Test Results'
                        ])
                        echo "✅ Standard pytest HTML report published successfully"
                    } catch (Exception e) {
                        echo "❌ Failed to publish standard pytest HTML report: ${e.getMessage()}"
                        echo "📂 Listing workspace files for debugging:"
                        sh 'ls -la *.html || echo "No HTML files found"'
                    }
                    
                    try {
                        // Publish Coverage HTML report
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: 'coverage-html',
                            reportFiles: 'index.html',
                            reportName: 'Coverage HTML Report',
                            reportTitles: 'Coverage Report'
                        ])
                        echo "✅ Coverage HTML report published successfully"
                    } catch (Exception e) {
                        echo "❌ Failed to publish Coverage HTML report: ${e.getMessage()}"
                    }
                    
                    try {
                        // Publish Flake8 HTML report
                        publishHTML([
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: '.',
                            reportFiles: 'flake8-report.html',
                            reportName: 'Flake8 HTML Report',
                            reportTitles: 'Code Quality Report'
                        ])
                        echo "✅ Flake8 HTML report published successfully"
                    } catch (Exception e) {
                        echo "❌ Failed to publish Flake8 HTML report: ${e.getMessage()}"
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline finished. Archiving all reports...'
            
            // Archive artifacts as fallback
            archiveArtifacts artifacts: '**/pytest-report.html, **/jenkins-pytest-report.html, **/pytest-report/*, **/coverage-html/*, **/flake8-report.html, **/flake8-report.txt, **/reports-dashboard.html', allowEmptyArchive: true
            
            // Create direct links to reports in build description
            script {
                try {
                    def buildUrl = env.BUILD_URL
                    
                    // Simple text description that will definitely work
                    def plainTextLinks = """� Test Reports Dashboard: ${buildUrl}artifact/reports-dashboard.html

Quick Links:
• Coverage-Style Pytest Report: ${buildUrl}artifact/pytest-report/index.html
• Single-File Pytest Report: ${buildUrl}artifact/jenkins-pytest-report.html
• Standard Pytest Report: ${buildUrl}artifact/pytest-report.html
• Coverage Report: ${buildUrl}artifact/coverage-html/index.html
• Code Quality Report: ${buildUrl}artifact/flake8-report.html"""
                    
                    currentBuild.description = plainTextLinks
                    echo "✅ Build description updated with report links"
                } catch (Exception e) {
                    echo "⚠️ Could not update build description: ${e.getMessage()}"
                }
            }
        }
        success {
            echo '✅ Pipeline successful! All tests passed and reports generated.'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs and reports for details.'
        }
    }
}
