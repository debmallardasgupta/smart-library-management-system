from marshmallow import Schema, fields, validate


class BookCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    isbn = fields.Str(required=False, allow_none=True, validate=validate.Length(max=20))
    genre = fields.Str(required=False, allow_none=True, validate=validate.Length(max=100))
    total_copies = fields.Int(required=False, load_default=1, validate=validate.Range(min=1))


class BookUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    author = fields.Str(validate=validate.Length(min=1, max=150))
    isbn = fields.Str(allow_none=True, validate=validate.Length(max=20))
    genre = fields.Str(allow_none=True, validate=validate.Length(max=100))
    total_copies = fields.Int(validate=validate.Range(min=1))
    available_copies = fields.Int(validate=validate.Range(min=0))


book_create_schema = BookCreateSchema()
book_update_schema = BookUpdateSchema(partial=True)
