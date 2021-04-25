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

from flask import Blueprint, request

from mrmat_python_api_flask import db
from mrmat_python_api_flask.db.resource import Resource

bp = Blueprint('resource_v1', __name__)


@bp.route('/', methods=['GET'])
def get_all():
    all = Resource.query.all()
    return all, 200


@bp.route('/<i>', methods=['GET'])
def get_one(i: int):
    resource = Resource.query.filter(Resource.id == i)
    if resource is None:
        return {'status': 404, 'message': f'Unable to find entry with identifier {i} in database'}, 404
    return resource, 200


@bp.route('/', methods=['POST'])
def create():
    json = request.get_json()
    resource = Resource(owner=json['owner'], name=json['name'])
    db.session.add(resource)
    db.session.commit()
    return resource, 201


@bp.route('/<i>', methods=['PUT'])
def modify(i: int):
    json = request.get_json()
    resource = Resource.query.filter(Resource.id == i)
    if resource is None:
        return {'status': 404, 'message': f'Unable to find entry with identifier {i} in database'}, 404
    resource.owner = json['owner']
    resource.name = json['name']
    db.session.add(resource)
    db.session.commit()
    return resource, 200


@bp.route('/<i>', methods=['DELETE'])
def remove(i: int):
    resource = Resource.query.filter(Resource.id == i)
    if resource is None:
        return {'status': 404, 'message': f'Unable to find entry with identifier {i} in database'}, 404
    db.session.delete(resource)
    db.session.commit()
    return {}, 204
