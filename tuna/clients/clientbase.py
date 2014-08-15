
# python standard library
from abc import abstractproperty, abstractmethod
import socket
import threading

# this package
from tuna import BaseClass, TunaError


COMMA = ','
TIMEOUT = 10


class BaseClient(BaseClass):
    """
    A base class for clients.
    """
    def __init__(self, hostname, username=None, port=None, lock=None,
                 timeout=TIMEOUT, **kwargs):
        """
        Constructor

        :param:

         - `hostname`: ip address or resolvable hostname.
         - `username`: the login name.
         - `timeout`: Time to give the client to connect
         - `port`: TCP port of the server
         - `kwargs`: anything else that the client can use will be passed in to it
         - `lock`: re-entrant lock to block calls
        """
        super(BaseClient, self).__init__()
        self._logger = None
        self.hostname = hostname
        self.username = username
        self.timeout = timeout
        self._client = None
        self.port = port
        self.kwargs = kwargs
        self._lock = None
        return

    @abstractproperty
    def client(self):
        """
        The actual client to the device
        """
        return

    @abstractmethod
    def exec_command(self, command, timeout=TIMEOUT):
        """
        The main interface with the client

        :param:

         - `command`: A string to send to the client.
         - `timeout`: Set non-blocking timeout.

        :rtype: tuple
        :return: stdin, stdout, stderr

        :raise: TunaError for client exceptions
        """
        return

    @property
    def lock(self):
        """
        Re-entrant lock so users can use it in threads
        """
        if self._lock is None:
            self._lock = threading.RLock()
        return self._lock
        
    def close(self):
        """
        Closes and removes the client (if it exists)
        
        :postcondition: client's connection is closed and self._client is None                
        """
        if self._client is not None:
            self._client.close()
            self._client = None
        return
    
    def __str__(self):
        """
        creates the string representation
        :return: username, hostname, port, password in string
        """
        user = "Username: {0}".format(self.username)
        host = "Hostname: {0}".format(self.hostname)
        port = "Port: {0}".format(self.port)
        if hasattr(self, 'password'):
            output = [user, host, port, "Password: {0}".format(self.password)]
        elif 'password' in self.kwargs:
            output = [user, host, port, "Password: {0}".format(self.kwargs['password'])]
        else:
            output = [user, host, port]
        return COMMA.join(output)

    def __getattr__(self, method):
        """
        A pass-through to the client for un-implemented methods.

        .. warning:: This can't go in the base-class
        """
        return getattr(self.client, method)
# end BaseClient


def handlesocketerrors(method,  *args, **kwargs):
    """
    function to use as a method decorator (expects ``self`` as one of the arguments)

    Also expects that the object has connection and logger attributes

    :param:

     - `method`: method instance
    """
    def wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except socket.error as error:
            message = "{e}: Error with connection to {c}".format(c=self.connection,
                                                                 e=type(error))
            self.logger.error(message)
            raise TunaError(message)
    return wrapped


def suppresssocketerrors(method,  *args, **kwargs):
    """
    Unlike handlesocketerrors this logs the error and quits (no exception raised)
    function to use as a method decorator (expects ``self`` as one of the arguments)

    Also expects that the object has connection and logger attributes

    :param:

     - `method`: method instance
    """
    def wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except socket.error as error:
            message = "{e}: Error with connection to {c}".format(c=self.connection,
                                                                 e=type(error))
            self.logger.error(message)
    return wrapped
