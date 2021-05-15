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

import sys
import argparse
from oauthlib.oauth2 import MobileApplicationClient
from requests_oauthlib import OAuth2Session

from mrmat_python_api_flask import __version__


def main() -> int:
    """
    Main entry point
    Returns: Exit code
    """
    parser = argparse.ArgumentParser(description=f'mrmat-python-api-flask-client - {__version__}')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='Debug')

    args = parser.parse_args()

    oauth = OAuth2Session(
        client=MobileApplicationClient(client_id='mrmat-python-api-flask-client', scope=['openid']))
    authorization_url, state = oauth.authorization_url('https://keycloak.mrmat.org/auth/realms/master/protocol/openid-connect/auth')
    response = oauth.get(authorization_url)
    token = oauth.token_from_fragment(response.url)
    pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
