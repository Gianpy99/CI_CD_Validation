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
                    
                    # Run unittest tests first
                    echo "=== Running unittest tests ==="
                    python3 -m unittest test_app.py -v > test-reports/unittest-output.txt 2>&1 || echo "UNITTEST_FAILED=true" > test-reports/unittest-status.txt
                    
                    # Run pytest tests with detailed output
                    echo "=== Running pytest tests ==="
                    python3 -m pytest test_app_pytest.py -v \\
                        --junitxml=test-reports/pytest-results.xml \\
                        --html=test-reports/pytest-report.html --self-contained-html \\
                        --tb=short > test-reports/pytest-output.txt 2>&1 || echo "PYTEST_FAILED=true" > test-reports/pytest-status.txt
                    
                    # Generate coverage if available
                    echo "=== Generating coverage report ==="
                    python3 -m coverage run --source=. -m unittest test_app.py || true
                    python3 -m coverage xml -o test-reports/coverage.xml || true
                    python3 -m coverage html -d test-reports/htmlcov || true
                    python3 -m coverage report > test-reports/coverage-summary.txt || true
                    
                    # Create consolidated test summary
                    echo "=== Test Summary ===" > test-reports/test-summary.txt
                    echo "Build Number: ${BUILD_NUMBER}" >> test-reports/test-summary.txt
                    echo "Timestamp: $(date)" >> test-reports/test-summary.txt
                    echo "Branch: ${GIT_BRANCH}" >> test-reports/test-summary.txt
                    echo "" >> test-reports/test-summary.txt
                    
                    if [ -f test-reports/unittest-status.txt ]; then
                        echo "❌ UNITTEST: FAILED" >> test-reports/test-summary.txt
                    else
                        echo "✅ UNITTEST: PASSED" >> test-reports/test-summary.txt
                    fi
                    
                    if [ -f test-reports/pytest-status.txt ]; then
                        echo "❌ PYTEST: FAILED" >> test-reports/test-summary.txt
                    else
                        echo "✅ PYTEST: PASSED" >> test-reports/test-summary.txt
                    fi
                    
                    echo "" >> test-reports/test-summary.txt
                    echo "=== Coverage Summary ===" >> test-reports/test-summary.txt
                    cat test-reports/coverage-summary.txt >> test-reports/test-summary.txt || echo "Coverage not available" >> test-reports/test-summary.txt
                    
                    # Display summary in console
                    echo "📋 BUILD SUMMARY 📋"
                    cat test-reports/test-summary.txt
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
                    
                    // Analizza i risultati per determinare lo stato
                    script {
                        def testSummary = readFile('test-reports/test-summary.txt')
                        echo "📊 FINAL TEST SUMMARY:"
                        echo testSummary
                        
                        if (testSummary.contains('FAILED')) {
                            currentBuild.result = 'UNSTABLE'
                            echo "⚠️ Some tests failed - marking build as UNSTABLE"
                        }
                    }
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
