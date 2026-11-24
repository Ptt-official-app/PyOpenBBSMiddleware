# Repository Guidelines

## Project Overview
`github.com/Ptt-official-app/PyOpenBBSMiddleware`: Python (Flask + gevent) middleware between web/app clients and a PTT BBS backend (`go-pttbbs`), with MongoDB for client/user/token state. **Deprecated**: development moved to `go-openbbsmiddleware` (now `pttbbs-backend`) starting from v0.3.0 (see README); this repo is effectively unmaintained at v0.2.0. Targets Python 3.7/3.8 (Dockerfile uses 3.7, CI uses 3.8).

## Architecture & Data Flow
Client -> Flask route in `openbbs_middleware/main.py` (`/api` prefix via `_with_app_prefix`, `@crossdomain()`) -> `util_flask.process_json()` / `process_params()` -> `api.X(params)` returns `(err, result)` -> `util_flask.process_result(err, result)` (JSON; `{'err': str(err)}` on error).
- Auth: `before_request` sets `flask.g.user` from the `Authorization: bearer <token>` header by looking up the `access_token` collection (`get_user_id`); `login_required` returns 401 when empty.
- Login/register (`api/account_login.py`, `api/account_register.py`): validate `client_id`/`client_secret` against the `client` collection (`account/utils.is_valid_client`), forward credentials to the backend via `utils/util_http.http_post` (`ptt_server` config + `backend/routes.py`), then `post_login` stores the returned JWT in `access_token`/`user`.
- Board search (`api/find_board_by_name.py`): `http_post` to the backend, then `deserialize/deserialize_board_list.py` -> `deserialize_board_summary.py` (adds per-user `read` state from `user_read_board`).
- Browser form flow (`/login`, `/register`, `/logout`): flask-security with custom forms in `http_server/` and `register_user` monkey-patched in `util_flask.py`. Passwords are not stored; only `user_id`, `jwt`, `uid`.
- Most other modules in `api/` (e.g. `get_user_info`, `get_post_list`, `get_favorite_board`) return hard-coded mock data (marked `XXX mock-data`) or are empty stubs; `mock/` holds board fixtures used by tests.

## Key Directories
- `openbbs_middleware/api/` one module per endpoint (`ROUTE` constant + handler function)
- `openbbs_middleware/http_server/` Flask app setup (`util_flask.py`), flask-security forms, `register_user.py`
- `openbbs_middleware/account/` backend login/register calls, client validation, `post_login`
- `openbbs_middleware/backend/routes.py` backend URL paths; `deserialize/`, `schema/`, `mock/`, `utils/`, `static/` (login/register HTML), `cfg.py` (config + Mongo collection map), `constants.py`
- `tests/` mirrors the package layout; `tests/test.ini` is the test config; `tests/mock.py` mocks `requests.post`
- `apidoc/` swagger YAML (`template.yaml` -> `template.json` via `yamltojson.py`; referenced by `swagger_from_file:` docstrings in `main.py`)
- `.cc/` cookiecutter templates and generators; `scripts` is a symlink to `.cc/scripts`

## Development Commands
```
./scripts/clone_project.sh        # create virtualenv `__` and pip install requirements-dev.txt
./scripts/dev_module.sh a.b.c     # generate module + test file via cookiecutter
./scripts/test.sh                 # nosetests --rednose -v
./scripts/coverage.sh             # nosetests --with-coverage --cover-package=openbbs_middleware
./scripts/lint.sh                 # python -m pre_commit run --all (flake8, whitespace hooks)
./scripts/run.sh [host]           # python -m openbbs_middleware.main -i production.ini.template --host H -p 3457
./scripts/swagger.sh <host>       # build apidoc/template.json, run swagger-ui in docker on :5000
./scripts/docker_initbbs.sh <BBSHOME> pttofficialapps/go-pttbbs:latest
docker-compose --env-file docker_compose.env -f docker-compose.yaml up -d
```
`main.py` requires `-i <ini>` and `-p <port>`; it reads `apidoc/template.json` relative to the cwd, so run from the repo root. `tox` runs `lint`, `py37`, `py38`.

## Code Conventions & Common Patterns
- **API module pattern**: `ROUTE = '/Path'` and `def handler(params): ... return None, result` or `return err, {}` (error first, `pyutil_mongo` style). Register the route in `main.py` with `@app.route(_with_app_prefix(...))` + `@crossdomain()` and a `swagger_from_file: apidoc/<name>.yaml` docstring.
- Errors are returned, not raised; helpers like `utils/util.flatten_errors` and `util_type._int` also return `(err, value)`.
- Mongo access only through `pyutil_mongo` (`db_find_one`, `db_find`, `db_update`); collections are declared in `cfg._USER_COLLECTION_MAP`. Timestamps are milliseconds (`util_time.get_current_milli_ts`).
- Config: INI section `[openbbs_middleware:main]` loaded by `pyutil_cfg` into `cfg.config` (keys such as `mongo_host`, `mongo_dbname`, `ptt_server`, `host`, `flask_secret_file`, `flask_security_salt_file`, `flask_static_folder`). `cfg.logger` is the logger.
- Style: 4-space indent, `# -*- coding: utf-8 -*-` header, Google-style docstrings, single-quoted strings; flake8 rules are in `.pre-commit-config.yaml` (E501/E402/F401 ignored).

## Important Files
`openbbs_middleware/main.py`, `openbbs_middleware/http_server/util_flask.py`, `openbbs_middleware/cfg.py`, `openbbs_middleware/account/utils.py`, `openbbs_middleware/utils/util_http.py`, `setup.py` (dependency pins), `tests/__init__.py` (global test setup), `tests/test.ini`, `production.ini.template`, `production.docker.ini`, `docker-compose.yaml`, `Dockerfile`, `.github/workflows/main.yml`.

## Runtime/Tooling Preferences
- Dependencies are pinned in `setup.py` (Flask-Security-Too 3.4.4, flask-mongoengine 1.0.0, Werkzeug 0.16.1, gevent 20.9.0, requests 2.25.0) and pull `pyutil_cfg`, `pyutil_mongo` and a `flask-swagger` fork from GitHub; they are old and may not install on current Python versions. `python-rapidjson` is imported but only comes in transitively via `pyutil_cfg`.
- Runtime needs MongoDB and a reachable go-pttbbs at `ptt_server` (e.g. `http://localhost:3456/v1`). Unit tests use `mongomock` and mocked `requests.post`, so they need neither.
- Test runner is `nose` 1.3.7, which does not run on Python 3.10+.

## Testing & QA
- `unittest.TestCase` classes under `tests/`, one `test_<module>.py` per module (many are empty generated skeletons). Run with `nosetests`.
- `tests/__init__.py` `setup()` (nose package fixture) calls `cfg.init('tests/test.ini')`, `util_flask.init_flask()` and seeds client `test_client_id` / `test_client_secret`. It is not run by pytest; with pytest, call `tests.setup()` from a `conftest.py`.
- Wrap tests that touch Mongo in `@mongomock.patch(servers=(('localhost', 27017),))`; mock the backend with `@mock.patch('requests.post', side_effect=mocked_requests_post)`; use `app.test_request_context(..., headers={'Authorization': 'bearer init_register'})` + `app.preprocess_request()` for code that reads `flask.g.user`.
- CI (`.github/workflows/main.yml`): Python 3.8, `pre_commit run --all`, `nosetests`, coverage.
