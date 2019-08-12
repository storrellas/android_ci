#!/bin/bash

# url="git://github.com/some-user/my-repo.git"
# url="https://github.com/some-user/my-repo.git"
url=$REPO_URL

re="^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$"

if [[ $url =~ $re ]]; then    
    protocol=${BASH_REMATCH[1]}
    separator=${BASH_REMATCH[2]}
    hostname=${BASH_REMATCH[3]}
    user=${BASH_REMATCH[4]}
    repo=${BASH_REMATCH[5]}
fi

basename=$(basename $url)
repo_name=${basename%.*}

# Clone
ssh-keyscan -H $hostname >> ~/.ssh/known_hosts
git clone $url
cd $repo_name
ls -la

# Launch gradle
./gradlew build --debug


