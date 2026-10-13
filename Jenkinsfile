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
                        bat '"C:\\Users\\Kaavya S\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" build -t hospital-appointment-system:1.0 .'
                    }
                }
            }
        }

        stage('Check WSL and Ansible Access') {
            when {
                not { isUnix() }
            }
            steps {
                bat '"C:\\Windows\\System32\\wsl.exe" -d Ubuntu -u kaavya -- bash -lc "ansible-playbook --version"'
            }
        }

        stage('Deploy with Ansible') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'ansible-playbook ansible/deploy.yml'
                    } else {
                        bat '"C:\\Windows\\System32\\wsl.exe" -d Ubuntu -u kaavya -- bash -lc "ansible-playbook /home/kaavya/hospital-appointment-system/ansible/deploy.yml"'
                    }
                }
            }
        }

        stage('Verify Application Health') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'curl --fail http://localhost:5000/health'
                    } else {
                        bat 'curl.exe --fail http://localhost:5000/health'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed, Docker image built, Ansible deployment completed, and health check passed.'
        }
        failure {
            echo 'FAILURE: Check the Jenkins console output to identify the failed stage.'
        }
    }
}
