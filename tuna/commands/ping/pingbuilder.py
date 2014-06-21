
# this package
from tuna.commands.ping.ping import Ping
from tuna import BaseClass


class PingBuilder(BaseClass):
    """
    A builder of pings
    """
    def __init__(self, connection, configuration):
        """
        PingBuilder Constructor

        :param:

         - `connection`: connection to the device that will send pings
         - `configuration`: a PingConfiguration
        """
        super(PingBuilder, self).__init__()
        self.connection = connection
        self.configuration = configuration
        self._product = None
        return

    @property
    def product(self):
        """
        A built Ping instance
        """
        if self._product is None:
            self.logger.debug("Building the ping with '{0}' and '{1}'".format(self.connection,
                                                                              self.configuration))
            self._product = Ping(connection=self.connection,
                                 target=self.configuration.target,
                                 time_limit=self.configuration.time_limit,
                                 timeout=self.configuration.timeout,
                                 threshold=self.configuration.threshold,
                                 operating_system=self.configuration.operating_system,
                                 arguments=self.configuration.arguments,
                                 data_expression=self.configuration.data_expression,
                                 trap_errors=self.configuration.trap_errors)
        return self._product
# end class PingBuilder        
