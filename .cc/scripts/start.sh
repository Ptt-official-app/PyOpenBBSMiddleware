#!/bin/bash

source __/bin/activate

python -m openbbs_middelware.main -i production.ini -p 3456
