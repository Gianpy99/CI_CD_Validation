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
                    # Generate HTML report, requires flake8-html package (in requirements.txt)
                    $PYTHON_CMD -m flake8 . --format=html --output-file=flake8-report.html || true
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

                    echo "Running pytest..."
                    # Generate a self-contained HTML report to ensure JS works correctly
                    $PYTHON_CMD -m pytest --html=pytest-report.html --self-contained-html
                    
                    echo "Running coverage..."
                    $PYTHON_CMD -m coverage run -m pytest
                    $PYTHON_CMD -m coverage report
                    $PYTHON_CMD -m coverage html -d coverage-html
                '''
            }
        }

        stage('Publish Reports') {
            steps {
                echo 'Publishing HTML reports...'
                
                // Publish Pytest HTML report
                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'pytest-report.html',
                    reportName: 'Pytest HTML Report'
                ])
                
                // Publish Coverage HTML report
                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'coverage-html',
                    reportFiles: 'index.html',
                    reportName: 'Coverage HTML Report'
                ])
                
                // Publish Flake8 HTML report
                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'flake8-report.html',
                    reportName: 'Flake8 HTML Report'
                ])
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline finished. Archiving all reports...'
            archiveArtifacts artifacts: '**/pytest-report.html, **/coverage-html/*, **/flake8-report.*', allowEmptyArchive: true
        }
        success {
            echo '✅ Pipeline successful!'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
