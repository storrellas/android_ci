FROM gradle:latest


ENV HTTP_PROXY ${HTTP_PROXY}

# Configuration for apt
RUN echo "Acquire::http::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_http
RUN cat /etc/apt/apt.conf.d/proxy_http
RUN echo "Acquire::https::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_https
RUN cat /etc/apt/apt.conf.d/proxy_https

# Install dependencies
RUN env
RUN ls -la
RUN apt-get update
RUN apt-get install nano dnsutils -y
