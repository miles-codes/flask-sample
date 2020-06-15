from marshmallow import Schema, fields


class IsoTimeField(fields.DateTime):
    def __init__(self, **kwargs):
        kwargs = dict([(k, v) for k, v in kwargs.items() if k != 'format'])
        super().__init__(format='iso', **kwargs)

    def _serialize(self, value, attr, obj):
        if value and hasattr(value, 'microsecond'):
            value = value.replace(microsecond=0)

        return super()._serialize(value, attr, obj)




class BaseSchema(Schema):
    id = fields.Integer(allow_none=True, default=None)
    created_at = IsoTimeField(dump_only=True)
    updated_at = IsoTimeField(dump_only=True)
