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
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

"""Main entry point when executing this application as a WSGI app
"""
import json
import sys
import os
import pkg_resources
from logging.config import dictConfig

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_oidc import OpenIDConnect
import flask_oidc.discovery
from flask_smorest import Api

__version__ = pkg_resources.get_distribution('mrmat-python-api-flask').version
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
oidc = OpenIDConnect()
api = Api()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    },
    'mrmat_python_api_flask': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app(config_override=None, instance_path=None):
    """Factory method to create a Flask app.

    Allows configuration overrides by providing the optional test_config dict as well as a `config.py`
    within the instance_path. Will create the instance_path if it does not exist. instance_path is meant
    to be outside the package directory.

    Args:
        config_override: Optional dict to override configuration
        instance_path: Optional fully qualified path to instance directory (for configuration etc)

    Returns: an initialised Flask app object

    """
    app = Flask(__name__,
                static_url_path='',
                static_folder='static',
                instance_relative_config=True,
                instance_path=instance_path)

    #
    # Set configuration defaults. If a config file is present then load it. If we have overrides, apply them

    app.config.setdefault('FLASK_RUN_SCHEME', 'http')
    app.config.setdefault('FLASK_RUN_HOST', 'localhost')
    app.config.setdefault('FLASK_RUN_PORT', 5000)
    app.config.setdefault('SECRET_KEY', os.urandom(16))
    app.config.setdefault('SQLALCHEMY_DATABASE_URI',
                          'sqlite+pysqlite:///' + os.path.join(app.instance_path, 'mrmat-python-api-flask.sqlite'))
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.config.setdefault('OIDC_CLIENT_SECRETS', os.path.join(app.instance_path, 'oidc_config.json'))
    app.config.setdefault('OIDC_USER_INFO_ENABLED', True)
    app.config.setdefault('OIDC_RESOURCE_SERVER_ONLY', True)
    app.config.setdefault('API_TITLE', 'MrMat :: Python :: API :: Flask')
    app.config.setdefault('API_VERSION', __version__)
    app.config.setdefault('OPENAPI_VERSION', '3.0.2')
    app.config.setdefault('OPENAPI_URL_PREFIX', '/apidoc')
    app.config.setdefault('OPENAPI_JSON_PATH', 'openapi.json')
    app.config.setdefault('OPENAPI_SWAGGER_UI_PATH', 'swagger')
    app.config.setdefault('OPENAPI_SWAGGER_UI_URL', 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/')
    app.config.setdefault('OPENAPI_REDOC_PATH', 'redoc')
    app.config.setdefault('OPENAPI_REDOC_URL', 'https://rebilly.github.io/ReDoc/releases/latest/redoc.min.js')
    app.config.setdefault('OPENAPI_RAPIDOC_PATH', 'rapidoc')
    app.config.setdefault('OPENAPI_RAPIDOC_URL', 'https://unpkg.com/rapidoc/dist/rapidoc-min.js')
    app.config.setdefault('OPENAPI_SWAGGER_UI_CONFIG', {
        'oauth2RedirectUrl': f"{app.config['FLASK_RUN_SCHEME']}://{app.config['FLASK_RUN_HOST']}:"
                             f"{app.config['FLASK_RUN_PORT']}/apidoc/swagger/oauth2-redirect"
    })
    app.config.setdefault('OPENAPI_SWAGGER_UI_ENABLE_OAUTH', True)

    #
    # Allow overriding the defaults via a JSON file pointed to by the FLASK_CONFIG environment variable
    # and via the config_override mapping provided by the CLI if we're called that way

    if 'FLASK_CONFIG' in os.environ and os.path.exists(os.path.expanduser(os.environ['FLASK_CONFIG'])):
        app.logger.info(f"Configuring from {os.environ['FLASK_CONFIG']}")
        app.config.from_json(os.path.expanduser(os.environ['FLASK_CONFIG']))
    if config_override is not None:
        app.logger.info('Configuring overrides')
        app.config.from_mapping(config_override)

    #
    # Create the instance folder if it does not exist

    try:
        if not os.path.exists(app.instance_path):
            app.logger.info(f'Creating new instance path at {app.instance_path}')
            os.makedirs(app.instance_path)
        else:
            app.logger.info(f'Using existing instance path at {app.instance_path}')
    except OSError:
        app.logger.error(f'Failed to create new instance path at {app.instance_path}')
        sys.exit(1)

    # Initialize the app
    # When using Flask-SQLAlchemy, there is no need to explicitly import DAO classes because they themselves
    # inherit from the SQLAlchemy model

    global db, ma, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    api.init_app(app)

    #
    # Initialise OIDC if we have configuration
    # If the json file at OIDC_CLIENT_SECRETS does not exist but we have OIDC_DISCOVERY,
    # OIDC_CLIENT_ID and OIDC_CLIENT_SECRET then we can construct it through discovery.
    # Note that this actually *must* be called OIDC_CLIENT_SECRETS because it's hardcoded within
    # the flask_oidc module.

    def set_oidc_security_scheme(oidc_config: dict):
        api.spec.components.security_scheme('mrmat_keycloak', {
            'type': 'oauth2',
            'flows': {
                'authorizationCode': {
                    'authorizationUrl': oidc_config['web']['auth_uri'],
                    'tokenUrl': oidc_config['web']['token_uri'],
                    'scopes': {
                        'openid': 'Basic token without extra authorisation',
                        'mrmat-python-api-flask-resource-read': 'Allows reading objects '
                                                                'in the Resource API',
                        'mrmat-python-api-flask-resource-write': 'Allows creating/modifying'
                                                                 ' and deleting objects '
                                                                 'in the Resource API'
                    }
                }
            }})

    #
    # Offer a redirect for UI OIDC authentication

    @app.route('/apidoc/swagger/oauth2-redirect')
    def oauth2_redirect():
        return render_template('swagger-ui-redirect.html')

    #
    # Construct the OIDC configuration if sufficient parameters are available

    if os.path.exists(app.config.get('OIDC_CLIENT_SECRETS')):
        app.logger.info(f"Initialising OIDC from {app.config.get('OIDC_CLIENT_SECRETS')}")
        oidc.init_app(app)
        with open(app.config.get('OIDC_CLIENT_SECRETS'), 'r') as c:
            oidc_config = json.load(c)
        set_oidc_security_scheme(oidc_config)
    elif {'OIDC_DISCOVERY', 'OIDC_CLIENT_ID', 'OIDC_CLIENT_SECRET'} <= set(app.config.keys()):
        app.logger.info(f"Discovering OIDC from {app.config.get('OIDC_DISCOVERY')}")
        discovery = flask_oidc.discovery.discover_OP_information(app.config.get('OIDC_DISCOVERY'))
        oidc_config = {
            'web': {
                'client_id': app.config.get('OIDC_CLIENT_ID'),
                'client_secret': app.config.get('OIDC_CLIENT_SECRET'),
                'auth_uri': discovery['authorization_endpoint'],
                'token_uri': discovery['token_endpoint'],
                'token_introspection_uri': discovery['introspection_endpoint'],
                'userinfo_uri': discovery['userinfo_endpoint'],
                'issuer': discovery['issuer'],
                'redirect_uris': [
                    f"{app.config['FLASK_RUN_SCHEME']}://{app.config['FLASK_RUN_HOST']}:"
                    f"{app.config['FLASK_RUN_PORT']}/oidc_callback"
                ]
            }
        }
        with open(app.config.get('OIDC_CLIENT_SECRETS'), 'x') as c:
            json.dump(oidc_config, c)
        oidc.init_app(app)
        set_oidc_security_scheme(oidc_config)
    else:
        app.logger.warning('Running without any authentication/authorisation')

    #
    # Import and register our APIs here

    from mrmat_python_api_flask.apis.healthz import api_healthz  # pylint: disable=import-outside-toplevel
    from mrmat_python_api_flask.apis.greeting.v1 import api_greeting_v1  # pylint: disable=import-outside-toplevel
    from mrmat_python_api_flask.apis.greeting.v2 import api_greeting_v2  # pylint: disable=import-outside-toplevel
    from mrmat_python_api_flask.apis.greeting.v3 import api_greeting_v3  # pylint: disable=import-outside-toplevel
    from mrmat_python_api_flask.apis.resource.v1 import api_resource_v1  # pylint: disable=import-outside-toplevel
    api.register_blueprint(api_healthz, url_prefix='/healthz')
    api.register_blueprint(api_greeting_v1, url_prefix='/api/greeting/v1')
    api.register_blueprint(api_greeting_v2, url_prefix='/api/greeting/v2')
    api.register_blueprint(api_greeting_v3, url_prefix='/api/greeting/v3')
    api.register_blueprint(api_resource_v1, url_prefix='/api/resource/v1')

    return app
