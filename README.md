# MrMat :: Python :: API :: Flask

Boilerplate code for a Python Flask API

[![Build](https://github.com/MrMatOrg/mrmat-python-api-flask/actions/workflows/build.yml/badge.svg)](https://github.com/MrMatOrg/mrmat-python-api-flask/actions/workflows/build.yml)
[![SAST](https://github.com/MrMatOrg/mrmat-python-api-flask/actions/workflows/sast.yml/badge.svg)](https://github.com/MrMatOrg/mrmat-python-api-flask/actions/workflows/sast.yml)

This variant of a Python Flask API is code-first and using native Flask

Features:

* Code-first
* Pluggable APIs and multiple API versions
* Database schema migration using Flask-Migrate
* API body serialisation using Flask-Marshmallow
* No TLS, because this is intended to run behind a reverse proxy
* Healthz

## How to run this

You have the choice of running this 

* as a CLI app
* as a WSGI app 
* as a container image. 

### To run as a CLI app

To run this directly:

```
$ pip install -r requirements.txt
$ python ./setup.py install
$ mrmat-python-api-flask -h
usage: mrmat-python-api-flask [-h] [-d] [--host HOST] [--port PORT] [--instance-path INSTANCE_PATH] [--db DB]

mrmat-python-api-flask - 0.0.2

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Debug
  --host HOST           Host interface to bind to
  --port PORT           Port to bind to
  --instance-path INSTANCE_PATH
                        Fully qualified path to instance directory
  --db DB               Database URI

$ mrmat-python-api-flask 
[2021-05-09 16:29:49,966] INFO: Creating new instance path at /opt/dyn/python/mrmat-python-api-flask/var/mrmat_python_api_flask-instance
 * Serving Flask app "mrmat_python_api_flask" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
INFO  [werkzeug]  * Running on http://localhost:8080/ (Press CTRL+C to quit)

<Ctrl-C>
```

The instance directory defaults to `var/instance/` but can be overridden to be a fully qualified path via the 
`--instance-path` option. Any database supported by SQLAlchemy can be provided by the `--db` option. The database is 
a SQLite database within the instance directory by default.

When running in the CLI, the database is created and migrated to the latest revision.

### To run as a WSGI app

To run as a WSGI app, execute the following. When running as a WSGI app, the database is not created and migrated
on its own.

```
$ flask db upgrade
$ gunicorn --workers 2 'mrmat_python_api_flask:create_app()'
```
### To run as a container

To run as a container, first build that container:

```
$ python ./setup.py sdist
$ docker build -t mrmat-python-api-flask:0.0.1 -f var/docker/Dockerfile .
...
$ docker run --rm mrmat-python-api-flask:0.0.1
...

>You may be tempted by Alpine, but most of the Python wheels do not work for it. Go for slim-buster instead

## How to use this

Once started, you can curl towards the APIs mounted at various places. See the invocations of `app.register_blueprint`
within `mrmat_python_api_flask/__.init__.py` to find out where. 

>Note that omitting the last slash will cause a redirect that you can follow using curls -L option. We can probably
>get rid of that by using a more clever versioning scheme that doesn't make the root resource listen on / (e.g. `/greeting`).

## How to test this

Unit tests are within the `tests` directory. You can use the built-in Pycharm test configuration or do it on the CLI.

```
$ python ./setup.py install
$ python -m flake8
$ python -m pytest
```
