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
from flask import Flask

from mrmat_python_api_flask import __version__
from mrmat_python_api_flask.apis import api_greeting_v1, api_greeting_v2, api_healthz

app = Flask(__name__)
app.register_blueprint(api_healthz, url_prefix='/healthz')
app.register_blueprint(api_greeting_v1, url_prefix='/api/greeting/v1')
app.register_blueprint(api_greeting_v2, url_prefix='/api/greeting/v2')


def main() -> int:
    """
    Main entry point
    :return: Exit code
    """
    parser = argparse.ArgumentParser(description=f'mrmat-python-api-flask - {__version__}')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='Debug')
    parser.add_argument('--host',
                        dest='host',
                        required=False,
                        default='localhost',
                        help='Host interface to bind to')
    parser.add_argument('--port',
                        dest='port',
                        required=False,
                        default=8080,
                        help='Port to bind to')

    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)
    return 0


if __name__ == '__main__':
    sys.exit(main())
