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

"""Blueprint for the Greeting API in V3
"""

from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint
from mrmat_python_api_flask import oidc
from .model import GreetingV3Output, greeting_v3_output

bp = Blueprint('greeting_v3',
               __name__,
               description='The Greeting V3 API')


@bp.route('/')
class GreetingV3(MethodView):

    @oidc.accept_token(require_token=True)
    @bp.doc(security=[{'mrmat_keycloak': ['profile']}])
    @bp.response(200, GreetingV3Output)
    def get(self):
        """Get a greeting for your asserted name from a JWT token
        """
        return greeting_v3_output.dump({'message': f'Hello {g.oidc_token_info["preferred_username"]}'}), 200
