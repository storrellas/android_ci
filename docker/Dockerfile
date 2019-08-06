FROM gradle:latest


ENV HTTP_PROXY "http://barc.proxy.corp.sopra:8080"
ENV HTTPS_PROXY "http://barc.proxy.corp.sopra:8080"

RUN echo 'Acquire::http::Proxy "http://barc.proxy.corp.sopra:8080";' > /etc/apt/apt.conf.d/proxy_http
RUN echo 'Acquire::https::Proxy "http://barc.proxy.corp.sopra:8080";' > /etc/apt/apt.conf.d/proxy_https

RUN env
RUN ls -la
RUN apt-get update
RUN apt-get install nano dnsutils -y
