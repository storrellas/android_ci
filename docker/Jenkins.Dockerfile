FROM jenkins/jenkins:lts
LABEL MAINTAINER sergi.torrellas@soprasteria.com

ARG HTTP_PROXY
ARG HTTP_PROXY_HOST
ARG HTTP_PROXY_PORT

# ENV HTTP_PROXY ${HTTP_PROXY}
# ENV HTTPS_PROXY ${HTTP_PROXY}
# ENV http_proxy ${HTTP_PROXY}
# ENV https_proxy ${HTTP_PROXY}
# ENV HTTP_PROXY_HOST ${HTTP_PROXY_HOST}
# ENV HTTP_PROXY_PORT ${HTTP_PROXY_PORT}

USER root

# # Configuration for apt
# RUN echo "Acquire::http::Proxy  \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_http
# RUN echo "Acquire::https::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_https

# Install python3
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install docker

# Install docker
RUN apt install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN apt update
RUN apt install -y docker-ce

# Install docker-compose
RUN curl -L \
      https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)\ 
      -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN docker-compose --version

# Add src docker
ADD ./src/ /repo/

# # Running jenkins manually
# CMD java -Dhttp.proxyHost=$HTTP_PROXY_HOST \ 
#       -Dhttp.proxyPort=$HTTP_PROXY_PORT \ 
#       -Duser.home=/var/jenkins_home \
#       -Djenkins.model.Jenkins.slaveAgentPort=50000 \
#       -jar /usr/share/jenkins/jenkins.war