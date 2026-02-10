class AppException(Exception):

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"{self.__class__.__name__} error occuried with message: {self.msg}"

class AuthException(AppException):
    pass

