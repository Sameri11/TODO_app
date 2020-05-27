pipeline {
    agent any
    environment {
        DOCKER_CREDS = credentials('85eb3814-ba67-4244-9b50-fd4f4caab947')
        DOCKER_REGISTRY = 'registry.gitlab.com'
        DOCKER_REGISTRY_IMG = 'registry.gitlab.com/sameri11/todo_app'
    }
    stages {
        stage('build') {
            steps {
                sh "docker build -t ${DOCKER_REGISTRY_IMG} ."
            }
        }
        stage('push') {
            steps {
                sh "docker login -u ${DOCKER_CREDS_USR} -p ${DOCKER_CREDS_PSW} ${DOCKER_REGISTRY}"
                sh "docker push ${DOCKER_REGISTRY_IMG}"
            }
        }
    }
}