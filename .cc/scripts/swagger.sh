#!/bin/bash

flaskswagger openbbs_middleware.main:app --host localhost:5000 --base-path / --out-dir swagger --from-file-keyword=swagger_from_file --template ./apidoc/template.json

docker container stop swagger-ui
docker container rm swagger-ui
docker run --name swagger-ui -p 5000:8080 -e SWAGGER_JSON=/foo/swagger.json -v ${PWD}/swagger:/foo swaggerapi/swagger-ui
