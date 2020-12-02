#!/bin/bash

branch=`git branch|grep '^*'|sed 's/^\* //g'|sed -E 's/^\(HEAD detached at //g'|sed -E 's/\)$//g'`
project=`basename \`pwd\``

docker run --name ${project} -p 3457:3457 ${project}:${branch}

