class PywhoisError(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg)
        self.args = args
        self.kwargs = kwargs


# Propose aiming to use these if possible
# Currently not used at all
class PywhoisDomainNotFound(PywhoisError):
    """When text matching suggests the domain does not exist"""


class PywhoisRateLimited(PywhoisError):
    """When text matching suggests the client has been rate-limited"""


class PywhoisNetworkFailure(PywhoisError):
    """Connection refused, closed prematurely and similar"""
