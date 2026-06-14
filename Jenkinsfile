pipeline {
    agent any

    environment {
        HOST_IP = '172.31.25.206'
        APP_DIR = '/home/ubuntu/cartflow'
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
                    # copy files from Jenkins workspace to app directory
                    cp -r monitoring ${APP_DIR}/
                    cp docker-compose.yml ${APP_DIR}/
                    cp Jenkinsfile ${APP_DIR}/

                    # remove all containers
                    docker rm -f cartflow-nginx cartflow-frontend cartflow-backend cartflow-redis cartflow-prometheus cartflow-grafana cartflow-node-exporter || true

                    # remove networks
                    docker network rm cartflow_cartflow-net cartflow-pipeline_cartflow-net || true
                    docker network prune -f || true

                    # deploy from app directory
                    cd ${APP_DIR}
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
        success { echo 'CartFlow deployed successfully!' }
        failure { echo 'Deployment failed!' }
    }
}
