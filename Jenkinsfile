pipeline {
    agent any

    environment {
        registryCredential = 'ecr:eu-west-1:awscreds'
        appRegistry = "677276091734.dkr.ecr.eu-west-1.amazonaws.com/lamp-stack-frontend"
        frontendRegistry = "https://677276091734.dkr.ecr.eu-west-1.amazonaws.com"
        cluster = 'frontend-cluster'
        service = 'frontend-cluster-service'
    }

    stages {

        stage('Fetch code') {
            steps {
                git branch: 'main', url: 'https://github.com/BINAH25/microservices-react.git'
            }
        }


        stage('SonarQube analysis') {
            environment {
                scannerHome = tool 'sonar'
            }
            steps {
                withSonarQubeEnv('sonar') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Buid App Image') {
            steps {
                script {
                    dockerImage = docker.build( appRegistry + ":$BUILD_NUMBER", "./react-crud/")
                }
            }
        }


        stage('Scan Image with Trivy') {
            steps {
                script {
                    sh """
                        trivy image --format table --severity HIGH,CRITICAL ${appRegistry}:$BUILD_NUMBER || exit 1
                    """
                }
            }
        }


        // stage('Upload Image to ECR') {
        //     steps {
        //         script {
        //             docker.withRegistry( frontendRegistry, registryCredential ){
        //                 dockerImage.push("$BUILD_NUMBER")
        //                 dockerImage.push('latest')
        //             }
        //         }
        //     }
        // }

        // stage('Deploy to ecs') {
        //     steps {
        //         withAWS(credentials: 'awscreds', region: 'eu-west-1') {
        //             sh 'aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment'
        //         }
        //     }
        // }
    }
}