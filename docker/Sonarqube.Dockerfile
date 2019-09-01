FROM sonarqube:lts
LABEL MAINTAINER sergi.torrellas@soprasteria.com

ARG HTTP_PROXY
ARG HTTP_PROXY_HOST
ARG HTTP_PROXY_PORT
ARG APPCENTER_TOKEN

# ENV HTTP_PROXY ${HTTP_PROXY}
# ENV HTTPS_PROXY ${HTTP_PROXY}
# ENV http_proxy ${HTTP_PROXY}
# ENV https_proxy ${HTTP_PROXY}
# ENV HTTP_PROXY_HOST ${HTTP_PROXY_HOST}
# ENV HTTP_PROXY_PORT ${HTTP_PROXY_PORT}

USER root

# Configuration for apt
# RUN echo "Acquire::http::Proxy  \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_http
# RUN echo "Acquire::https::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_https

RUN apt update
RUN apt install -y sudo

# Add sonarqube user to sudoers
RUN echo "sonarqube ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


# RUN usermod --shell /bin/bash sonarqube
# RUN grep sonarqube /etc/passwd

USER sonarqube

RUN sudo cat /etc/sudoers

# Launch sonarqube
ADD ./docker/sonarqube_startup.sh.default /opt/sonarqube/startup.sh


#CMD "chmod sonarqube:sonarqube -R ./data/; ./bin/run.sh"
#CMD ["chmod", "sonarqube:sonarqube", "-R", "./data/", "&&", "ls", "-la"]
#CMD "/bin/bash -x chmod sonarqube:sonarqube -R ./data/"
#CMD whoami; chown sonarqube:sonarqube -R /opt/sonarqube/; ls -la; su sonarqube 

# RUN chmod -R 777 /opt/sonarqube/
# RUN groupadd -r sonarqube && useradd -r -g sonarqube sonarqube
#RUN chown -R root:root /opt/sonarqube/

# Modify sonar.properties
#ADD ./docker/sonar.properties /opt/sonarqube/conf


