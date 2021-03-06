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

import pytest

from typing import Optional, Dict
from flask import Response
from flask.testing import FlaskClient


def test_greeting_v3(client: FlaskClient, test_config: Dict, oidc_token_read: Optional[Dict]):
    if oidc_token_read is None:
        pytest.skip('Skip test because there is no OIDC client configuration')
    rv: Response = client.get('/api/greeting/v3/',
                              headers={'Authorization': f'Bearer {oidc_token_read["access_token"]}'})
    assert rv.status_code == 200
    json_body = rv.get_json()
    assert 'message' in json_body
    assert json_body['message'] == f'Hello {test_config["client"]["preferred_name"]}'
