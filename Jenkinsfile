def slackMessages = []

pipeline {
    agent { label "master" }
    stages {
        stage("Build container") {
            agent { label "docker" }
            steps {
                script {
                    sh "docker build -t localhost:5000/yeastizzy:latest ."
                    slackMessages += "New container image localhost:5000/yeastizzy:latest"
                }
            }
        }
        stage("Deploy container") {
            agent { label "docker" }
            steps {
                script {
                    sh "docker save localhost:5000/yeastizzy:latest | bzip2 | ssh oracle 'bunzip2 | docker load'"
                    slackMessages += "Container deployed to Oracle virtual machine"
                }
            }
        }
    }
    post {
        success { cleanWs() }
        always {
            sendSlackNotifications (
                buildStatus: currentBuild.result,
                threadMessages: slackMessages
            )
        }
    }
}
