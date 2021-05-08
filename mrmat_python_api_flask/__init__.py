#  MIT License
#
#  Copyright (c) 2021 MrMat
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import os
import pkg_resources

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


__version__ = pkg_resources.get_distribution('mrmat-python-api-flask').version
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def close_db(e=None):
    db: SQLAlchemy = g.pop('db', None)
    if db is not None:
        # TODO: Safely shut down DB layer
        pass


def create_app(override_config=None):
    """
    Factory method to create a Flask app.

    Allows configuration overrides by providing the optional test_config dict as well as a `config.py`
    within the instance_path. Will create the instance_path if it does not exist. instance_path is meant
    to be outside the package directory.

    Args:
        override_config: Optional dict to override configuration

    Returns: an initialised Flask app object

    """
    app = Flask(__name__, instance_relative_config=True)
    # TODO: Generate secret key
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite+pysqlite:///' + os.path.join(app.instance_path,
                                                                     'mrmat-python-api-flask.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False)
    if override_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(override_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # TODO: Log this
        pass

    # TODO: When using Flask-SQLAlchemy, the following import is not required because we're importing db.Model in the
    #       SQLAlchemy classes
    # from .dao.resource import ResourceDAO
    global db, ma, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    app.teardown_appcontext(close_db)

    from mrmat_python_api_flask.apis.healthz import bp as api_healthz
    from mrmat_python_api_flask.apis.greeting.v1 import api_greeting_v1
    from mrmat_python_api_flask.apis.greeting.v2 import api_greeting_v2
    from mrmat_python_api_flask.apis.resource.v1 import api_resource_v1
    app.register_blueprint(api_healthz, url_prefix='/healthz')
    app.register_blueprint(api_greeting_v1, url_prefix='/api/greeting/v1')
    app.register_blueprint(api_greeting_v2, url_prefix='/api/greeting/v2')
    app.register_blueprint(api_resource_v1, url_prefix='/api/resource/v1')

    return app
