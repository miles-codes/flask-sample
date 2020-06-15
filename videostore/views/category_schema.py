from marshmallow import (
    Schema, fields, post_load, pre_dump, validate, validates
)

from .base_view import BaseSchema


class CategorySchema(BaseSchema):
    name = fields.String(required=True)
