pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                git 'https://github.com/Gianpy99/CI_CD_Validation.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                '''
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo 'Running code quality checks...'
                sh '''
                    python3 -m flake8 app.py test_app.py --output-file=flake8-report.txt || true
                '''
                archiveArtifacts artifacts: 'flake8-report.txt', allowEmptyArchive: true
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running comprehensive testing...'
                sh '''
                    # Create test reports directory
                    mkdir -p test-reports
                    
                    # Run unittest tests first - FAIL BUILD IF THESE FAIL
                    echo "=== Running unittest tests ==="
                    python3 -m unittest test_app.py -v | tee test-reports/unittest-output.txt
                    UNITTEST_STATUS=${PIPESTATUS[0]}
                    
                    # Run pytest tests - FAIL BUILD IF THESE FAIL  
                    echo "=== Running pytest tests ==="
                    python3 -m pytest test_app_pytest.py -v \\
                        --junitxml=test-reports/pytest-results.xml \\
                        --html=test-reports/pytest-report.html --self-contained-html \\
                        --tb=short | tee test-reports/pytest-output.txt
                    PYTEST_STATUS=${PIPESTATUS[0]}
                    
                    # Generate coverage (optional, don't fail build)
                    echo "=== Generating coverage report ==="
                    python3 -m coverage run --source=. -m unittest test_app.py || true
                    python3 -m coverage xml -o test-reports/coverage.xml || true
                    python3 -m coverage html -d test-reports/htmlcov || true
                    python3 -m coverage report | tee test-reports/coverage-summary.txt || true
                    
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
            cleanWs()
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
