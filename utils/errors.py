class APIError(Exception):
    """Raised anywhere in the app to produce a consistent JSON error response.

    status_code: the HTTP status to respond with
    message: human-readable summary (goes in the "error" field, same as before)
    details: optional dict of extra info, e.g. field-level validation errors
    """

    def __init__(self, message, status_code=400, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details

    def to_dict(self):
        body = {"error": self.message}
        if self.details:
            body["details"] = self.details
        return body
