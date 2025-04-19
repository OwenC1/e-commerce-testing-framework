pipeline {
    agent {
        docker {
            image 'ecommerce-tests'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        BRANCH_NAME = "${env.GIT_BRANCH.contains('/') ? env.GIT_BRANCH.split('/')[1] : env.GIT_BRANCH}"
    }

    stages {
        stage('Run Tests') {
            steps {
                script {
                    if (BRANCH_NAME == 'main') {
                        echo "Running all tests for main branch"
                        sh 'pytest tests/ api_tests/ -v'
                    } else if (BRANCH_NAME.startsWith('feature/ui-')) {
                        echo "Running UI tests for ${BRANCH_NAME}"
                        sh 'pytest tests/ui_tests/ -v'
                    } else if (BRANCH_NAME.startsWith('feature/api-')) {
                        echo "Running API tests for ${BRANCH_NAME}"
                        sh 'pytest api_tests/ -v'
                    } else {
                        echo "Running basic tests for ${BRANCH_NAME}"
                        sh 'pytest'
                    }
                }
            }
        }

        stage('Generate Reports') {
            steps {
                sh 'pytest tests/ api_tests/ --html=reports/report.html -v'
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
    }

    post {
        success {
            echo "All tests passed!"
        }
        failure {
            echo "Something went wrong. Check the logs and test report."
        }
    }
}
