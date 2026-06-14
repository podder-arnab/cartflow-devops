pipeline {
    agent any

    environment {
        HOST_IP = '172.31.25.206'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f cartflow-nginx cartflow-frontend cartflow-backend cartflow-redis || true
                    docker network rm cartflow_cartflow-net cartflow-pipeline_cartflow-net || true
                    docker-compose up -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 20
                    curl -f http://${HOST_IP}/api/health || exit 1
                '''
            }
        }
    }

    post {
        success { echo 'Deployed successfully!' }
        failure { echo 'Deployment failed!' }
    }
}
