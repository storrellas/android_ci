FROM sonarqube:lts
LABEL MAINTAINER sergi.torrellas@soprasteria.com

ARG HTTP_PROXY
ARG HTTP_PROXY_HOST
ARG HTTP_PROXY_PORT
ARG APPCENTER_TOKEN

ENV HTTP_PROXY ${HTTP_PROXY}
ENV HTTPS_PROXY ${HTTP_PROXY}
ENV http_proxy ${HTTP_PROXY}
ENV https_proxy ${HTTP_PROXY}
ENV HTTP_PROXY_HOST ${HTTP_PROXY_HOST}
ENV HTTP_PROXY_PORT ${HTTP_PROXY_PORT}

USER root

# Configuration for apt
RUN echo "Acquire::http::Proxy  \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_http
RUN echo "Acquire::https::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_https

RUN apt update
RUN apt install -y sudo

# Add sonarqube user to sudoers
RUN echo "sonarqube ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


USER sonarqube

# Add startup script
ADD ./docker/sonarqube_startup.sh.default /opt/sonarqube/startup.sh



