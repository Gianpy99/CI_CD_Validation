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
                echo 'Running tests with coverage...'
                sh '''
                    # Run unittest tests with coverage
                    python3 -m coverage run -m unittest test_app.py
                    
                    # Run pytest tests for additional coverage
                    python3 -m pytest test_app_pytest.py -v \
                        --cov=app \
                        --cov-append \
                        --cov-report=xml:coverage.xml \
                        --cov-report=html:htmlcov \
                        --junitxml=test-results.xml || true
                        
                    # Generate final coverage report
                    python3 -m coverage report
                    python3 -m coverage html
                '''
            }
            post {
                always {
                    // Pubblica i risultati dei test
                    junit 'test-results.xml'
                    
                    // Archivia i report di coverage
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                    
                    // Archivia gli artefatti
                    archiveArtifacts artifacts: 'coverage.xml,test-results.xml', allowEmptyArchive: true
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
            echo 'Pipeline completed!'
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded! '
            // Qui potresti aggiungere notifiche (email, Slack, etc.)
        }
        failure {
            echo 'Pipeline failed! '
            // Qui potresti aggiungere notifiche di errore
        }
        unstable {
            echo 'Pipeline unstable! '
        }
    }
}
