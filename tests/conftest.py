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

import os
import logging
import json
import pytest

from typing import Optional, List, Dict

import jwt
import oauthlib.oauth2
import requests_oauthlib

from mrmat_python_api_flask import create_app, db

LOGGER = logging.getLogger(__name__)


@pytest.fixture
def test_config() -> Optional[Dict]:
    """Read the test configuration file the FLASK_CONFIG environment variable points to

    A token can only be obtained if the configuration file pointed to by the FLASK_CONFIG environment variable
    contains required entries to set up OIDC for testing. An empty dict is returned if these are not present.
    The following are required:

    {
        "web": {                This entry is required to be the very first entry. If you don't like that,
                                then externalize it into a separate file and point to it via OIDC_CLIENT_SECRETS
            "client_id":        Server side client_id
            "client_secret":    Server-side client_secret
            ...
        },
        "client": {
            "client_id":        Test client client_id
            "client_secret":    Test client secret
            "preferred_name":   Asserted preferred_name of the client_id
        "OIDC_CLIENT_SECRETS":  Point this to the same place as FLASK_CONFIG (to reduce the number of config files
    Returns:
        A dictionary of configuration or None if not configuration file is set
    """
    if 'FLASK_CONFIG' not in os.environ:
        LOGGER.info('Missing test configuration via FLASK_CONFIG environment variable. Tests are limited')
        return None
    config_file = os.path.expanduser(os.environ['FLASK_CONFIG'])
    if not os.path.exists(config_file):
        LOGGER.info('Configuration set via FLASK_CONFIG environment variable does not exist. Tests are limited')
        return None
    with open(os.path.expanduser(os.environ['FLASK_CONFIG'])) as C:
        return json.load(C)


@pytest.fixture
def client():
    """Start and configure the WSGI app.

    Configuration honours the FLASK_CONFIG environment variable but will set reasonable defaults if not present. This
    particularly overrides the configuration of an in-memory database rather than the normal persisted database in the
    instance directory.

    Yields:
        A Flask client used for testing
    """
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite://'})
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client


def oidc_token(config: Dict, scope: Optional[List]):
    """Obtain an OIDC token to be used for client testing.
    Args:
        config: Test configuration
        scope: Optional scope to request a token for. Defaults to ['openid']
    Returns:
        A dictionary containing the access token or None if configuration is lacking
    """
    if test_config is None or 'client' not in config:
        LOGGER.info('Missing OIDC test client configuration. Tests will be limited')
        return None
    for key in ['client_id', 'client_secret', 'preferred_name']:
        if key not in config['client']:
            LOGGER.info(f'Missing {key} in test client configuration. Tests will be limited')
            return None
    if scope is None:
        scope = ['openid']
    elif 'openid' not in scope:
        scope.insert(0, 'openid')
    client = oauthlib.oauth2.BackendApplicationClient(client_id=config['client']['client_id'], scope=scope)
    oauth = requests_oauthlib.OAuth2Session(client=client)
    return oauth.fetch_token(token_url=config['web']['token_uri'],
                             client_id=config['client']['client_id'],
                             client_secret=config['client']['client_secret'])


@pytest.fixture
def oidc_token_read(test_config) -> Optional[Dict]:
    """ Return an OIDC token with scope 'mrmat-python-api-flask-resource-read'

    Args:
        test_config: The test configuration as per the test_config fixture

    Returns:
        A Dict containing the desired token structure
    """
    if test_config is None:
        LOGGER.info('Missing OIDC test client configuration. Tests will be limited')
        return None
    token = oidc_token(test_config, ['mrmat-python-api-flask-resource-read'])
    token['jwt'] = jwt.decode(token['access_token'], options={"verify_signature": False})
    return token


@pytest.fixture
def oidc_token_write(test_config) -> Optional[Dict]:
    """ Return an OIDC token with scope 'mrmat-python-api-flask-resource-write'

    Args:
        test_config: The test configuration as per the test_config fixture

    Returns:
        A Dict containing the desired token structure
    """
    if test_config is None:
        LOGGER.info('Missing OIDC test client configuration. Tests will be limited')
        return None
    token = oidc_token(test_config, ['mrmat-python-api-flask-resource-write'])
    token['jwt'] = jwt.decode(token['access_token'], options={"verify_signature": False})
    return token
