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

"""Resource API SQLAlchemy model
"""

from sqlalchemy import Column, Integer, String
from marshmallow import fields

from mrmat_python_api_flask import db, ma


class Resource(db.Model):
    __tablename__ = 'resources'
    id = Column(Integer, primary_key=True)
    owner = Column(String(50))
    # TODO: Should have unique constraint on name
    name = Column(String(50))

    def __init__(self, owner=None, name=None):
        self.owner = owner
        self.name = name


class ResourceSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'owner', 'name')

    id = fields.Int()
    name = fields.Str()
    owner = fields.Str()


resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)
