# MrMat :: Python :: API :: Flask

Boilerplate code for a Python Flask API

[![Build](https://github.com/MrMatOrg/mrmat-python-api-flask/actions/workflows/build.yml/badge.svg)](https://github.com/MrMatOrg/mrmat-python-api-flask/actions/workflows/build.yml)
[![SAST](https://github.com/MrMatOrg/mrmat-python-api-flask/actions/workflows/sast.yml/badge.svg)](https://github.com/MrMatOrg/mrmat-python-api-flask/actions/workflows/sast.yml)


This variant of a Python Flask API is code-first and using native Flask

Features:

* Code-first
* Multiple API versions
* No TLS, because this is intended to run behind a reverse proxy
* Healthz

## How to run this

Start with `mrmat-python-api-flask`. You can specify `--host 0.0.0.0` to listen on a specific API and `--port PORT` to
override the default 8080.

Once started, you can do curl towards the greeting API at `/api/greeting/v1/` and `/api/greeting/v1/?name=Custom`.
Note that omitting the last slash will cause a redirect that you can follow using curls -L option. We can probably
get rid of that by using a more clever versioning scheme that doesn't make the root resource listen on / (e.g. `/greeting`).

## How to test this

Pycharm built-in. If you do it on the CLI, you do need `python -m pytest`, otherwise it'll get confused about loading
its modules. Also note that the API spec yaml must be added once more when testing in `conftest.py`. The obvious attempt
to have that done straight within `mrmat_python_api_flask/app.py` outside main doesn't work (and I don't know why).

## How to build this

See the provided Dockerfile in `var/docker`. This requires that you have run `python ./setup.py sdist` as a prerequisite
and will create a container image in which the application is run within a production-ready WSGI server.

