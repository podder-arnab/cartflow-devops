pipeline {
    agent any

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
                    docker-compose down || true
                    docker-compose up -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo 'Running health check...'
                sh '''
                    sleep 15
                    curl -f http://localhost/api/health || exit 1
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
