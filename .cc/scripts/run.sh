#!/bin/bash

host=${1:-127.0.0.1}

. __/bin/activate

echo "to run python: host: ${host}"

python -m openbbs_middleware.main -i production.ini.template --host ${host} -p 3457
