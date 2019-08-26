ls -la
echo $PWD
env
export PROJECT_LOCATION="$JENKINS_HOME_HOST/${PWD#/var/jenkins_home/}"
echo $PROJECT_LOCATION
export JENKINS_COMMAND="./gradlew -Dhttp.proxyHost=barc.proxy.corp.sopra -Dhttp.proxyPort=8080 -Dhttps.proxyHost=barc.proxy.corp.sopra -Dhttps.proxyPort=8080 -Dhttp.nonProxyHosts=nexus.nespresso.com -Dhttps.nonProxyHosts=nexus.nespresso.com build"
#sudo docker run -w /root/project -v/home/sergi/android_ci/jenkins_home/workspace/androi_ci:/root/project ./gradlew build
#sudo docker run -w /root/project -v/home/sergi/workspace_for_android_ci/we_are_nutrition-android/:/root/project/ android_ci ./gradlew build
sudo docker run -w /root/project -v$PROJECT_LOCATION:/root/project/ android_ci $JENKINS_COMMAND