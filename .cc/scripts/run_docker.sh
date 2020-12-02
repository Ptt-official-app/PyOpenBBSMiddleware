#!/bin/bash

host=${1:-127.0.0.1}

. __/bin/activate

echo "to run python: host: ${host}"

python -m openbbs_middleware.main -i production.docker.ini --host ${host} -p 3457
