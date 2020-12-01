#!/bin/bash

# virtualenv_dir
if [ "${BASH_ARGC}" != "1" ]
then
  virtualenv_dir="__"
else
  virtualenv_dir="${BASH_ARGV[0]}"
fi

the_basename=`basename \`pwd\``

echo -e "\033[1;32m[INFO]\033[m virtualenv_dir: ${virtualenv_dir} the_basename: ${the_basename}"

# virtualenv
if [ ! -d ${virtualenv_dir} ]
then
  echo -e "\033[1;32m[INFO]\033[m no ${virtualenv_dir}. will create one"
  virtualenv -p `which python3` --prompt="[${the_basename}] " "${virtualenv_dir}"
fi


echo -e "\033[1;32m[INFO]\033[m to activate: ${virtualenv_dir}"
source ${virtualenv_dir}/bin/activate

the_python_path=`which python`
echo -e "\033[1;32m[INFO]\033[m python: ${the_python_path}"

echo -e "\033[1;32m[INFO]\033[m current_dir: `pwd`"

# cp all to current dir
rm -rf .cc/.git*
ln -s .cc/scripts ./

# post setup - git

# gitignore
if [ ! -f .gitignore ]
then
    echo "/${virtualenv_dir}" >> .gitignore
fi

# requirements-dev.txt
echo -e "\033[1;32m[INFO]\033[m requirements-dev:"
if [ ! -f requirements-dev.txt ]
then
    cp .cc/requirements-dev.txt requirements-dev.txt
fi
pip install -r requirements-dev.txt

# project_dev
echo -e "\033[1;32m[INFO]\033[m to init project"
./scripts/project_dev.sh

# git init
echo -e "\033[1;32m[INFO]\033[m to git init"
git init; git add .; git commit -m "init dev"

# done
echo -e "\033[1;32m[INFO]\033[m done"
echo -e "\033[1;32m[INFO]\033[m remember to: . __/bin/activate"
