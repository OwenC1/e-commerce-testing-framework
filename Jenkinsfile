pipeline {
    agent any

    environment {
        BRANCH_NAME = "${env.GIT_BRANCH.contains('/') ? env.GIT_BRANCH.split('/')[1] : env.GIT_BRANCH}"
        AWS_DEFAULT_REGION = 'eu-north-1'  // Change this to your region
        ECR_REPO = '880757820656.dkr.ecr.eu-north-1.amazonaws.com/ecommerce-tests' // Replace with your actual ECR URI
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (BRANCH_NAME == 'main') {
                        echo "Running all tests for main branch"
                        sh '''
                            source venv/bin/activate
                            pytest tests/ api_tests/ -v
                        '''
                    } else if (BRANCH_NAME.startsWith('feature/ui-')) {
                        echo "Running UI tests for ${BRANCH_NAME}"
                        sh '''
                            source venv/bin/activate
                            pytest tests/ui_tests/ -v
                        '''
                    } else if (BRANCH_NAME.startsWith('feature/api-')) {
                        echo "Running API tests for ${BRANCH_NAME}"
                        sh '''
                            source venv/bin/activate
                            pytest api_tests/ -v
                        '''
                    } else {
                        echo "Running basic tests for ${BRANCH_NAME}"
                        sh '''
                            source venv/bin/activate
                            pytest
                        '''
                    }
                }
            }
        }

        stage('Generate Reports') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest tests/ api_tests/ --html=reports/report.html -v
                '''
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
            }
        }

        stage('Docker Build & Push to ECR') {
            when {
                branch 'main'  // Only push to ECR on main branch
            }
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-ecr-creds']]) {
                    sh '''
                        aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REPO
                        docker build -t $ECR_REPO:$IMAGE_TAG .
                        docker push $ECR_REPO:$IMAGE_TAG
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "All tests passed and Docker image pushed to ECR!"
        }
        failure {
            echo "Something went wrong. Check the logs and test report."
        }
    }
}
