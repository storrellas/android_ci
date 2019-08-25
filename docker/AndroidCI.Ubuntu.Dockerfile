FROM ubuntu:latest
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

# # Configuration for apt
# RUN echo "Acquire::http::Proxy  \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_http
# RUN echo "Acquire::https::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_https

# Install dependencies
RUN env
RUN apt-get update
RUN apt-get install unzip nano dnsutils wget openjdk-8-jdk git -y

# Install gradle
RUN wget https://services.gradle.org/distributions/gradle-5.1.1-all.zip -P /tmp
RUN unzip -d /opt/gradle /tmp/gradle-*.zip
ENV GRADLE_HOME /opt/gradle/gradle-5.1.1
ENV PATH ${GRADLE_HOME}/bin:${PATH}

# Get android-sdk
RUN wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
RUN mkdir android-sdk
RUN unzip sdk-tools-linux-4333796.zip -d /opt/android-sdk/

# Export the Android SDK path
ENV ANDROID_HOME="/opt/android-sdk"
ENV PATH="${PATH}:${ANDROID_HOME}/tools/bin"
ENV PATH="${PATH}:${ANDROID_HOME}/platform-tools"
#RUN sdkmanager --list --verbose --no_https --proxy=http --proxy_host=barc.proxy.corp.sopra --proxy_port=8080

# # CONFIGURE android-sdk
# RUN echo y | sdkmanager --no_https --proxy=http --proxy_host=${HTTP_PROXY_HOST} --proxy_port=${HTTP_PROXY_PORT} "platforms;android-28"
# RUN echo y | sdkmanager --no_https --proxy=http --proxy_host=${HTTP_PROXY_HOST} --proxy_port=${HTTP_PROXY_PORT} "platform-tools"
# RUN echo y | sdkmanager --no_https --proxy=http --proxy_host=${HTTP_PROXY_HOST} --proxy_port=${HTTP_PROXY_PORT} "build-tools;28.0.3"
# RUN yes | sdkmanager --no_https --proxy=http --proxy_host=${HTTP_PROXY_HOST} --proxy_port=${HTTP_PROXY_PORT} --licenses

RUN echo y | sdkmanager "platforms;android-28"
RUN echo y | sdkmanager "platform-tools"
RUN echo y | sdkmanager "build-tools;28.0.3"
RUN yes | sdkmanager --licenses

WORKDIR /root/
ADD ./docker/startup.sh.default /root/startup.sh
CMD bash -x /root/startup.sh


