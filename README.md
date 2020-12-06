# PyOpenBBSMiddleware

Python middleware for OpenBBS.

## Docker

You can run docker with the following steps:

* copy `docker_compose.env.template` to `docker_compose.env` and modify the settings.
* `./scripts/docker_initbbs.sh [BBSHOME] pttofficialapps/go-pttbbs:latest`
* `docker-compose --env-file docker_compose.env -f docker-compose.yaml up -d`
* register at `http://localhost:3457/Account/register`
* login at `http://localhost:3457/Account/login`
* logout at `http://localhost:3457/Account/logout`
* `telnet localhost 8888` and use the account that you registered.

## Develop

You can start developing with the following steps:

* `git clone [repo]`
* `./scripts/clone_projet.sh`

Use the following template-script to start a module (automatically generate code-files and test-files):

* `./scripts/dev_module.sh [module]`

ex: `./scripts/dev_module.sh a.b.c`

## Unit-Test

You can do unit-test with:

* `./scripts/test.sh`

## Swagger

You can run swagger with:
* `./scripts/swagger.sh`
* go to `http://localhost:5000`

## More document

You can go to [github Wiki](https://github.com/Ptt-official-app/PyOpenBBSMiddleware/wiki) and see more document there

### [程式架構](https://github.com/Ptt-official-app/PyOpenBBSMiddleware/wiki/%E7%A8%8B%E5%BC%8F%E6%9E%B6%E6%A7%8B%E8%AA%AA%E6%98%8E)
