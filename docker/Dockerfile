FROM gradle:latest


ENV HTTP_PROXY ${HTTP_PROXY}
ENV HTTPS_PROXY ${HTTP_PROXY}
ENV http_proxy ${HTTP_PROXY}
ENV https_proxy ${HTTP_PROXY}

# Configuration for apt
RUN echo "Acquire::http::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_http
RUN echo "Acquire::https::Proxy \"$HTTP_PROXY\";" > /etc/apt/apt.conf.d/proxy_https

# Install dependencies
RUN env
RUN ls -la
RUN apt-get update
RUN apt-get install nano dnsutils wget -y

# Get android-sdk
RUN wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
RUN mkdir android-sdk
RUN unzip sdk-tools-linux-4333796.zip -d /opt/android-sdk/
WORKDIR /opt/android-sdk/

# Export the Android SDK path
ENV ANDROID_HOME="/opt/android-sdk"
ENV PATH="${PATH}:${ANDROID_HOME}/tools/bin"
ENV PATH="${PATH}:${ANDROID_HOME}/platform-tools"
RUN env
#RUN sdkmanager --list --verbose --no_https --proxy=http --proxy_host=barc.proxy.corp.sopra --proxy_port=8080

# CONFIGURE android-sdk
# RUN echo y | sdkmanager --no_https --proxy=http --proxy_host=barc.proxy.corp.sopra --proxy_port=8080 "platforms;android-28"
# RUN echo y | sdkmanager --no_https --proxy=http --proxy_host=barc.proxy.corp.sopra --proxy_port=8080 "platform-tools"
# RUN echo y | sdkmanager --no_https --proxy=http --proxy_host=barc.proxy.corp.sopra --proxy_port=8080 "build-tools;28.0.3"
# RUN yes | sdkmanager --no_https --proxy=http --proxy_host=barc.proxy.corp.sopra --proxy_port=8080 --licenses

RUN echo y | sdkmanager "platforms;android-28"
RUN echo y | sdkmanager "platform-tools"
RUN echo y | sdkmanager "build-tools;28.0.3"
RUN yes | sdkmanager --licenses

# Install Jenkins
RUN apt install -y gnupg2
RUN wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | apt-key add -
RUN bash -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
RUN apt update
RUN apt install -y jenkins

#CMD export JENKINS_HOME=/var/lib/jenkins && java -jar /usr/share/jenkins/jenkins.war

