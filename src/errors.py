class BaseError(Exception):
    """Base Error Class"""
    def __init__(self, statusCode=400, title=None, message=None, fields=None):
        Exception.__init__(self)
        self.statusCode = statusCode
        self.title = title
        self.message = message
        self.fields = fields

    def to_dict(self):
        return {'statusCode': self.statusCode,
                'title': self.title,
                'message': self.message,
                'fields': self.fields}


class FieldError(BaseError):
    def __init__(self, fields):
        BaseError.__init__(self)
        self.statusCode = 400
        self.message = 'One or more data fields are incorrect'
        self.title = 'FieldError'
        self.fields = fields


class ServerError(BaseError):
    def __init__(self, message='Internal server error'):
        BaseError.__init__(self)
        self.statusCode = 400
        self.message = 'The browser (or proxy) sent a request that this server could not understand.'
        self.title = 'Bad request'
        self.fields = None


class FaceEncodingFail(BaseError):
    def __init__(self, message='Bad Photo'):
        BaseError.__init__(self)
        self.message = message
        self.title = 'Bad request'
        self.fields = None
