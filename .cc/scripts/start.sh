#!/bin/bash

source __/bin/activate

python -m openbbs_middleware.main -i production.ini -p 3456
