from marshmallow import (
    Schema, fields, post_load, pre_dump, validate, validates
)

from .base_view import BaseSchema
from .category_schema import CategorySchema


class MovieSchema(BaseSchema):
    title = fields.String(required=True)
    category = fields.Nested(CategorySchema)
