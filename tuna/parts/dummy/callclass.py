
# this package
from tuna import BaseClass
from tuna import ARGS, KWARGS


class CallClassConstants(object):
    """
    Some constants so the expected strings are explicitly defined somewhere
    """
    __slots__ = ()
    debug_level = 'debug'
    info_level = 'info'


class CallClass(BaseClass):
    """
    A class for dummies to return when called.
    """
    def __init__(self, message=None, payload=None,
                 level=CallClassConstants.info_level):
        """
        CallClass constructor

        :param:

         - `message`: string to return from __str__
         - `payload`: payload to return on call
         - `level`: logging level to use
        """
        super(CallClass, self).__init__()
        if message is None:
            message = 'call'
        self.message = message

        self.payload = payload
        self.level = level
        self._log_arguments = None
        return

    @property
    def log_arguments(self):
        """
        logger.Logging method 
        """
        if self._log_arguments is None:
            if self.level == CallClassConstants.info_level:
                self._log_arguments = self.logger.info
            else:
                self._log_arguments = self.logger.debug
        return self._log_arguments

    def __call__(self, *args, **kwargs):
        """
        returns the payload after logging items
        """
        self.log_arguments(ARGS.format(value=args))
        self.log_arguments(KWARGS.format(value=kwargs))
        return self.payload

    def __str__(self):
        """
        Returns the name given
        """
        return self.message
