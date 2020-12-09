#!/bin/bash

if [ "$1" == "" ]; then
    echo "usage: swagger.sh [host]"
    exit 255
fi

host=$1

apidoc/yamltojson.py apidoc/template.yaml apidoc/template.json

flaskswagger openbbs_middleware.main:app --host ${host} --base-path / --out-dir swagger --from-file-keyword=swagger_from_file --template ./apidoc/template.json

docker container stop swagger-ui
docker container rm swagger-ui
docker run -itd --restart always --name swagger-ui -p 5000:8080 -e SWAGGER_JSON=/foo/swagger.json -v ${PWD}/swagger:/foo swaggerapi/swagger-ui
