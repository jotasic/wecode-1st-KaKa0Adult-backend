pipeline {
    agent {
        docker {
            image 'python:3.8.3' 
            args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker'
        }
    }
    stages {
//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                          1. Django Test Stage                           //
//                                                                          //
//  현재 사용하는 docker 컨테이너는 python 기반의 컨테이너 이므로           //
//  test는 DB를 사용안 하고 하는데, 이 부분을 python과 mysql이 설치된       //
//  image로 변경해서 배포 환경과 동일한 환경으로 test할 수 있도록 수정해야됨//
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
        stage('1.Test') {
            steps {
                slackSend channel: 'jenkins', color: '#0064f0', message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
                withCredentials([string(credentialsId: "KAKAO_PET_SHOP_DJANGO_SECRECT_KEY", variable: "DJANGO_SECRECT_KEY"), string(credentialsId: "KAKAO_PET_SHOP_ALGORITHM", variable: "DJANGO_ALGORITHM")]) {
                        
//////////////////////////////////////////////////////////////////////////////
//  Setup Test environment                                                  //
//////////////////////////////////////////////////////////////////////////////
                    sh 'apt-get -y update'
                    sh 'apt-get -y install gcc build-essential zlib1g-dev make'
                    sh 'pip install -r requirements.txt'

//////////////////////////////////////////////////////////////////////////////
//  Unit Test                                                               //
//////////////////////////////////////////////////////////////////////////////
                    sh 'python manage.py test --settings=kaka0Adult.settings.jenkins'
                }
            }
        }

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                           2. dev branch 배포                             //
//                                                                          //
//  현재 구축되어 있지 않음                                                 //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
        stage('2.Staging Deploy') {
            when {
                branch 'dev'
            }
            steps {
                sh 'echo dev Not yet...'
            }
        }

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                           3. main branch 배포                            //
//                                                                          //
//  만약 github로 push된 브렌치가 main일 시 동작하는 stage                  //
//  1. Docker 이미지 만들고, Docker hub에 push                              //
//  2. ssh를 이용해서 EC2 서버에 배포                                       //
//    - 컨테이너 종료                                                       //
//    - docker image 삭제                                                   //
//    - docker run (image가 없으므로 docker hub에서 다운로드 받는다)        //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
        stage('3.Prod Deploy') {
            // when {
            //     branch 'main'
            // }
            steps{
                withCredentials([string(credentialsId: "KAKAO_PET_SHOP_SQL_HOST", variable: "SQL_HOST"), string(credentialsId: "KAKAO_PET_SHOP_SQL_PASSWORD", variable: "SQL_PASSWORD"), usernamePassword(credentialsId: 'DOCKER_ACCOUNT', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD'), string(credentialsId: "KAKAO_PET_SHOP_DJANGO_SECRECT_KEY", variable: "DJANGO_SECRECT_KEY"), string(credentialsId: "KAKAO_PET_SHOP_ALGORITHM", variable: "DJANGO_ALGORITHM")]){

//////////////////////////////////////////////////////////////////////////////
// Make Docker image                                                        //
//////////////////////////////////////////////////////////////////////////////
                    sh 'docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"'
                    sh 'docker build --build-arg ARG_DJANGO_ALGORITHM="$DJANGO_ALGORITHM" --build-arg ARG_DJANGO_SECRECT_KEY="$DJANGO_SECRECT_KEY" --build-arg ARG_SQL_HOST="$SQL_HOST" --build-arg ARG_SQL_PASSWORD="$SQL_PASSWORD" --no-cache -t "$DOCKER_USERNAME"/kakao-pet-shop-prod:"$BUILD_NUMBER" -f Dockerfile-prod .'
                    sh 'docker push "$DOCKER_USERNAME"/kakao-pet-shop-prod:"$BUILD_NUMBER"'

//////////////////////////////////////////////////////////////////////////////
//  Deploy Docker image to EC2 servers                                      //
//////////////////////////////////////////////////////////////////////////////
                    script {
                        def remote = [:] 
                        remote.allowAnyHosts = true

                        withCredentials([sshUserPrivateKey(credentialsId: "BACKEND_SERVER_SSH_IDENTITY", keyFileVariable: "identity", usernameVariable: "userName"), string(credentialsId: "BACKEND_SERVER_IPS", variable: "SERVER_IPS")]) {

                            remote.name = userName
                            remote.user = userName 
                            remote.identityFile = identity
                            def ips = SERVER_IPS.split(',')
                            def cmd = 'docker run -d --rm -p 8000:8000 --name kakao_pet_shop -v log:/usr/src/app/log ' + DOCKER_USERNAME +'/kakao-pet-shop-prod:' + BUILD_NUMBER
                            
                            ips.each { ip ->
                                remote.host = ip 
                                sshCommand remote: remote, command: 'CONTAINERS=$(docker ps -a -q) ; if [ -n \"$CONTAINERS\" ]; then docker stop  $CONTAINERS ; fi'
                                sshCommand remote: remote, command: 'docker rmi $(docker images -aq)'
                                sshCommand remote: remote, command: cmd
                            }
                        }
                    }
                }
            }
        }
    }

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                                  Post                                    //
//                                                                          //
//  모든 setp이 완료가 되면, 성공 및 실패 여부를 Slack에 보낸다.            //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
    post {
        success { 
            slackSend channel: 'jenkins', color:'#00c800', message: "SUCCESS: JOB '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
        }
        failure {
            slackSend channel: 'jenkins', color:'#dc0000', message: "FAILED: JOB '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
        }
    }
}