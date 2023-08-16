pipeline {
    agent any

    environment {
        FULL_REPO_NAME = 'yoni101087/counterservice' // Set your full repository name here
        DOCKERHUB_USER = FULL_REPO_NAME.tokenize('/').first()
        APP_NAME = FULL_REPO_NAME.tokenize('/').last()
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
                    // Checkout the code from the specified branch
                    checkout([$class: 'GitSCM', branches: [[name: "${params.BRANCH_NAME}"]], userRemoteConfigs: [[url: "https://github.com/${env.FULL_REPO_NAME}.git"]]])
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    // Get the Git commit hash
                    def gitCommitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    // Set the gitCommitHash as an environment variable to make it available in other stages
                    env.GIT_COMMIT_HASH = gitCommitHash
                    // Build the Docker image
                    sh "docker build -t ${env.APP_NAME}:${gitCommitHash} ."
                }
            }
        } // Build
        
        stage('Promote to Production') {
            steps {
                script {
                    // Log in to DockerHub
                    withCredentials([usernamePassword(
                        credentialsId: '4e62cb84-b955-487a-a818-34ed3b912710', 
                        passwordVariable: 'DOCKER_PASS', 
                        usernameVariable: 'DOCKER_USER')]) {
                        sh """
                            docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
                        """
                    }
                    // Tag the Docker image as "stable"
                    sh "docker tag ${env.APP_NAME}:${gitCommitHash} ${env.DOCKERHUB_USER}/${env.APP_NAME}:${gitCommitHash}"
            
                    // Push the "stable" tagged image to DockerHub
                    sh "docker push ${env.DOCKERHUB_USER}/${env.APP_NAME}:${gitCommitHash}"
                }
            }
        } //Promote to Production

        
        stage('Deploy To Production') {
            when {
                expression { env.BRANCH_NAME == 'master' }
                 }
            steps {
                script {
                    // Run the Docker container in the production environment
                    
                    sh """
                        docker rm -f ${env.APP_NAME}
                        docker run -d -p 80:80 --name ${env.APP_NAME} --restart always ${env.APP_NAME}:${gitCommitHash}
                        sh "docker tag ${env.APP_NAME}:${gitCommitHash} ${env.DOCKERHUB_USER}/${env.APP_NAME}:stable"
                        
                    """
                }
            }
        } //Deploy To Production
        
    }
}
