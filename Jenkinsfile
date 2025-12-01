pipeline {
  agent any

  environment {
    IMAGE_NAME = "dhikshanya06/devsecops-app:${BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          sh """
            echo "Building ${IMAGE_NAME}"
            docker build -t ${IMAGE_NAME} .
          """
        }
      }
    }

    stage('Scan Image (Trivy)') {
      steps {
        script {
          sh '''
            echo "Scanning image ${IMAGE_NAME} for HIGH/CRITICAL vulnerabilities..."
            trivy image --exit-code 1 --severity HIGH,CRITICAL ${IMAGE_NAME}
          '''
        }
      }
    }

    stage('Login to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKERHUB_USR', passwordVariable: 'DOCKERHUB_PSW')]) {
          sh '''
            echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin
          '''
        }
      }
    }

    stage('Push Image to Docker Hub') {
      steps {
        script {
          sh """
            echo "Pushing ${IMAGE_NAME} to Docker Hub"
            docker push ${IMAGE_NAME}
          """
        }
      }
    }

    stage('Cleanup') {
      steps {
        script {
          sh """
            docker rmi ${IMAGE_NAME} || true
          """
        }
      }
    }
  }

  post {
    always {
      echo "Pipeline finished. Build: ${BUILD_NUMBER}"
    }
    success {
      echo "Success: image ${IMAGE_NAME} built and pushed"
    }
    failure {
      echo "Failure: check the console log and Trivy report"
    }
  }
}
