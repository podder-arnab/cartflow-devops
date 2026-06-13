pipeline {
    agent any

    environment {
        HOST_IP = '172.31.25.206'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Verify Files') {
            steps {
                echo 'Verifying project files...'
                sh 'ls -la'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying CartFlow...'
                sh '''
                    docker-compose down --remove-orphans || true
                    docker network prune -f || true
                    docker-compose up -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo 'Running health check...'
                sh '''
                    sleep 20
                    curl -f http://${HOST_IP}/api/health || exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CartFlow deployed successfully!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}
