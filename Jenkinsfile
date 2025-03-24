pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('DOCKER_CREDENTIALS')
        GITHUB_CREDENTIALS = credentials('GITHUB_CREDENTIALS')
        REPO_NAME = 'savinpandey/cicd-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'GITHUB_CREDENTIALS', url: 'https://github.com/SavinPandey/pipeline.git', branch: 'main'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                sh "echo ${DOCKER_CREDENTIALS} | docker login -u '${DOCKER_CREDENTIALS_USR}' --password-stdin"
            }
        }

        stage('Get latest image tag') {
            steps {
                script {
                    def latestTag = sh(
                        script: "curl -s 'https://hub.docker.com/v2/repositories/${REPO_NAME}/tags/' | jq -r '.results[].name' | grep -E '^v[0-9]+$' | sort -V | tail -n1",
                        returnStdout: true
                    ).trim()

                    if (!latestTag || latestTag == "null") {
                        env.NEW_TAG = "v1"
                    } else {
                        def tagNum = latestTag.replaceAll('v', '').toInteger() + 1
                        env.NEW_TAG = "v${tagNum}"
                    }
                    echo "✅ New Docker tag: ${env.NEW_TAG}"
                }
            }
        }

        stage('Build and tag Docker image') {
            steps {
                sh "docker build -t ${REPO_NAME}:${NEW_TAG} ."
            }
        }

        stage('Push Docker image') {
            steps {
                sh "docker push ${REPO_NAME}:${NEW_TAG}"
            }
        }

        stage('Update Kubernetes Deployment') {
            steps {
                sh """
                sed -i 's|image: .*|image: ${REPO_NAME}:${NEW_TAG}|g' deployment/deployment.yaml
                cat deployment/deployment.yaml
                """
            }
        }

        stage('Commit and Push Updated Deployment') {
            steps {
                withCredentials([string(credentialsId: 'GITHUB_CREDENTIALS', variable: 'TOKEN')]) {
                    sh """
                    git config --global user.email "github-actions@github.com"
                    git config --global user.name "GitHub Actions"
                    git remote set-url origin https://x-access-token:$TOKEN@github.com/SavinPandey/pipeline.git
                    git add deployment/deployment.yaml
                    git commit -m "Update deployment image to ${NEW_TAG}"
                    git pull origin main --rebase
                    git push origin main
                    """
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline executed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for errors.'
        }
    }
}
