FROM gradle:latest


ENV HTTP_PROXY "http://barc.proxy.corp.sopra:8080"
ENV HTTPS_PROXY "http://barc.proxy.corp.sopra:8080"

RUN env
RUN ls -la
RUN apt-get update
RUN apt-get install nano dnsutils -y
