pipeline {
    agent {
        docker {
            alwaysPull true
            image "burnkim61/jenkins-django-build"
            args "-u root:root -v /var/run/docker.sock:/var/run/docker.sock"

        }
    }
    stages {
        
//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                          1. Django Test Stage                            //
//                                                                          //
//  현재 사용하는 docker 컨테이너는 python 기반의 컨테이너 이므로           //
//  test는 DB를 사용안 하고 하는데, 이 부분을 python과 mysql이 설치된       //
//  image로 변경해서 배포 환경과 동일한 환경으로 test할 수 있도록 수정해야됨//
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
        stage('1.Environment Setup') {
            steps {
                slackSend (channel: 'jenkins', color: '#0064f0', message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
                sh 'pip install -r requirements.txt'
            }
        }

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                          2. Django Test Stage                            //
//                                                                          //
//  현재 사용하는 docker 컨테이너는 python 기반의 컨테이너 이므로           //
//  test는 DB를 사용안 하고 하는데, 이 부분을 python과 mysql이 설치된       //
//  image로 변경해서 배포 환경과 동일한 환경으로 test할 수 있도록 수정해야됨//
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
        stage('2.Test') {
            steps {
                withCredentials([ \
                    string(credentialsId: "KAKAO_PET_SHOP_DJANGO_SECRECT_KEY", variable: "DJANGO_SECRECT_KEY"), \
                    string(credentialsId: "KAKAO_PET_SHOP_ALGORITHM", variable: "DJANGO_ALGORITHM") \
                    ]) {
                        sh """
		                    sudo service mysql start
		                    sudo mysql -uroot -e "UPDATE mysql.user SET authentication_string=PASSWORD('password') WHERE User='root'; FLUSH PRIVILEGES;"
                            python3.8 manage.py test --settings=kaka0Adult.settings.jenkins
                        """
                }
            }
        }

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                           3. dev branch 배포                             //
//                                                                          //
//  현재 구축되어 있지 않음                                                 //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
        stage('3.Staging Deploy') {
            when {
                branch 'dev'
            }
            steps {
                sh 'echo dev Not yet...'
            }
        }

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                           4. main branch 배포                            //
//                                                                          //
//  만약 github로 push된 브렌치가 main일 시 동작하는 stage                  //
//  1. Docker 이미지 만들고, Docker hub에 push                              //
//  2. ssh를 이용해서 EC2 서버에 배포                                       //
//    - 컨테이너 종료                                                       //
//    - docker image 삭제                                                   //
//    - docker run (image가 없으므로 docker hub에서 다운로드 받는다)        //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////

        stage('4.Prod Deploy') {
            // when {
            //     branch 'main'
            // }
            steps{
                withCredentials([ \
                    string(credentialsId: "KAKAO_PET_SHOP_SQL_HOST", variable: "SQL_HOST"), \
                    string(credentialsId: "KAKAO_PET_SHOP_SQL_PASSWORD", variable: "SQL_PASSWORD"), \
                    string(credentialsId: "KAKAO_PET_SHOP_DJANGO_SECRECT_KEY", variable: "DJANGO_SECRECT_KEY"),  \
                    string(credentialsId: "KAKAO_PET_SHOP_ALGORITHM", variable: "DJANGO_ALGORITHM"), \
                    string(credentialsId: "AWS_CLI_ACCESS_KEY", variable: "AWS_CLI_ACCESS_KEY"), \
                    string(credentialsId: "AWS_CLI_SECRET_ACCESS_KEY", variable: "AWS_CLI_SECRET_ACCESS_KEY"), \
                    usernamePassword(credentialsId: 'DOCKER_ACCOUNT', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD') \
                ]){

//////////////////////////////////////////////////////////////////////////////
// Make Docker image                                                        //
//////////////////////////////////////////////////////////////////////////////
                    sh """
                        sudo service docker start 
                        
                        docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"

                        docker build --no-cache \
                        --build-arg ARG_DJANGO_ALGORITHM="$DJANGO_ALGORITHM"  \
                        --build-arg ARG_DJANGO_SECRECT_KEY="$DJANGO_SECRECT_KEY" \
                        --build-arg ARG_SQL_HOST="$SQL_HOST" \
                        --build-arg ARG_SQL_PASSWORD="$SQL_PASSWORD" \
                        -t "$DOCKER_USERNAME"/kakao-pet-shop-prod:"${env.BUILD_NUMBER}" \
                        -f ./Dockerfile/Dockerfile-prod .

                        docker push "$DOCKER_USERNAME"/kakao-pet-shop-prod:"${env.BUILD_NUMBER}"
                    """

//////////////////////////////////////////////////////////////////////////////
//  Deploy Docker image to EC2 servers                                      //
//////////////////////////////////////////////////////////////////////////////
                    sh """
                        aws configure set region us-east-2
                        aws configure set aws_access_key_id $AWS_CLI_ACCESS_KEY
                        aws configure set aws_secret_access_key $AWS_CLI_SECRET_ACCESS_KEY
                    """

                    sh """
                        aws ec2 describe-instances \
                        --filters "Name=tag-value,Values=backend-server*"  \
                        --query 'Reservations[*].Instances[*].[PrivateIpAddress]' \
                        --output text > ips.txt

                        echo "Private IP Address:\n"
                        cat ips.txt
                    """

                    sh """
                        cat ips.txt | while read ip
                        do
                            echo ">>> Start Deployment Server: \$ip" 
                            ssh -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostkeyChecking=no backend-server@\$ip /bin/bash -s<<-'EOF'
                            (docker ps -a -q) ; if [ -n \$CONTAINERS ]; then docker stop  \$CONTAINERS ; fi
                            docker rmi \$(docker images -aq)
                            docker run -d --restart=unless-stopped --rm -p 8000:8000 --name=kakao_pet_shop -v log:/usr/src/app/log $DOCKER_USERNAME/kakao-pet-shop-prod:${env.BUILD_NUMBER}
                            echo ">>> Done Deployment Server: \$ip"
                        EOF
                        done

                    """
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
            slackSend (channel: 'jenkins', color:'#00c800', message: "SUCCESS: JOB '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
        failure {
            slackSend (channel: 'jenkins', color:'#dc0000', message: "FAILED: JOB '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
    }
}
