pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    echo "🔍 Checking Python availability..."
                    
                    # Check if Python is available
                    if command -v python3 >/dev/null 2>&1; then
                        PYTHON_CMD="python3"
                        echo "✅ Found python3: $(which python3)"
                        $PYTHON_CMD --version
                    elif command -v python >/dev/null 2>&1; then
                        PYTHON_CMD="python"
                        echo "✅ Found python: $(which python)"
                        $PYTHON_CMD --version
                    else
                        echo "❌ No Python found!"
                        echo "Please install Python in the Jenkins container manually"
                        exit 1
                    fi
                    
                    echo "🎯 Using Python command: $PYTHON_CMD"
                    
                    # Check pip
                    if $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
                        echo "✅ pip available"
                    else
                        echo "❌ pip not available!"
                        exit 1
                    fi
                    
                    # Install requirements
                    echo "📦 Installing packages..."
                    $PYTHON_CMD -m pip install --upgrade pip --break-system-packages || $PYTHON_CMD -m pip install --upgrade pip
                    $PYTHON_CMD -m pip install --break-system-packages -r requirements.txt || $PYTHON_CMD -m pip install -r requirements.txt
                '''
            }
        }
        
        stage('Debug Environment') {
            steps {
                echo 'Running environment debug...'
                sh '''
                    chmod +x debug-jenkins.sh
                    ./debug-jenkins.sh
                '''
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo 'Running code quality checks...'
                sh '''
                    # Determine Python command (python first, then python3)
                    if command -v python >/dev/null 2>&1; then
                        PYTHON_CMD="python"
                    elif command -v python3 >/dev/null 2>&1; then
                        PYTHON_CMD="python3"
                    else
                        echo "❌ No Python found!"
                        exit 1
                    fi
                    
                    $PYTHON_CMD -m flake8 app.py test_app.py --output-file=flake8-report.txt || true
                '''
                archiveArtifacts artifacts: 'flake8-report.txt', allowEmptyArchive: true
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running comprehensive testing...'
                sh '''
                    # Determine Python command (python first, then python3)
                    if command -v python >/dev/null 2>&1; then
                        PYTHON_CMD="python"
                    elif command -v python3 >/dev/null 2>&1; then
                        PYTHON_CMD="python3"
                    else
                        echo "❌ No Python found!"
                        exit 1
                    fi
                    
                    echo "Using Python command: $PYTHON_CMD"
                    
                    # Create test reports directory
                    mkdir -p test-reports
                    
                    # Run unittest tests first - FAIL BUILD IF THESE FAIL
                    echo "=== Running unittest tests ==="
                    set +e  # Don't exit immediately on error
                    $PYTHON_CMD -m unittest test_app.py -v > test-reports/unittest-output.txt 2>&1
                    UNITTEST_STATUS=$?
                    cat test-reports/unittest-output.txt
                    
                    # Run pytest tests - FAIL BUILD IF THESE FAIL  
                    echo "=== Running pytest tests ==="
                    $PYTHON_CMD -m pytest test_app_pytest.py -v \\
                        --junitxml=test-reports/pytest-results.xml \\
                        --html=test-reports/pytest-report.html --self-contained-html \\
                        --tb=short > test-reports/pytest-output.txt 2>&1
                    PYTEST_STATUS=$?
                    cat test-reports/pytest-output.txt
                    set -e  # Re-enable exit on error
                    
                    # Generate coverage (optional, don't fail build)
                    echo "=== Generating coverage report ==="
                    $PYTHON_CMD -m coverage run --source=. -m unittest test_app.py || true
                    $PYTHON_CMD -m coverage xml -o test-reports/coverage.xml || true
                    $PYTHON_CMD -m coverage html -d test-reports/htmlcov || true
                    $PYTHON_CMD -m coverage report | tee test-reports/coverage-summary.txt || true
                    
                    # Create build summary
                    echo "=== BUILD SUMMARY ===" | tee test-reports/test-summary.txt
                    echo "Build Number: ${BUILD_NUMBER}" >> test-reports/test-summary.txt
                    echo "Timestamp: $(date)" >> test-reports/test-summary.txt
                    echo "Branch: ${GIT_BRANCH}" >> test-reports/test-summary.txt
                    echo "" >> test-reports/test-summary.txt
                    
                    if [ $UNITTEST_STATUS -eq 0 ]; then
                        echo "✅ UNITTEST: PASSED" | tee -a test-reports/test-summary.txt
                    else
                        echo "❌ UNITTEST: FAILED" | tee -a test-reports/test-summary.txt
                    fi
                    
                    if [ $PYTEST_STATUS -eq 0 ]; then
                        echo "✅ PYTEST: PASSED" | tee -a test-reports/test-summary.txt
                    else
                        echo "❌ PYTEST: FAILED" | tee -a test-reports/test-summary.txt
                    fi
                    
                    echo "" >> test-reports/test-summary.txt
                    echo "Coverage Summary:" >> test-reports/test-summary.txt
                    cat test-reports/coverage-summary.txt >> test-reports/test-summary.txt || echo "Coverage not available" >> test-reports/test-summary.txt
                    
                    # Display final summary
                    echo ""
                    echo "📋 FINAL BUILD SUMMARY 📋"
                    cat test-reports/test-summary.txt
                    echo ""
                    
                    # CRITICAL: Check if any tests failed and FAIL THE BUILD
                    if [ $UNITTEST_STATUS -ne 0 ] || [ $PYTEST_STATUS -ne 0 ]; then
                        echo "🚨🚨🚨 BUILD FAILURE! TESTS FAILED! 🚨🚨🚨"
                        echo "� BLOCKING DEPLOYMENT TO PROTECT PRODUCTION"
                        echo "🔧 Fix the failing tests and commit again"
                        echo ""
                        echo "Exit codes:"
                        echo "  - Unittest: $UNITTEST_STATUS"
                        echo "  - Pytest: $PYTEST_STATUS"
                        echo ""
                        exit 1
                    fi
                    
                    echo "✅ ALL TESTS PASSED! BUILD SUCCESS!"
                    echo "🚀 Safe to proceed with deployment"
                '''
            }
            post {
                always {
                    // Pubblica risultati dei test JUnit
                    junit testResults: 'test-reports/pytest-results.xml', allowEmptyResults: true
                    
                    // Pubblica report HTML dei test
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'test-reports',
                        reportFiles: 'pytest-report.html',
                        reportName: 'Pytest Report',
                        reportTitles: 'Test Results'
                    ])
                    
                    // Pubblica report di coverage
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'test-reports/htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report',
                        reportTitles: 'Code Coverage'
                    ])
                    
                    // Archivia tutti i report
                    archiveArtifacts artifacts: 'test-reports/**/*', allowEmptyArchive: true, fingerprint: true
                }
            }
        }
        
        stage('Build Artifact') {
            steps {
                echo 'Creating build artifact...'
                sh '''
                    mkdir -p dist
                    cp app.py dist/
                    echo "Build completed on $(date)" > dist/build-info.txt
                    echo "Commit: $GIT_COMMIT" >> dist/build-info.txt
                    echo "Branch: $GIT_BRANCH" >> dist/build-info.txt
                    tar -czf app-${BUILD_NUMBER}.tar.gz dist/
                '''
                archiveArtifacts artifacts: 'app-*.tar.gz', fingerprint: true
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to staging environment...'
                sh '''
                    echo "Simulating deployment to staging..."
                    echo "Application deployed successfully to staging at $(date)" > deployment-log.txt
                '''
                archiveArtifacts artifacts: 'deployment-log.txt', allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            echo '📋 Pipeline completed!'
            script {
                // Stampa un summary finale molto chiaro
                echo """
                =====================================
                🚀 JENKINS BUILD SUMMARY
                =====================================
                Build: #${BUILD_NUMBER}
                Status: ${currentBuild.result ?: 'SUCCESS'}
                Duration: ${currentBuild.durationString}
                Workspace: ${WORKSPACE}
                =====================================
                📊 REPORTS AVAILABLE:
                • Test Results (JUnit): Check 'Test Results' tab
                • Pytest Report: Check 'Pytest Report' link  
                • Coverage Report: Check 'Coverage Report' link
                • Build Artifacts: Check 'Build Artifacts' section
                =====================================
                """
            }
            // cleanWs() non disponibile in questa installazione Jenkins
        }
        success {
            echo '✅ Pipeline succeeded! 🎉'
            script {
                echo """
                🎉 BUILD SUCCESSFUL! 
                All tests passed. Ready for deployment.
                Check the reports above for detailed metrics.
                """
            }
        }
        failure {
            echo '❌ Pipeline failed! 💥'
            script {
                echo """
                💥 BUILD FAILED!
                Check the console output and test reports for details.
                Fix the issues and try again.
                """
            }
        }
        unstable {
            echo '⚠️ Pipeline unstable! Some tests failed.'
            script {
                echo """
                ⚠️ BUILD UNSTABLE!
                Some tests failed but build artifacts were created.
                Check test reports to see which tests failed.
                Review the 'Test Results' and 'Pytest Report' for details.
                """
            }
        }
    }
}
