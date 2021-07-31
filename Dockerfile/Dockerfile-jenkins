FROM ubuntu:18.04

## Install sudo
RUN apt update && apt install sudo -y

WORKDIR /jenkins

## Install mysql
RUN sudo apt install mysql-server -y

## Setting Up Database
RUN echo " \n\
[client] \n\
default-character-set=utf8mb4 \n\
\n\
[mysql] \n\
default-character-set=utf8mb4 \n\
\n\
[mysqld] \n\
init_connect='SET collation_connection = utf8_unicode_ci' \n\
init_connect='SET NAMES utf8mb4' \n\
character-set-server=utf8mb4 \n\
skip-character-set-client-handshake \n\
bind-address = 0.0.0.0 " | sudo tee -a /etc/mysql/my.cnf

## Install Python
RUN sudo apt update -y \
    && sudo apt install python3.8 -y \
    && sudo apt install python3-pip -y \
    && sudo apt install libmysqlclient-dev libmysqld-dev build-essential python3.8-dev -y \
    && python3.8 -mpip install --upgrade pip

## Install Docker
RUN sudo apt install -y curl
RUN curl -fsSL https://get.docker.com -o get-docker.sh
RUN sudo sh get-docker.sh

## Install AWS cli
RUN sudo apt install -y curl unzip
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN sudo ./aws/install

CMD ["/bin/bash", "-c"]
