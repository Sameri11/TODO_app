pipeline {
    agent { docker { image 'docker:dind' } }
    stages {
        stage('build') {
            steps {
                sh docker build -t registry.gitlab.com/sameri11/todo_app .
                sh docker push registry.gitlab.com/sameri11/todo_app
            }
        }
    }
}