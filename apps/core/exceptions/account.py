__author__ = 'phillip'


class NoPermissionToLogWithCompany(Exception):
    pass

class CompanyHasNoUserAssociated(Exception):
    pass

class NotAllowedToRelogin(Exception):
    pass

class UserIdDoesNotRemainsInSession(Exception):
    pass