__author__ = 'phillip'

class AccountException(Exception):
    pass

class AccountDoesNotExistException(AccountException):
    pass

class TokenIsNoLongerValidException(AccountException):
    pass

class TokenIsNotActiveException(AccountException):
    pass

class TokenDoesNotExistException(AccountException):
    pass