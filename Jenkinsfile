pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv .jenkins-venv
                            .jenkins-venv/bin/python -m pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            "C:/Users/Kaavya S/AppData/Local/Programs/Python/Python312/python.exe" -m venv .jenkins-venv
                            .jenkins-venv\\Scripts\\python.exe -m pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Run Automated Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '.jenkins-venv/bin/python -m pytest -v'
                    } else {
                        bat '.jenkins-venv\\Scripts\\python.exe -m pytest -v'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker build -t hospital-appointment-system:1.0 .'
                    } else {
                        bat 'docker build -t hospital-appointment-system:1.0 .'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed and Docker image built.'
        }
        failure {
            echo 'FAILURE: Check the Jenkins console output.'
        }
    }
}
