FROM jenkins/jenkins:lts
LABEL MAINTAINER sergi.torrellas@soprasteria.com

# Install python3
USER root
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install docker

# Install docker
RUN apt install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN apt update
RUN apt install -y docker-ce

# Add src docker
ADD ./src/ /repo/