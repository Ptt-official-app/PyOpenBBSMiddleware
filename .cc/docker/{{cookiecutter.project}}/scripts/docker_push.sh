#!/bin/bash

if [ "$#" != "2" ]
then
  echo "usage: docker_push.sh [registry] [account]"
  exit 255
fi

registry=$1
account=$2

branch=`git branch|grep '*'|awk '{print $2}'`
project=`basename \`pwd\``

docker tag ${project}:${branch} ${registry}/${account}/${project}:${branch}
docker push ${registry}/${account}/${project}:${branch}

docker tag ${project}:${branch} ${registry}/${account}/${project}:latest
docker push ${registry}/${account}/${project}:latest
