class Response:
    """Util class for standardize response schema"""

    REQUEST_FAILED = "Request failed, try again later."
    BODY_EMPTY = "Request body is empty."
    ALREADY_EXISTS = "{} already exists."
    NOT_FOUND = "{} not found."

    @staticmethod
    def success(data: list or dict, code: int = 200) -> (dict, int):
        return {'data': data}, code

    @staticmethod
    def error(errors: dict, code: int = 500) -> (dict, int):
        return {'errors': errors}, code
