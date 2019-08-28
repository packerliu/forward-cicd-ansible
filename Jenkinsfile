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
#                sh "ansible-playbook /var/lib/jenkins/fwd-ansible/test_esx_traffic.yml --extra-vars=@/var/lib/jenkins/fwd-ansible/deployments/test-snapshots-before.yml --extra-vars=expected_check_status=FAIL"
                sh "ansible-playbook pre-change-validation.yml"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Simulate change in Sandbox') {
            steps {
                sh "echo 'Placeholder for policy simulation on Forward Sandbox'"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Apply network change') {
            steps {
                sh "ansible-playbook ansible-test.yml -vvvv"
                echo "currentBuild.currentResult: ${currentBuild.currentResult}"
            }
        }
        stage('Post-change validation') {
            steps {
                script {
                    try {
                        sh "echo 'Placeholder for Post-change validation'"
                        echo "currentBuild.currentResult: ${currentBuild.currentResult}"
                    } catch (error) {
                        error("Changes failed testing.  Rolled back.")
                        echo "currentBuild.currentResult: ${currentBuild.currentResult}"
                    }
                }
            }
        }
    }
}
