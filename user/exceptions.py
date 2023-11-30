from rest_framework.exceptions import APIException

class CustomAPIException(APIException):

    def __init__(self, name, detail, code=400):
        self.detail = detail
        self.status_code = code
        self.__class__.__name__ = name

class SomethingWentWrong(APIException):
    status_code = 400
    default_detail = "Something went wrong."

class AccountAlreadyExists(APIException):
    status_code = 409
    default_detail = "An account with the specified email address already exists."


class IncorrectCredentials(APIException):
    status_code = 400
    default_detail = "The provided credentials are incorrect."
