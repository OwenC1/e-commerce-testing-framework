pipeline {
    agent any
    
    environment {
        // Get branch name to decide which tests to run
        BRANCH_NAME = "${env.GIT_BRANCH.contains('/') ? env.GIT_BRANCH.split('/')[1] : env.GIT_BRANCH}"
    }
    
    stages {
        stage('Setup') {
            steps {
                // First we set up our testing environment
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
                    // Choose which tests to run based on the branch
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
                // Create test reports
                sh '''
                    source venv/bin/activate
                    pytest tests/ api_tests/ --html=reports/report.html -v
                '''
                
                // Publish HTML reports
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
            echo "Some tests failed, check the report for details."
        }
    }
}