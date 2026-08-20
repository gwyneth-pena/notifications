class APIException(Exception):
    """Base generic exception for handling structured API errors."""
    def __init__(
            self, 
            msg: str, 
            location: str = "body", 
            field: str = "", 
            type_: str = "value_error", 
            status_code: int = 422
        ):
            self.msg = msg
            self.location = location
            self.field = field
            self.type_ = type_
            self.status_code = status_code
            super().__init__(self.msg)