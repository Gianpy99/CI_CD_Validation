pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/Gianpy99/CI_CD_Validation.git'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 -m unittest test_app.py'
            }
        }
    }
}
