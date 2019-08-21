#!/bin/bash

# Copy public key and set permission
cp -rv /root/provision/id_rsa /root/.ssh/
chown 600 /root/.ssh/id_rsa

# url="git://github.com/some-user/my-repo.git"
# url="https://github.com/some-user/my-repo.git"
url=$REPO_URL

# Get Host
re="^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$"
if [[ $url =~ $re ]]; then    
    protocol=${BASH_REMATCH[1]}
    separator=${BASH_REMATCH[2]}
    hostname=${BASH_REMATCH[3]}
    user=${BASH_REMATCH[4]}
    repo=${BASH_REMATCH[5]}
fi
ssh-keyscan -H $hostname >> ~/.ssh/known_hosts

# Get repo_name
basename=$(basename $url)
repo_name=${basename%.*}

# Clone
git clone $url
cd $repo_name

# Launch gradle
#./gradlew build --debug
./gradlew -Dhttp.proxyHost=barc.proxy.corp.sopra -Dhttp.proxyPort=8080  \
        -Dhttps.proxyHost=barc.proxy.corp.sopra -Dhttps.proxyPort=8080  \
        -Dhttp.nonProxyHosts=nexus.nespresso.com  \
        -Dhttps.nonProxyHosts=nexus.nespresso.com build --debug


