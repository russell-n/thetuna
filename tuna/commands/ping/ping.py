
# python standard library
import re
import time

# this package
from tuna import BaseClass, TunaError
from tuna.clients.clientbase import handlesocketerrors
from tuna.commands.command.command import TheCommand


class Ping(BaseClass):
    """
    A class to ping a target
    """
    def __init__(self, connection, target, time_limit=300, threshold=5, arguments=None, operating_system=None,
                 timeout=1, data_expression=None, trap_errors=False):
        """
        Ping constructor

        :param:

         - `connection`: A paramiko SSHClient like connection to send ping commands to
         - `target`: IP address to ping
         - `time_limit`: seconds to try to ping
         - `threshold`: number of consecutive pings needed for a success
         - `operating_system`: OS of the device (to change the parameters and expected output)
         - `timeout`: seconds to allow the socket to try and read
         - `data_expression`: regular expression to match successful ping
         - `trap_errors`: If True, logs socket errors but doesn't raise exceptions
        """
        super(Ping, self).__init__()
        self.connection = connection
        self.target = target
        self.time_limit = time_limit
        self.timeout = timeout
        self.threshold = threshold
        self._command = None
        self._arguments = arguments
        self._arguments_target = None
        self._operating_system = operating_system
        self._data_expression = data_expression
        self.trap_errors = trap_errors
        return

    @property
    def data_expression(self):
        """
        A regular expression to match the successful ping
        """
        if self._data_expression is None:
            self._data_expression = PingConstants.rtt_expression
        return self._data_expression

    @property
    def arguments(self):
        """
        The arguments for the ping command, if not passed in, uses OS to guess
        """
        if self._arguments is None:
            if self.operating_system == PingConstants.cygwin:
                self._arguments = PingConstants.cygwin_one_repetition
            elif self.operating_system == PingConstants.linux:
                self._arguments = PingConstants.linux_one_repetition
            else:
                self.check_rep()
        return self._arguments

    @property
    def arguments_target(self):
        """
        adds the target to the arguments

        Because of the way the AutomatedRVR is building things the target is unknown until runtime
        but the arguments are set at build time
        """
        if self._arguments_target is None:
            if self.target is None or self.arguments.endswith(self.target):
                self.logger.warning("target ({0}) and arguments should be set as separate parameters".format(self.target))
            self._arguments_target = "{0} {1}".format(self.arguments,
                                                      self.target)
        return self._arguments_target

    @property
    def command(self):
        """
        The ping command to send to the device

        :return: string ping command
        """
        if self._command is None:
            self._command = TheCommand(connection=self.connection,
                                       command=PingConstants.command,
                                       data_expression=self.data_expression,
                                       arguments=self.arguments_target,
                                       identifier=PingConstants.command,
                                       timeout=self.timeout,
                                       trap_errors=self.trap_errors)
        return self._command
                            
    @property
    @handlesocketerrors
    def operating_system(self):
        """
        If this isn't set, tries to use `uname` to discover the operating system
        
        :return: string representing the operating system        
        """
        if self._operating_system is None:
            # I don't like this, but it was the way the old code was doing it
            stdin, stdout, stderr = self.connection.exec_command('uname', timeout=1)
            
            self._operating_system = stdout.readline().rstrip().lower()
            if self._operating_system not in PingConstants.known_operating_systems:
                raise TunaError("unknown operating-system: {0}".format(self._operating_system))
            self.logger.info("Setting Operating System to: '{0}'".format(self._operating_system))
            
            for line in stderr:
                try:
                    self.logger.error(line)
                    if len(line):
                        raise TunaError("Error getting operating system, try adding it to the config file instead")
                except socket.timeout:
                    # I don't know if this is a fatal error or not
                    self.logger.warning("socket timed out reading from standard error after 'uname' command")                    
        return self._operating_system

    def __call__(self):
        """
        tries to ping the target until the threshold of successes is reached
        """
        stop_time = time.time() + self.timeout
        successes = 0

        while time.time() < stop_time:
            match = self.command()
            if match:
                successes += 1
                self.logger.info("{d} pinged target ({t}) -- {s} out of {total} rtt: {r} ms".format(t=self.target,
                                                                                                    d=self.connection.test_interface,
                                                                                                    s=successes,
                                                                                                    total=self.threshold,
                                                                                                    r=match))
                
            if successes == self.threshold:
                return True
            if match is None:
                self.logger.info("Failed ping attempt, setting successes to 0")
                successes = 0
        return False

    def check_rep(self):
        """
        Does a check of parameters

        :raise: TunaError on error
        """
        if self.operating_system not in PingConstants.known_operating_systems:
            raise TunaError("Unknown Operating System: {0} (known: {1})".format(self.operating_system,
                                                                                      ','.join(PingConstants.known_operating_systems)))
        return

    def reset(self):
        """
        Resets all of the values

        Because of the circular nature of some of the settings (arguments_target relies on arguments,
        arguments might rely on operating_system (or might be set by user)), there's no one trigger
        to reset the arguments. This should only be used to wipe the settings clean so it can be restarted
        """
        self._arguments = None
        self._operating_system = None
        self._arguments_target = None
        self._command = None
        self._data_expression = None
        return

        
# end class Ping    


class PingConstants(object):
    """
    Ping constants (so other modules can reference them)
    """
    __slots__ = ()
    command = 'ping'
    linux = 'linux'
    cygwin = 'cygwin'
    known_operating_systems = (linux, cygwin)

    # there's another set of code that says cygwin uses:
    # ' -n  1 -w 500'
    # this should be checked
    cygwin_one_repetition = '-n 1'
    linux_one_repetition  = '-c 1 -W 1'

    round_trip_time = 'rtt'

    # regular expressions
    # the cygwin needs to be confirmed
    cygwin_rtt_expression = 'time.(\d+)ms'
    rtt_expression = 'time\s*=\s*(?P<{0}>[\d.]+)\sms'.format(round_trip_time)
# end class PingConstants    
