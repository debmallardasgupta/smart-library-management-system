from marshmallow import Schema, fields, validate


class BorrowSchema(Schema):
    book_id = fields.Int(required=True, validate=validate.Range(min=1))


borrow_schema = BorrowSchema()
