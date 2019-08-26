pipeline {
    agent any

    stages {
        stage('Download code from GitHub') {
            steps {
                echo "Downloading code from https://github.com/maccioni/forward-cicd-ansible"
            }
        }
        stage('Pre-change validation') {
            steps {
                sh "echo 'Checking if the policy is already in place. If it is, exit successfully.'"
                echo "Pre-change validation result: ${currentBuild.result}"
                echo "Pre-change validation currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Simulate change in Sandbox') {
            steps {
                sh "echo 'Placeholder for policy simulation on Forward Sandbox'"
            }
        }
        stage('Apply network change') {
            steps {
                sh "ansible-playbook ansible-test.yml -vvvv"
            }
        }
        stage('Post-change validation') {
            steps {
                script {
                    try {
                        sh "echo 'Placeholder for Post-change validation'"
                    } catch (error) {
                        error("Changes failed testing.  Rolled back.")
                    }
                }
            }
        }
    }
}
