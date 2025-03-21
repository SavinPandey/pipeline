pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/SavinPandey/pipeline.git'
            }
        }
        stage('Build') {
            steps {
                sh 'npm install'  // Modify for your project
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo Deploying...'
            }
        }
    }
}
