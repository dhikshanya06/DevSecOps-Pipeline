pipeline {
  agent any

  environment {
    IMAGE_NAME = "dhikshanya06/devsecops-app:${BUILD_NUMBER}"
    TARGET_HOST = "3.226.247.216"
    TARGET_USER = "ec2-user"
    SSH_CRED_ID = "ec2-deployer"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build Docker Image') {
      steps {
        script {
          sh '''
            echo "Building ${IMAGE_NAME}"
            docker build -t ${IMAGE_NAME} .
          '''
        }
      }
    }

    stage('Scan Image (Trivy)') {
      steps {
        script {
          sh '''
            echo "Scanning image ${IMAGE_NAME} for HIGH/CRITICAL vulnerabilities..."
            trivy image --severity HIGH,CRITICAL ${IMAGE_NAME} || true
          '''
        }
      }
    }

    stage('Login to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKERHUB_USR', passwordVariable: 'DOCKERHUB_PSW')]) {
          sh '''echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin'''
        }
      }
    }

    stage('Push Image to Docker Hub') {
      steps {
        script {
          sh '''
            echo "Pushing ${IMAGE_NAME} to Docker Hub"
            docker push ${IMAGE_NAME}
          '''
        }
      }
    }

    stage('Deploy to EC2') {
      steps {
        script {
          // try sshagent first. if plugin missing, fallback will be used in second block
          try {
            sshagent (credentials: [env.SSH_CRED_ID]) {
              sh """
                echo "Deploying ${IMAGE_NAME} to ${TARGET_HOST}"
                ssh -o StrictHostKeyChecking=no ${TARGET_USER}@${TARGET_HOST} \\
                  'set -e
                   docker pull ${IMAGE_NAME} || sudo docker pull ${IMAGE_NAME}
                   docker stop devsecops-app || true
                   docker rm devsecops-app || true
                   docker run -d --name devsecops-app -p 80:80 ${IMAGE_NAME} || sudo docker run -d --name devsecops-app -p 80:80 ${IMAGE_NAME}
                  '
              """
            }
          } catch (err) {
            // fallback: use ssh key stored in credentials as temporary file
            withCredentials([sshUserPrivateKey(credentialsId: env.SSH_CRED_ID, keyFileVariable: 'KEYFILE', usernameVariable: 'SSHUSER')]) {
              sh '''
                chmod 600 "$KEYFILE"
                echo "Fallback deploy using key file $KEYFILE"
                ssh -o StrictHostKeyChecking=no -i "$KEYFILE" ${SSHUSER}@${TARGET_HOST} 'set -e
                  docker pull '${IMAGE_NAME}' || sudo docker pull '${IMAGE_NAME}'
                  docker stop devsecops-app || true
                  docker rm devsecops-app || true
                  docker run -d --name devsecops-app -p 80:80 '${IMAGE_NAME}' || sudo docker run -d --name devsecops-app -p 80:80 '${IMAGE_NAME}'
                '
              '''
            }
          }
        }
      }
    }

    stage('Cleanup') {
      steps {
        script { sh 'docker rmi ${IMAGE_NAME} || true' }
      }
    }
  }

  post {
    always { echo "Pipeline finished. Build: ${BUILD_NUMBER}" }
    success { echo "Success: image ${IMAGE_NAME} built and pushed and deployed" }
    failure { echo "Failure: check Jenkins console and Trivy report" }
  }
}
