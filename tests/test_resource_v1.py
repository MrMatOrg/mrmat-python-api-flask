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

from flask.testing import FlaskClient

from resource_api_client import ResourceAPIClient


def test_create(client: FlaskClient):
    rac = ResourceAPIClient(client)
    (resp, resp_body) = rac.create(owner='MrMat', name='Test Resource 1')
    assert resp.status_code == 201
    assert resp_body['id'] == 1
    assert resp_body['owner'] == 'MrMat'
    assert resp_body['name'] == 'Test Resource 1'


def test_modify(client: FlaskClient):
    rac = ResourceAPIClient(client)
    (resp, resp_body) = rac.create(owner='MrMat', name='Test Resource Original')
    assert resp.status_code == 201
    assert resp_body['id'] == 1
    assert resp_body['owner'] == 'MrMat'
    assert resp_body['name'] == 'Test Resource Original'

    (resp, resp_body) = rac.modify(1, owner='Ee Lyn', name='Test Resource Modified')
    assert resp.status_code == 200
    assert resp_body['id'] == 1
    assert resp_body['owner'] == 'Ee Lyn'
    assert resp_body['name'] == 'Test Resource Modified'


def test_remove(client: FlaskClient):
    rac = ResourceAPIClient(client)
    (resp, resp_body) = rac.create(owner='MrMat', name='Short-lived Test Resource')
    assert resp.status_code == 201
    assert resp_body['id'] == 1

    (resp, resp_body) = rac.remove(1)
    assert resp.status_code == 204
    assert resp_body is None


def test_get_all(client: FlaskClient):
    rac = ResourceAPIClient(client)
    (resp, resp_body) = rac.get_all()
    assert resp.status_code == 200
    assert 'resources' in resp_body
    assert len(resp_body['resources']) == 0

    (resp, resp_body) = rac.create(owner='MrMat', name='Test Resource')
    assert resp.status_code == 201
    assert resp_body['id'] >= 0

    (resp, resp_body) = rac.get_all()
    assert resp.status_code == 200
    assert len(resp_body['resources']) == 1


def test_get_one(client: FlaskClient):
    rac = ResourceAPIClient(client)
    (resp, resp_body) = rac.get_one(1)
    assert resp.status_code == 404
    assert resp_body is None

    (resp, resp_body) = rac.create(owner='MrMat', name='Test Resource')
    assert resp.status_code == 201
    assert resp_body['id'] == 1

    (resp, resp_body) = rac.get_one(1)
    assert resp.status_code == 200
    assert resp_body['id'] == 1
    assert resp_body['owner'] == 'MrMat'
    assert resp_body['name'] == 'Test Resource'

