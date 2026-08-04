from marshmallow import ValidationError

from utils.errors import APIError


def validate_payload(schema, data):
    """Runs schema.load(data), raising APIError(400) with field-level details on failure."""
    try:
        return schema.load(data or {})
    except ValidationError as err:
        raise APIError("Validation failed", status_code=400, details=err.messages)
