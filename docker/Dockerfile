FROM gradle:latest


ENV HTTP_PROXY ${HTTP_PROXY}
ENV HTTPS_PROXY ${HTTP_PROXY}
ENV http_proxy ${HTTP_PROXY}
ENV https_proxy ${HTTP_PROXY}

# Configuration for apt
RUN echo "Acquire::http::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_http
RUN cat /etc/apt/apt.conf.d/proxy_http
RUN echo "Acquire::https::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_https


# Install dependencies
RUN env
RUN ls -la
RUN apt-get update
RUN apt-get install nano dnsutils wget -y

# Get android-sdk
RUN wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
#use_proxy=yes
#http_proxy=barc.proxy.corp.sopra:8080
#https_proxy=barc.proxy.corp.sopra:8080


