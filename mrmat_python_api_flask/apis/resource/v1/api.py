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

from werkzeug.local import LocalProxy
from flask import Blueprint, request, g, current_app
from marshmallow import ValidationError

from mrmat_python_api_flask import db, oidc
from .model import Resource, resource_schema, resources_schema

bp = Blueprint('resource_v1', __name__)
logger = LocalProxy(lambda: current_app.logger)


@bp.route('/', methods=['GET'])
@oidc.accept_token(require_token=True)
def get_all():
    logger.error('Error')
    logger.warning('Warning')
    logger.info('Info')
    logger.debug(f'Called by {g.oidc_token_info["sub"]}')
    a = Resource.query.all()
    return {'resources': resources_schema.dump(a)}, 200


@bp.route('/<i>', methods=['GET'])
@oidc.accept_token(require_token=True)
def get_one(i: int):
    resource = Resource.query.filter(Resource.id == i).first_or_404()
    if resource is None:
        return {'status': 404, 'message': f'Unable to find entry with identifier {i} in database'}, 404
    return resource_schema.dump(resource), 200


@bp.route('/', methods=['POST'])
@oidc.accept_token(require_token=True)
def create():
    try:
        json_body = request.get_json()
        if not json_body:
            return {'message': 'No input data provided'}, 400
        body = resource_schema.load(request.get_json())
    except ValidationError as ve:
        return ve.messages, 422
    resource = Resource(owner=body['owner'], name=body['name'])
    db.session.add(resource)
    db.session.commit()
    return resource_schema.dump(resource), 201


@bp.route('/<i>', methods=['PUT'])
@oidc.accept_token(require_token=True)
def modify(i: int):
    body = resource_schema.load(request.get_json())
    resource = Resource.query.filter(Resource.id == i).one()
    if resource is None:
        return {'status': 404, 'message': 'Unable to find requested resource'}, 404
    resource.owner = body['owner']
    resource.name = body['name']
    db.session.add(resource)
    db.session.commit()
    return resource_schema.dump(resource), 200


@bp.route('/<i>', methods=['DELETE'])
@oidc.accept_token(require_token=True)
def remove(i: int):
    resource = Resource.query.filter(Resource.id == i).one()
    if resource is None:
        return {'status': 410, 'message': 'Unable to find requested resource'}, 410
    db.session.delete(resource)
    db.session.commit()
    return {}, 204
