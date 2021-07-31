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

"""Blueprint for the Greeting API in V2
"""

from flask.views import MethodView
from flask_smorest import Blueprint
from .model import greeting_v2_output, GreetingV2Output, GreetingV2Input

bp = Blueprint('greeting_v2',
               __name__,
               description='Greeting V2 API')


@bp.route('/')
class GreetingV2(MethodView):
    """GreetingV2 API Implementation
    """

    @bp.arguments(GreetingV2Input,
                  description='The name to greet',
                  location='query',
                  required=False,
                  as_kwargs=True)
    @bp.response(200, GreetingV2Output)
    def get(self, **kwargs):
        """Get a named greeting
        ---
        It is possible to place logic here like we do for safe_name, but if we parse
        the GreetingV2Input via MarshMallow then we can also set a 'default' or 'missing' there.
        """
        safe_name: str = kwargs['name'] or 'World'
        return greeting_v2_output.dump({'message': f'Hello {safe_name}'}), 200
