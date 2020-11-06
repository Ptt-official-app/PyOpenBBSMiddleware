#!/bin/bash

branch=`git branch|grep '*'|awk '{print $2}'`
project=`basename \`pwd\``

docker build --squash -t ${project}:${branch} .
