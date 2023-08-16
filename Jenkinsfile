pipeline {
    agent any

    environment {
        FULL_REPO_NAME = 'yoni101087/counterservice'
        DOCKERHUB_USER = FULL_REPO_NAME.tokenize('/').first()
        APP_NAME = FULL_REPO_NAME.tokenize('/').last()
        GIT_COMMIT_HASH = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
    }

    parameters {
        string(name: 'BRANCH_NAME', description: 'Branch name to deploy', defaultValue: 'master')
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: "${params.BRANCH_NAME}"]], userRemoteConfigs: [[url: "https://github.com/${env.FULL_REPO_NAME}.git"]]])
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    sh "docker build -t ${env.APP_NAME}:${env.GIT_COMMIT_HASH} ."
                }
            }
        }

        stage('Promote to Production') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: '4e62cb84-b955-487a-a818-34ed3b912710', 
                        passwordVariable: 'DOCKER_PASS', 
                        usernameVariable: 'DOCKER_USER')]) {
                        sh """
                            docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
                        """
                    }
                    sh "docker tag ${env.APP_NAME}:${env.GIT_COMMIT_HASH} ${env.DOCKERHUB_USER}/${env.APP_NAME}:${env.GIT_COMMIT_HASH}"
                    sh "docker push ${env.DOCKERHUB_USER}/${env.APP_NAME}:${env.GIT_COMMIT_HASH}"
                }
            }
        }

        stage('Deploy To Production') {
            when {
                expression { env.BRANCH_NAME == 'master' }
            }
            steps {
                script {
                    try {
                        //Try to deploy new version to production
                        sh """
                            docker service update --image ${env.APP_NAME} ${env.APP_NAME}:${env.GIT_COMMIT_HASH}
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
            post {
                failure {
                    sh """
                    echo "Deployment to production failed!"
                    docker service update --rollback ${env.APP_NAME}
                    """

                }
            }
        }
        stage('Tag as stable') {
            steps {
                script {

                        sh """
                            docker tag ${env.APP_NAME}:${env.GIT_COMMIT_HASH} ${env.APP_NAME}:stable
                            docker tag ${env.APP_NAME}:${env.GIT_COMMIT_HASH} ${env.DOCKERHUB_USER}/${env.APP_NAME}:${env.GIT_COMMIT_HASH}
                            docker push ${env.DOCKERHUB_USER}/${env.APP_NAME}:${env.GIT_COMMIT_HASH}-stable
                        """
                    }

                }
            }
        }



    }
}
