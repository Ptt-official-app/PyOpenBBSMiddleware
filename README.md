PyOpenBBSMiddleware
==========

Python middleware for OpenBBS.

Docker
-----

You can run docker with the following steps:

* `docker-compose -f docker-compose.yaml up -d`
* register at `http://localhost:3457/Account/register`
* login at `http://localhost:3457/Account/login`
* logout at `http://localhost:3457/Account/logout`
* `telnet localhost 8888` and use the account that you registered.
* swagger spec at `http://localhost:3457/spec` (paste in `https://petstore.swagger.io/`)

Develop
-----

You can start developing with the following steps:

* `git clone [repo]`
* `./scripts/clone_projet.sh`

Use the following template-script to start a module (automatically generate code-files and test-files):

* `./scripts/dev_module.sh [module]`

ex: `./scripts/dev_module.sh a.b.c`

Unit-Test
-----

You can do unit-test with:

* `./scripts/test.sh`

Swagger
-----

You can run swagger with:
* `./scripts/swagger.sh`
