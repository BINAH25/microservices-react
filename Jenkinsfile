def COLOR_MAP = [
    'SUCCESS': 'good', 
    'FAILURE': 'danger',
]
pipeline {
    agent any

    environment {
        ECR_REGISTRY = credentials('ecr-registry')
        ECR_REPOSITORY = credentials('ecr-repository')
        AWS_REGION = credentials('aws-region')
        
        registryCredential = "ecr:${AWS_REGION}:awscreds"
        appRegistry = "${ECR_REGISTRY}/${ECR_REPOSITORY}"
        frontendRegistry = "https://${ECR_REGISTRY}"
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


        stage('Upload Image to ECR') {
            steps {
                script {
                    docker.withRegistry( frontendRegistry, registryCredential ){
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
            }
        }

        // stage('Deploy to ecs') {
        //     steps {
        //         withAWS(credentials: 'awscreds', region: 'eu-west-1') {
        //             sh 'aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment'
        //         }
        //     }
        // }
    }

    post {
        always {
            echo 'Slack Notifications.'
            slackSend channel: '#micro-service-pipeline',
                color: COLOR_MAP[currentBuild.currentResult],
                message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
        }
    }
}