from marshmallow import (
    Schema, fields, post_load, pre_dump, validate, validates
)
from ostruct import OpenStruct

from ..lib import inverted
from ..models import User
from .base_view import BaseSchema


class UserStatusSchema(Schema):
    DEFAULT_OBJ = OpenStruct(id=User.STATUSES['active'], name='active')
    id = fields.Integer(
        many=False, required=False, allow_none=True,
        default=DEFAULT_OBJ.id, missing=DEFAULT_OBJ.id,
        validate=[validate.OneOf(User.STATUSES.values())]
    )
    name = fields.String(
        required=False, allow_none=True,
        default=DEFAULT_OBJ.name, missing=DEFAULT_OBJ.name
    )


class UserRoleSchema(Schema):
    DEFAULT_OBJ = OpenStruct(id=User.ROLES['user'], name='user')
    id = fields.Integer(
        many=False, required=False, allow_none=True,
        default=DEFAULT_OBJ.id, missing=DEFAULT_OBJ.id,
        validate=[validate.OneOf(User.ROLES.values())]
    )
    name = fields.String(
        required=False, allow_none=True,
        default=DEFAULT_OBJ.name, missing=DEFAULT_OBJ.name
    )


class UserSchema(BaseSchema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=False, load_only=True)

    role_obj = fields.Nested(
        UserRoleSchema, required=False,
        load_from='role', dump_to='role',
        default=UserRoleSchema.DEFAULT_OBJ,
        missing=UserRoleSchema.DEFAULT_OBJ
    )
    status_obj = fields.Nested(
        UserStatusSchema, required=False,
        load_from='status', dump_to='status',
        default=UserStatusSchema.DEFAULT_OBJ,
        missing=UserStatusSchema.DEFAULT_OBJ
    )

    @pre_dump
    def wrap_relations(self, obj, many=False):
        obj.status_obj = OpenStruct()
        obj.status_obj.id = obj.status
        obj.status_obj.name = inverted(User.STATUSES)[obj.status]

        obj.role_obj = OpenStruct()
        obj.role_obj.id = obj.role
        obj.role_obj.name = inverted(User.ROLES)[obj.role]

    @post_load
    def unwrap_relations(self, data, many=False):
        if 'role_obj' in data:
            data['role'] = data['role_obj']['id']
            del data['role_obj']

        if 'status_obj' in data:
            data['status'] = data['status_obj']['id']
            del data['status_obj']
