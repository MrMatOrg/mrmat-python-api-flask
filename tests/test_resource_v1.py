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

from flask import Response
from flask.testing import FlaskClient
from typing import Dict


def test_create(client: FlaskClient):
    resource_entry: Dict = {'owner': 'MrMat', 'name': 'Test Resource 1'}
    rv: Response = client.post('/api/resource/v1/', json=resource_entry)
    assert rv.status_code == 201
    json_body: Dict = rv.get_json()
    assert json_body['id'] == 1
    for key in ['owner', 'name']:
        assert json_body[key] == resource_entry[key]


def test_get_all(client: FlaskClient):
    # TODO: We're starting off with an empty database
    rv: Response = client.get('/api/resource/v1/')
    assert rv.status_code == 200
    json_body = rv.get_json()
    assert 'resources' in json_body
    assert len(json_body['resources']) == 0


def test_get_one(client: FlaskClient):
    # TODO: We're starting off with an empty database
    rv: Response = client.get('/api/resource/v1/1')
    assert rv.status_code == 404
    json_body = rv.get_json()
    assert json_body is None
