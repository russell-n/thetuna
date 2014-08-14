
# python standard library
import time
import textwrap
from threading import RLock

# this package
from tuna.clients.simpleclient import SimpleClient
from tuna.clients.telnetclient import TelnetClient
from tuna import BaseClass, TunaError
from tuna.infrastructure.baseconfiguration import BaseConfiguration


class HostEnum(object):
    """
    A holder of Host constants
    """
    __slots__ = ()

    # options  
    control_ip = 'control_ip'
    password = 'password'
    connection_type = 'connection_type'
    test_ip = 'test_ip'
    username = 'username'
    port = 'port'
    timeout = 'timeout'
    prefix = 'prefix'
    operating_system = 'operating_system'
    telnet = 'telnet'
    prefix_command = '{p} {c}'
    
    options = (control_ip, password, connection_type, test_ip, username,
               port, timeout, prefix, operating_system)
    # defaults
    default_port = 22
    default_type = 'ssh'
    default_timeout = 1
    default_operating_system = 'linux'
    
# end HostEnum    


class TheHost(BaseClass):
    """
    The main host used to build the other hosts
    """
    def __init__(self, hostname, test_interface, username=None, timeout=1, prefix=None, 
                 operating_system='linux', connection_type=HostEnum.default_type,
                 **kwargs):
        """
        TheHost Constructor

        :param:

         - `hostname`: hostname to connect to the device
         - `test_interface`: the address of the interface to send test-traffic to (over)
         - `username`: login name
         - `timeout`: timeout for reading from the connection
         - `prefix`: string to add to every command sent to the connection
         - `operating_system`: os to help commands predict syntax
         - `connection_type`: Identifier for the connection (see HostEnum)
         - `kwargs`: extra parameters for connections other than the SimpleClient
        """
        super(TheHost, self).__init__()
        self.hostname = hostname
        self.test_interface = test_interface
        self.username = username
        self.timeout = timeout
        self.prefix = prefix
        self.operating_system = operating_system
        self.connection_type = connection_type
        self.kwargs = kwargs

        # properties
        self._client = None
        self._client_constructors = None
        self._lock = None

        # backward compatibility
        self.ControlInterface = hostname
        self.TestInterface = test_interface
        self.testInterface = test_interface
        return

    @property
    def lock(self):
        """
        A re-entrant lock to protect the exec-command calls
        """
        if self._lock is None:
            self._lock = RLock()
        return self._lock

    @property
    def client(self):
        """
        A built client (connection)
        """
        if self._client is None:
            self._client = self.client_constructors[self.connection_type](hostname=self.hostname,
                                                                          username=self.username,
                                                                          timeout=self.timeout,
                                                                          **self.kwargs)
        return self._client

    @property
    def client_constructors(self):
        """
        A collection of Client class constructors

        :return: dict of type:class definition objects
        """
        if self._client_constructors is None:
            self._client_constructors = dict(zip((HostEnum.default_type, HostEnum.telnet),
                                                 (SimpleClient, TelnetClient)))
        return self._client_constructors

    def exec_command(self, command, timeout=1):
        """
        Calls the Clients's non-blocking run to execute `prefix command`.

        :param:

         - `command`: string to send to the ssh-client
         - `timeout`: Timeout for reading from the socket (set to None for output that will be empty for a while)

        :rtype: Tuple
        :return: Stdin, Stdout, Stderr
        """
        if self.prefix is not None:
            command = HostEnum.prefix_command.format(p=self.prefix,
                                                          c=command)
        with self.lock:
            return self.client.exec_command(command,
                                        timeout=timeout)
            
    def close(self):
        """
        Closes the client and sets it to None
        """
        if self._client is not None:
            # so it doesn't create it by mistake
            self.client.close()
            self._client = None
        return

    def kill_all(self, process):
        """
        Kills all the process instances on the remote client. 

        :postcondition: kill command on all process id's that match 'process' string on remote host.
        :raise: TunaError if couldn't kill process
        """
        stdin, stdout, stderr = self.exec_command("ps -e | grep {0}".format(process))
        
        for line in stdout:
            self.logger.debug(line)
            if process in line and 'grep' not in line:
                process_id = line.lstrip().split()[0]
                command = 'kill -9 {0}'.format(process_id)
                self.logger.debug(command)
                stdin_2, stdout_2, stderr_2 = self.exec_command(command)
                self.check_stderr(stderr_2)
            elif 'Operation not permitted' in line:
                self.logger.error(line)
                raise TunaError("Unable to kill process '{0}' on {1}".format(process,
                                                                                   self.client))
        self.check_stderr(stderr)
        stdin, stdout, stderr = self.exec_command("ps -e | grep {0}".format(process))
        for line in stdout:
            self.logger.debug(line)
            if process in line and 'grep' not in line:
                self.logger.error(line)                
                raise TunaError("Unable to kill process '{0}' on '{1}'".format(process,
                                                                                     self.client))
        self.check_stderr(stderr)
        return

    def check_stderr(self, stderr):
        """
        helper code to check if stderr is empty
        """
        for line in stderr:
            if len(line):
                self.logger.error(line)
                if "Operation not permitted" in line:
                    raise TunaError("Insufficient privileges to kill on {0}".format(self.client))
        return


    def __str__(self):
        """
        string of settings
        """
        return "Host -- OS: {0} Prefix: {1} Client -- {2}".format(self.operating_system,
                                                               self.prefix,
                                                               self.client)

# end class TheHost    


class HostConfiguration(BaseConfiguration):
    """
    A holder of device-configurations
    """
    def __init__(self, section, *args, **kwargs):
        """
        HostConfiguration constructor

        :param:

         - `configuration`: Built Configuration Adapter
         - `section`: The [<section>] name (e.g. 'server')
        """
        super(HostConfiguration, self).__init__(*args, **kwargs)
        self._section = section
        self.logger.debug("using section: [{0}]".format(self.section))

        # properties
        self._control_ip = None
        self._password = None
        self._connection_type = None
        self._test_ip = None
        self._username = None
        self._timeout = None
        self._prefix = None
        self._operating_system = None
        self._kwargs = None
        return

    @property
    def example(self):
        """
        an example device configuration
        """
        if self._example is None:
            self._example = textwrap.dedent("""
            [{section}]
            # login information (these are required)
            username = admin

            # this isn't if your public keys are working
            #password = root
            
            # address of the control-interface 
            control_ip = 192.168.10.34

            # this identifies the type (only 'telnet' or 'ssh')
            #connection_type = {connection_type}

            # address of the interface to test
            test_ip = 192.168.20.34

            # connection time-out in seconds
            #timeout = {timeout}

            # optional prefix to add to ALL commands (default: None)
            # this will be added with a space (i.e. <prefix> <command>)
            # so if needed, add a semicolon like in the example between the PATH and adb
            
            #prefix = PATH=/opt:$PATH; adb shell

            # the operating system for the DUT
            # just cygwin and linux initially

            # operating_system = {operating_system}

            # there are too many options for the different connection-types
            # so you can add necessary parameters but make sure the name
            # matcheds the parameter name
            # e.g. if you need to set the port:
            # port=52686
            """.format(section=self.section,
                       connection_type=HostEnum.default_type,
                       timeout=HostEnum.default_timeout,
                       operating_system=HostEnum.default_operating_system))
        return self._example

    @property
    def section(self):
        """
        The section name in the configuration file
        """
        return self._section

    @property
    def control_ip(self):
        """
        The optional hostname for the device (default=None)
        """
        if self._control_ip is None:
            self._control_ip = self.configuration.get(section=self.section,
                                                       option=HostEnum.control_ip,
                                                       optional=True)
        return self._control_ip

    @property
    def password(self):
        """
        The optional password for the device (default=None)
        """
        if self._password is None:
            self._password = self.configuration.get(section=self.section,
                                                    option=HostEnum.password,
                                                    optional=True)
        return self._password

    @property
    def connection_type(self):
        """
        One of 'ssh' or'telnet'

        """
        if self._connection_type is None:
            self._connection_type = self.configuration.get(section=self.section,
                                                         option=HostEnum.connection_type,
                                                         optional=True,
                                                         default=HostEnum.default_type)
        return self._connection_type

    @property
    def test_ip(self):
        """
        Gets the hostname for the test interface (not optional)

        :raise: ConfigParser.NoOptionError if option not in configuration
        """
        if self._test_ip is None:
            self._test_ip = self.configuration.get(section=self.section,
                                                   option=HostEnum.test_ip)
        return self._test_ip
    
    @property
    def prefix(self):
        """
        Gets a prefix string to add to each command sent to the DUT
        """
        if self._prefix is None:
            self._prefix = self.configuration.get(section=self.section,
                                                  option=HostEnum.prefix,
                                                  optional=True)
        return self._prefix
    
    @property
    def timeout(self):
        """
        Gets the timeout for connections (e.g. reading from stdout)

        :rtype: Float
        :return: Seconds to wait for output before timing-out
        """
        if self._timeout is None:
            self._timeout = self.configuration.getfloat(section=self.section,
                                                        option=HostEnum.timeout,
                                                        optional=True,
                                                        default=1)
        return self._timeout
    
    @property
    def username(self):
        """
        Gets the login username for the device

        :raise: ConfigParser.NoOptionError if option not in configuration
        """
        if self._username is None:
            self._username = self.configuration.get(section=self.section,
                                                    option=HostEnum.username)
        return self._username

    @property
    def operating_system(self):
        """
        Gets the operating system if the user set it
        """
        if self._operating_system is None:
            self._operating_system = self.configuration.get(section=self.section,
                                                            option=HostEnum.operating_system,
                                                            optional=True,
                                                            default=HostEnum.default_operating_system)
        return self._operating_system

    @property
    def kwargs(self):
        """
        dictionary of options not in this class
        """
        if self._kwargs is None:
            exclude = self.configuration.defaults.keys()
            exclude.extend(HostEnum.options)
            options = [option for option in self.configuration.options(self.section) if option not in exclude]
            values = [self.configuration.get(self.section, option) for option in options]
            self._kwargs = dict(zip(options, values))
        return self._kwargs
    
    def reset(self):
        """
        Sets the properties to None
        """
        self._operating_system = None
        self._prefix = None
        self._timeout = None
        self._port = None
        self._control_ip = None
        self._password = None
        self._connection_type = None
        self._test_ip = None
        self._username = None
        return

    def check_rep(self):
        """
        Checks if the parameters seem reasonable

        :raise: AssertionError if something seems wrong
        """
        super(HostConfiguration, self).check_rep()
        if self.timeout is not None:
            # a timeout of 0 or less will timeout before you can get output
            assert self.timeout > 0, "Timeout must be greater than 0, not {0}".format(self.timeout)
        if self.connection_type in "ssh telnet".split():
            assert self.control_ip is not None, "If not using serial, the control_ip needs to be set"
        return
# end class HostConfiguration    
