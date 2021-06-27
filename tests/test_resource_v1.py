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

from typing import Dict
from flask.testing import FlaskClient

from resource_api_client import ResourceAPIClient


def test_create(client: FlaskClient, oidc_token_write: Dict):
    if oidc_token_write is None:
        pytest.skip('No OIDC configuration is available')
    rac = ResourceAPIClient(client, token=oidc_token_write)
    (resp, resp_body) = rac.create(name='Test Resource 1')
    assert resp.status_code == 201
    assert resp_body['id'] == 1
    #assert resp_body['owner'] == oidc_token_write['jwt']['sub']
    assert resp_body['name'] == 'Test Resource 1'


def test_modify(client: FlaskClient, oidc_token_write):
    if oidc_token_write is None:
        pytest.skip('No OIDC configuration is available')
    rac = ResourceAPIClient(client, token=oidc_token_write)

    (resp, resp_body) = rac.create(name='Test Resource Original')
    assert resp.status_code == 201
    assert resp_body['id'] == 1
    #assert resp_body['owner'] == oidc_token_write['jwt']['sub']
    assert resp_body['name'] == 'Test Resource Original'

    (resp, resp_body) = rac.modify(1, name='Test Resource Modified')
    assert resp.status_code == 200
    assert resp_body['id'] == 1
    #assert resp_body['owner'] == oidc_token_write['jwt']['sub']
    assert resp_body['name'] == 'Test Resource Modified'


def test_remove(client: FlaskClient, oidc_token_write):
    if oidc_token_write is None:
        pytest.skip('No OIDC configuration is available')
    rac = ResourceAPIClient(client, token=oidc_token_write)
    (resp, resp_body) = rac.create(name='Short-lived Test Resource')
    assert resp.status_code == 201
    assert resp_body['id'] == 1

    (resp, resp_body) = rac.remove(1)
    assert resp.status_code == 204
    assert resp_body is None


def test_get_all(client: FlaskClient, oidc_token_read, oidc_token_write):
    if oidc_token_read is None or oidc_token_write is None:
        pytest.skip('No OIDC configuration is available')
    rac_read = ResourceAPIClient(client, token=oidc_token_read)
    rac_write = ResourceAPIClient(client, token=oidc_token_write)

    (resp, resp_body) = rac_read.get_all()
    assert resp.status_code == 200
    assert 'resources' in resp_body
    assert len(resp_body['resources']) == 0

    (resp, resp_body) = rac_write.create(name='Test Resource 2')
    assert resp.status_code == 201
    assert resp_body['id'] >= 0

    (resp, resp_body) = rac_read.get_all()
    assert resp.status_code == 200
    assert len(resp_body['resources']) == 1


def test_get_one(client: FlaskClient, oidc_token_read, oidc_token_write):
    if oidc_token_read is None or oidc_token_write is None:
        pytest.skip('No OIDC configuration is available')
    rac_read = ResourceAPIClient(client, token=oidc_token_read)
    rac_write = ResourceAPIClient(client, token=oidc_token_write)

    (resp, resp_body) = rac_read.get_one(1)
    assert resp.status_code == 404
    assert resp_body is None

    (resp, resp_body) = rac_write.create(name='Test Resource 3')
    assert resp.status_code == 201
    assert resp_body['id'] == 1

    (resp, resp_body) = rac_read.get_one(1)
    assert resp.status_code == 200
    assert resp_body['id'] == 1
    #assert resp_body['owner'] == oidc_token_write['jwt']['sub']
    assert resp_body['name'] == 'Test Resource 3'
