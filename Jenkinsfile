pipeline {
    agent any

    stages {
        stage('Gather user inputs') {
            steps {
                echo "Downloaded code from https://github.com/maccioni/forward-cicd-ansible"
                timeout(time: 120, unit: 'SECONDS') {
                    script {
                        env.SERVICE_NAME = input message: 'Provide Service Name', ok: 'Enter',
                            parameters: [string(defaultValue: '', description: 'Service Name', name: 'name')]
                        env.SERVICE_IP = input message: 'Provide Service IP', ok: 'Enter!',
                            parameters: [ string(defaultValue: '', description: 'Service IP', name: 'ip') ]
                        env.SERVICE_PORT = input message: 'Provide Service port', ok: 'Enter!',
                            parameters: [ string(defaultValue: '', description: 'Service port', name: 'port') ]
                        env.CLIENTS = input message: 'Provide Users Network', ok: 'Enter!',
                            parameters: [ string(defaultValue: '', description: 'Users Network', name: 'clients') ]
                    }
                    // Save user inputs to files in the tmp directory to be used at later stages
                    sh "ansible-playbook save_inputs.yml -vvvvv"
                    echo "Service name: ${env.SERVICE_NAME} Service IP: ${env.SERVICE_IP} Service port: ${env.SERVICE_PORT} Clients Network: ${env.CLIENTS}"
                    slackSend (message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.JENKINS_URL}/blue/organizations/jenkins/forward-cicd-ansible/detail/master/${env.BUILD_NUMBER})",  username: 'fabriziomaccioni', token: "${env.SLACK_TOKEN}", teamDomain: 'nfd-fwd', channel: 'cicd-service-deployment')
                }
            }
        }
        stage('Check if change is needed') {
            steps {
                sh 'env'
                echo "Get Path info using Ansible URI module"
                sh "ansible-playbook get_path.yml -vvvvv"
                echo "Check if routing and policies are already in place for the given path"
                sh "ansible-playbook is_change_needed.yml -vvvvv"
            }
        }
        stage('Verify change in Sandbox') {
            steps {
                echo "Build new FW config with the new service security rule"
                sh "ansible-playbook sandbox_config_build.yml -vvvvv"
                echo "Change security policy in the Forward Sandbox"
                sh "ansible-playbook sandbox_save_changes.yml -vvvvv"
                echo "Create a new Intent Check for the new service"
                // Copy and run the playbook from fwd-ansible directory to use
                // the new Forward Ansible modules
                sh "cp intent_check_new_service.yml /var/lib/jenkins/fwd-ansible"
                //sh "ansible-playbook /var/lib/jenkins/fwd-ansible/intent_check_new_service.yml -vvvvv"
                echo "Get all Checks from Forward Platform using Ansible URI module"
                sh "ansible-playbook get_checks.yml -vvvvv"
                script {
                    try {
                        echo "Verify all Checks"
                        sh "python verify_checks.py"
                    } catch (error) {
                        echo("Some Checks are failing.  Failing the pipeline and exiting.")
                    }
                }
            }
        }
        stage('Apply network change to production') {
            steps {
            echo "Copy files and run playbook in the jump host server to deploy changes to production "
            sh "scp /etc/ansible/hosts ansible.cfg ./tmp/* deploy_changes.yml rollback_changes.yml /var/lib/jenkins/forward.properties root@10.128.2.244:"
            sh "ssh root@10.128.2.244 'ansible-playbook deploy_changes.yml -vvvvv'"
            }
        }
        stage('Verify new connectivity and check for regressions') {
            steps {
                echo "Collect from modified devices only and make sure collection and processing are over"
                sh "cp partial_collection_take.yml ./tmp/firewall_name /var/lib/jenkins/fwd-ansible"
                sh "ansible-playbook /var/lib/jenkins/fwd-ansible/take_partial_collection.yml -vvvvv"
                echo "Get all Checks using Ansible URI module"
                sh "ansible-playbook get_checks.yml -vvvvv"
                script {
                    try {
                        echo "Verify all Checks"
                        sh "python verify_checks.py"
                    } catch (error) {
                        echo("Some Checks are failing.  Rolling back configuration.")
                        sh "ssh root@10.128.2.244 'ansible-playbook rollback_changes.yml -vvvvv'"
                    }
                }
            }
        }
    }
    post {
        always {
            echo "(Post always) currentBuild.currentResult: ${currentBuild.currentResult}"
            echo "(Post always) currentBuild.Result: ${currentBuild.result}"
        }
        success {
            echo "(Post success) Pipeline executed successfully!"
            slackSend (message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.JENKINS_URL}/blue/organizations/jenkins/forward-cicd-ansible/detail/master/${env.BUILD_NUMBER})", color: '#00FF00', username: 'fabriziomaccioni', teamDomain: 'nfd-fwd', channel: 'cicd-service-deployment')
        }
        unstable {
            echo "(Post unstable) Pipeline is unstable :/"
        }
        failure {
            echo "(Post failure) Pipeline Failed!!!"
            slackSend (message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.JENKINS_URL}/blue/organizations/jenkins/forward-cicd-ansible/detail/master/${env.BUILD_NUMBER})", color: '#FF0000', username: 'fabriziomaccioni', teamDomain: 'nfd-fwd', channel: 'cicd-service-deployment')
        }
        changed {
            echo "(Post failure) Something changed..."
        }
    }
}
