#!/bin/bash

if [ "$#" != "1" ]
then
    echo "usage: module.sh [module]"
    exit 255
fi

module=$1
package="openbbs_middleware"

python .cc/gen.py module "${module}" "${package}"

parent_pkg=""
# split module
arr=$(echo ${module}|tr "." "\n")

# setup
for each_pkg in ${arr[@]}
do
  echo "each_pkg: ${each_pkg}"
  if [ "${parent_pkg}" != "" ]
  then
    echo "[INFO] to create pkg: ${parent_pkg}"
    python .cc/gen.py pkg "${parent_pkg}" "${package}"
    parent_pkg="${parent_pkg}."
  fi
  parent_pkg="${parent_pkg}${each_pkg}"
done
