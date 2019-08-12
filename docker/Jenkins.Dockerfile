FROM jenkins/jenkins:lts
LABEL MAINTAINER sergi.torrellas@soprasteria.com

# Install python3
USER root
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install docker-py

# Add src docker
ADD ./src/ /repo/
