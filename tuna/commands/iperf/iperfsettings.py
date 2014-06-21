
# python standard library
from types import IntType, FloatType, NoneType, StringType
import re
from abc import abstractproperty

# this package
from tuna import BaseClass, TunaError


STRING_START = '^'
STRING_END = '$'
SPACE = r'\s'
NOT_SPACE = r'\S'
DIGIT = r'\d'
ZERO_OR_MORE = '*'
ONE_OR_MORE = '+'
ZERO_OR_ONE = '?'
DOT = r'\.'
SPACES = SPACE + ZERO_OR_MORE
NOT_SPACES = NOT_SPACE + ONE_OR_MORE
DIGITS = DIGIT + ONE_OR_MORE
OPTIONAL_DIGITS = DIGIT + ZERO_OR_MORE
EMPTY_STRING = ''

class IperfConstants(object):
    """
    Holder of Iperf Constants
    """
    __slots__ = ()
    # directions
    down = 'downstream'
    up = 'upstream'
    
    port_lower_bound = 1024
    udp = 'udp'
    
    # validators
    number_types = (NoneType, IntType, FloatType)
    
    # options
    general_options = ("format", 'interval', 'len', 'print_mss', 'output',
                      'port', 'window', 'compatibility', 'mss', 'nodelay',
                      'version', 'IPv6Version', 'reportexclude', 'reportstyle')

    server_options = ('udp', 'daemon', 'single_udp')

    # expressions
    # match 'n[KM] (iperf seems to ignore the case)
    value_expression = re.compile(STRING_START + SPACES + DIGITS + DOT + ZERO_OR_ONE +
                                  OPTIONAL_DIGITS + '[kKmM]' + ZERO_OR_ONE + SPACES + STRING_END)
    no_whitespace_expression = re.compile(STRING_START + NOT_SPACES + STRING_END)
    reportexclude_expression = re.compile(STRING_START + '[cdmsvCDMSV]' + ONE_OR_MORE + STRING_END)


class IperfBaseSettings(BaseClass):
    """
    A base for the client and server settings to provide common methods
    """
    def __init__(self):
        """
        IperfBaseSettings constructor

        :param:

         - `attributes`: list of class attributes (used by the __str__)
         - `kwargs`: dict to build the IperfGeneralSettings
        """
        super(IperfBaseSettings, self).__init__()
        self._logger = None
        return


    def set_boolean(self, attribute, turn_on):
        """
        Set's attributes to empty string or None, based on `turn_on` value.

        Empty string is used to add flag to output string without adding a value.

        :param:

         - `attribute`: Name of this class' attribute: self.<attribute>
         - `turn_on`: Boolean which if True will set the attribute to empty string

        :postcondition: self.<attribute> is empty string or None
        """
        if turn_on:
            setattr(self, attribute, EMPTY_STRING)
        else:
            setattr(self, attribute, None)
        return

    def set_number(self, attribute, value, lower_bound=None, caster=int):
        """
        Sets the attribute to the value

        :param:

         - `attribute`: attribute of self to set (self.<attribute> = value)
         - `value`: value to set attribute to
         - `lower_bound`: lowest allowed value
         - `caster`: function to cast the value to a number if it's not one already

        :postcondition: self.<attribute> set to value
        :raises: TunaError if not a non-negative number
        """
        if type(value )in IperfConstants.number_types:
            setattr(self, attribute, value)
        else:
            try:
                setattr(self, attribute, caster(value))
            except ValueError as error:
                self.logger.error(error)
                raise TunaError("{0} must be number or castable to a {1}, not {2}".format(attribute.lstrip('_'), caster,
                                                                                                value))
        if (lower_bound is not None and
            getattr(self, attribute) < lower_bound and
            value is not None):
            raise TunaError("{0} must be greater than {1}, not {2}".format(attribute.lstrip("_"),
                                                                                 lower_bound,
                                                                                 value))
        self.logger.debug("{0} set to {1}".format(attribute, value))
        return

    def set_bytes(self, attribute, value):
        """
        Sets the attribute to the value

        :param:

         - `attribute`: Name of attribute to set (e.g. '_len' for self._len)
         - `value`: value to set the attribute to
        
        :postcondition: attribute set to value

        :raises: TunaError if value is a string and doesn't match the form 'n[KM]'
        """
        setattr(self, attribute, value)
        if (not (type(value) in IperfConstants.number_types) and
            not IperfConstants.value_expression.search(value)):
            raise TunaError("`{0}` must be of the form 'n[KM]', not {1}".format(attribute.lstrip("_"),
                                                                                      value))
        self.logger.debug("'{0}' set to {1}".format(attribute, getattr(self, attribute)))
        return    


class IperfGeneralConstants(object):
    """
    Holder of constants for the IperfGeneralSettings
    """
    __slots__ = ()
    valid_formats = 'bkmBKM'

    # attributes
    interval = '_interval'
    len = '_len'
    print_mss = '_print_mss'
    window = '_window'
    compatibility = '_compatibility'
    udp = '_udp'
    port = '_port'
    mss = '_mss'


class IperfGeneralSettings(IperfBaseSettings):
    """
    A holder of iperf settings common to both client and server
    """
    def __init__(self, format=None,
                 interval=None,
                 len=None,
                 print_mss=None,
                 output=None,
                 port=None,
                 window=None,
                 compatibility=None,
                 mss=None,
                 nodelay=None,
                 version=None,
                 IPv6Version=None,
                 reportexclude=None,
                 reportstyle=None):
        """
        IperfGeneralSettings constructor

        :param:

         - `format`: the output format [bkmKM]
         - `interval`: the reporting interval in seconds
         - `len`: the read/write buffer size `n[KM]`
         - `print_mss`: print TCP maximum segment size (pass in Boolean to turn on or off)
         - `output`: filename to save output to
         - `port`: server port
         - `window`: TCP window size 'n[KM]'
         - `compatibility`: flag to use with older iperf versions
         - `mss`: value to set for the TCP maximum segment size
         - `nodelay`: boolean to turn the flag on or off
         - `version`: boolean to turn the version flag on or off
         - `IPv6Version`: boolean to turn the IP v6 flag on or off
         - `reportexclude`: one of [CDMSV] to turn off Connection, Data, Multicast, Setting, or Server reporting
         - `reportstyle`: C or c to turn on csv output
        """
        super(IperfGeneralSettings, self).__init__()
        self._format = None
        self.format = format

        self._interval = None
        self.interval = interval

        self._len = None
        self.len = len

        self._print_mss = None
        self.print_mss = print_mss

        self._output = None
        self.output = output

        self._port = None
        self.port = port

        self._window = None
        self.window = window

        self._compatibility = None
        self.compatibility = compatibility

        self._mss = None
        self.mss = mss

        self._nodelay = None
        self.nodelay = nodelay

        self._version = None
        self.version = version

        self._IPv6Version = None
        self.IPv6Version = IPv6Version

        self._reportexclude = None
        self.reportexclude = reportexclude

        self._reportstyle = None
        self.reportstyle = reportstyle
        return

    @property
    def format(self):
        """
        String for the output reporting (bits, kilobits, etc.)
        """
        return self._format

    @format.setter
    def format(self, new_format):
        """
        sets self._format

        :param:

         - `new_format`: character string in {b, k, m, B, K, M}

        :raise: TunaError if format is unknown
        """
        self._format = new_format
        if new_format is not None and new_format not in IperfGeneralConstants.valid_formats:
            raise TunaError("Invalid Iperf Format : {f} needs to be one of {v}".format(f=new_format,
                                                                                             v=IperfGeneralConstants.valid_formats))
        self.logger.debug("format set to '{0}'".format(new_format))
        return

    @property
    def interval(self):
        """
        The interval between data reporting (in seconds)
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """
        Sets the interval attribute

        :param:

         - `interval`: non-negative number

        :raise: TunaError if not castable to non-negative number
        """
        self.set_number(IperfGeneralConstants.interval, interval, lower_bound=0)
        return

    @property
    def len(self):
        """
        length of the read/write buffer
        """
        return self._len

    @len.setter
    def len(self, new_len):
        """
        Sets the read-write buffer

        :raise: TunaError error of not a non-negative number or string of form n[KM]
        """
        self.set_bytes(IperfGeneralConstants.len, new_len)
        return

    @property
    def print_mss(self):
        """
        Flag to print the TCP maximum segment size at the end of the output
        """
        return self._print_mss

    @print_mss.setter
    def print_mss(self, turn_on):
        """
        turns on the print_mss option.

        :param:

         - `turn_on`: resolvable to False to turn off or resolvable to True to turn on
        """
        self.set_boolean(IperfGeneralConstants.print_mss, turn_on)
        return

    @property
    def output(self):
        """
        Flag to send output to a file
        """
        return self._output

    @output.setter
    def output(self, filename):
        """
        sets the output flag to save to the given filename

        :param:

         - `filename`: string for filename

        :raise: TunaError if filename has white-space
        """
        self._output = filename
        if not IperfConstants.no_whitespace_expression.search(str(filename)):
            raise TunaError("filename must be string of non-whitespace characters, not {0}".format(filename))
        self.logger.debug("output set to '{0}'".format(self._output))
        return

    @property
    def port(self):
        """
        The server port flag

        :return: '--port <port number>' or None
        """
        return self._port

    @port.setter
    def port(self, new_port):
        """
        Sets the port flag (I tested it and iperf accepts negative ports and floats (but drops the fractional part))

        :param:

         - `new_port`: integer (or string castable to integer) or None

        :raise: TunaError if new-port is not integer
        """
        self.set_number(IperfGeneralConstants.port, new_port,
                        lower_bound=IperfConstants.port_lower_bound)
        return

    @property
    def window(self):
        """
        The TCP window-size flag

        :return: ' --window n[KM]' or None
        """
        return self._window

    @window.setter
    def window(self, new_window):
        """
        Sets the window size

        :param:

         - `new_window`: n[KM] or None
        """
        self.set_bytes(IperfGeneralConstants.window, new_window)
        return

    @property
    def compatibility(self):
        """
        The compatibilty flag to use with older versions of iperf

        :return: ' --compatibility ' or None
        """
        return self._compatibility

    @compatibility.setter
    def compatibility(self, turn_on):
        """
        Sets the compatibility flag

        :param:

         - `turn_on`: resolvable to True to set the flag, resolvable to False to turn it off
        """
        self.set_boolean(IperfGeneralConstants.compatibility, turn_on)
        return
    
    @property
    def mss(self):
        """
        The TCP Maximum Segment Size flag

        :return: ` --mss <n>`  or None
        """
        return self._mss

    @mss.setter
    def mss(self, new_mss):
        """
        Sets the mss flag

        :param:
         - `new_mss`: number or string castable to an Integer or None
        """
        self.set_number(IperfGeneralConstants.mss, new_mss)
        return

    @property
    def nodelay(self):
        """
        the flag to turn of Nagle's algorithm (for TCP)

        :return: ' --nodelay ' or None
        """
        return self._nodelay

    @nodelay.setter
    def nodelay(self, turn_on):
        """
        Sets the nodelay flag

        :param:
         - `turn_on`: resolvable to True to turn on, to False to turn off
        """
        self.set_boolean('_nodelay', turn_on)
        return

    @property
    def version(self):
        """
        the flag to get the iperf version number

        :return: ' --version ' or None
        """
        return self._version

    @version.setter
    def version(self, turn_on):
        """
        turns the version flag on or off

        :param:

         - `turn_on`: True to turn on, False to turn off
        """
        self.set_boolean('_version', turn_on)
        return

    @property
    def IPv6Version(self):
        """
        The flag to turn on IP v6 support

        :return: ' --IPv6Version ' or None
        """
        return self._IPv6Version

    @IPv6Version.setter
    def IPv6Version(self, turn_on):
        """
        Turns the IP v6 support flag on or off

        :param:

         - `turn_on`: True to turn on, False to turn off
        """
        self.set_boolean('_IPv6Version', turn_on)
        return

    @property
    def reportexclude(self):
        """
        returns the flag to turn off parts of the output

        :return: ' --reportexclude [CDMSV]' or None
        """
        return self._reportexclude

    @reportexclude.setter
    def reportexclude(self, exclusions):
        """
        sets flag to exclude parts of the output

        :param:

         - `exclusions`: string with some combination of values [CDMSV] or None
        """
        self._reportexclude = exclusions
        if exclusions is not None:
            if (type(exclusions) is not StringType):
                raise TunaError("reportexclude options must be a string, not '{0}'".format(exclusions))

            if not IperfConstants.reportexclude_expression.search(exclusions):
                raise TunaError("reportexclude options can only be one of [CDMSV] (case-insensitive), not '{0}'".format(exclusions))
        self.logger.debug("reportexclude set to '{0}'".format(exclusions))
        return

    @property
    def reportstyle(self):
        """
        the flag to turn on csv-formatting

        :return: ' --reportstyle [Cc]' or None
        """
        return self._reportstyle

    @reportstyle.setter
    def reportstyle(self, c_or_C):
        """
        Sets the csv-output flag

        :param:

          - `c_or_C`: 'c', 'C', or None
        """
        self._reportstyle = c_or_C
        if c_or_C is not None:
            if type(c_or_C) is not StringType:
                raise TunaError("reportstyle must be 'c' or 'C', not {0}".format(c_or_C))

            if len(c_or_C) > 1 or c_or_C not in 'Cc':
                raise TunaError('reportstyle must be "c" or "C", not {0}'.format(c_or_C))
        self.logger.debug("reportstyle set to '{0}'".format(c_or_C))
        return

    def update(self, parameters):
        """
        Sets the values based on parameters (dictionary of attribute:value)

        :param:

         - `parameters`: dict whose keys are settings names and values are valid settings

        :return: dict with used parameters removed 
        """
        matches = [(key, value) for key, value in parameters.iteritems() if hasattr(self, key)]
        for key, value in matches:
            setattr(self, key, value)
            del parameters[key]
        return parameters

    def __str__(self):
        """
        returns the options that have been set with their values formatted to pass to iperf
        """
        output = "".join([" --{o} {v}".format(o=option, v=getattr(self, option))
                          for option in IperfConstants.general_options if getattr(self, option) is not None])
        #for option in IperfConstants.general_options:
        #    if getattr(self, option) is not None:
        #        output += " --{o} {v}".format(o=option,
        #                                      v=getattr(self, option))
        return output


class IperfCompositeBase(IperfBaseSettings):
    """
    A base class for the client and server settings
    (which compose the Iperf General settings)
    """
    def __init__(self, attributes, udp=None, **kwargs):
        super(IperfCompositeBase, self).__init__()
        self._logger = None
        self.attributes = attributes
        self._prefix = None
        self._udp = None
        self.udp = udp
        self.general_settings = IperfGeneralSettings(**kwargs)
        return

    @property
    def udp(self):
        """
        The flag to turn on UDP

        :return: ' --udp ' or None
        """
        return self._udp

    @udp.setter
    def udp(self, turn_on):
        """
        Turns the udp flag on or off

        :param;

         - `turn_on`: resolvable to True to turn on, to False to turn off
        """
        self.set_boolean(IperfGeneralConstants.udp, turn_on)
        return

    @abstractproperty
    def prefix(self):
        """
        First part of string (e.g. --client <server> or --server)
        """

    def set(self, attribute, value):
        """
        this class aggregates the IperfGeneralSettings so this will try general settings first then self.<attribute>

        :param:

         - `attribute`: name of attribute to set (either from this class or IperfGeneralSettings)
         - `value`: value to set attribute

        :raise: TunaError if this class or IperfGeneralSettings doesn't have attribute
        """
        if hasattr(self.general_settings, attribute):
            setattr(self.general_settings, attribute, value)
        elif hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            # setattr will create the attribute if it didn't exist so
            # setting it will never raise an error 
            raise TunaError("Unknown Attribute: {0}".format(attribute))
        return

    def get(self, attribute):
        """
        Gets the value associated with the attribute from the General Settings

        :param:

         - `attribute`: name of a property to get

        :raise: TunaError if the attribute is unknown
        """
        if hasattr(self, attribute):
            return getattr(self, attribute)
        try:
            return getattr(self.general_settings, attribute)
        except AttributeError as error:
            self.logger.error(error)
            raise TunaError("Unknown attribute: {0}".format(attribute))
        return

    def update(self, parameters):
        """
        Updates self and IperfGeneral settings using parameters dictionary

        :param:

         - `parameters`: Dict of 'attribute:value' pairs

        :postcondition: self.general_settings and self updated

        :return: dict of leftover parameters
        """
        parameters = parameters.copy()

        for key, value in parameters.items():
            try:
                self.set(key, value)
                del parameters[key]
            except TunaError as error:
                self.logger.debug(error)
        return parameters            

    def __str__(self):
        """
        Outputs the settings (everything to pass to the iperf command)

        :precondition: self.prefix is a string
        """
        options = "".join([' --{o} {v}'.format(o=option, v=getattr(self, option))
                           for option in self.attributes if getattr(self, option) is not None])
        return  self.prefix + options + str(self.general_settings)


class IperfServerSettings(IperfCompositeBase):
    """
    A holder of settings for Iperf Servers
    """
    def __init__(self, daemon=None, single_udp=None,
                 **kwargs):
        """
        IperfServerSettings constructor

        :param:

         - `daemon`: Boolean to turn daemon mode on or off
         - `single_udp`: Boolean to turn UDP single-threaded mode on or off
         - `kwargs`: whatever IperfGeneralSettings takes
        """
        super(IperfServerSettings, self).__init__(attributes=IperfConstants.server_options,
                                                  **kwargs)
        self._daemon = None
        self.daemon = daemon

        self._single_udp = None
        self.single_udp = single_udp
        #self.general_settings = IperfGeneralSettings(**kwargs)
        return

    @property
    def prefix(self):
        """
        the server flag

        :return: ` --server `
        """
        if self._prefix is None:
            self._prefix = ' --server'
        return self._prefix

    @property
    def daemon(self):
        """
        Flag to turn on daemon mode

        :return: ' --daemon' or None
        """
        return self._daemon

    @daemon.setter
    def daemon(self, turn_on):
        """
        sets or unsets the daemon flag

        :param:

         - `turn_on`: True to turn on, False to turn off
        """
        self.set_boolean('_daemon', turn_on)
        return

    @property
    def single_udp(self):
        """
        The flag to turn on single-threaded UDP mode

        :return: '--single_udp' or None
        """
        return self._single_udp

    @single_udp.setter
    def single_udp(self, turn_on):
        """
        sets the flag to run in single-threaded UDP mode

        :param:

         - `turn_on`: True to turn on the flag, False to turn it off
        """
        self.set_boolean('_single_udp', turn_on)
        return
# end class IperfServerSettings    


class IperfClientConstants(object):
    """
    Constants for the IperfClientSettings
    """
    __slots__ = ()
    options = ('udp', 'bandwidth', 'dualtest', 'num', 'tradeoff', 'time', 'fileinput',
               'stdin', 'listenport', 'parallel', 'ttl')
    
    # attributes
    bandwidth = '_bandwidth'
    num = '_num'
    tradeoff = '_tradeoff'
    time = '_time'
    stdin = '_stdin'
    listenport = '_listenport'
    parallel = '_parallel'
    ttl = '_ttl'


class IperfClientSettings(IperfCompositeBase):
    """
    Settings for iperf clients
    """
    def __init__(self, server=None, bandwidth=None, dualtest=None, num=None,
                 tradeoff=None, time=None, fileinput=None, stdin=None,
                 listenport=None, parallel=None, ttl=None, linux_congestion=None):
        """
        IperfClientSettings constructor

        :param:

         - `server`: hostname of the target iperf server
         - `bandwidth`: UDP target bandwidth
         - `dualtest`: Boolean to enable simultaneous bi-directional testing
         - `num`: number of bytes to transmit before stopping
         - `tradeoff`: Boolean to enable separate bi-directional testing
         - `time`: number of seconds to run
         - `fileinput`: Name of a file to provide data to transmit
         - `stdin`: flag to take data from stdin
         - `listenport`: port to listen on when running bi-directional traffic
         - `parallel`: Number of threads to run
         - `ttl`: Time-to-liver for multicast traffic
         - `linux_congestion`: TCP control algorithm to use (Linux only)
        """
        super(IperfClientSettings, self).__init__(attributes=IperfClientConstants.options)
        self._prefix = None

        self._server = None
        self.server = server

        self._bandwidth = None
        self.bandwidth = bandwidth

        self._dualtest = None
        self.dualtest = dualtest

        self._num = None
        self.num = num

        self._tradeoff = None
        self.tradeoff = tradeoff

        self._time = None
        self.time = time

        self._fileinput = None
        self.fileinput = fileinput

        self._stdin = None
        self.stdin = stdin

        self._listenport = None
        self.listenport = listenport

        self._parallel = None
        self.parallel = parallel

        self._ttl = None
        self.ttl = ttl

        self._linux_congestion = None
        self.linux_congestion = linux_congestion
        return

    @property
    def prefix(self):
        """
        Prefix for options

        :return: --client <server address>
        :raise: TunaError if self._server is None
        """
        if self._prefix is None:
            try:
                self._prefix = " --client " + self.server
            except TypeError as error:
                self.logger.error(error)
                raise TunaError("server hostname must be set before use -- currently {0}".format(self.server))
        return self._prefix

    @property
    def server(self):
        """
        hostname for the target server

        :return: <server address or None>
        """
        return self._server    
        
    @server.setter
    def server(self, hostname):
        """
        Sets the hostname for the target server

        the server attribute was added because I kept forgetting what it was called when I wanted to change it

        :param:

         - `hostname`: address of the target iperf server

        :postcondition: self._prefix is None, self._server = hostname
        """
        self._prefix = None
        self._server = hostname
        return

    @property
    def bandwidth(self):
        """
        The flag to set the udp bandwidith

        :return: ' --bandwidth <bits/sec>' or None
        """
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, new_bandwidth):
        """
        Sets the bandwidth flag (and the UDP flag)

        :param:

         -  `new_bandwidth`: n[KM] or None
        """
        self.set_bytes(IperfClientConstants.bandwidth, new_bandwidth)
        return

    @property
    def dualtest(self):
        """
        Flag to enable simultaneous bi-directional testing

        :return: ` --dualtest ` or None
        """
        return self._dualtest

    @dualtest.setter
    def dualtest(self, turn_on):
        """
        enables or disables the dualtest flag

        :param:

         - `turn_on`: Boolean which if True enables the flag
        """
        self.set_boolean('_dualtest', turn_on)
        return

    @property
    def num(self):
        """
        Flag to set limit of bytes to send (instead of stopping after a certain amount of time)

        :return: ` --num n[KM]` or None
        """
        return self._num

    @num.setter
    def num(self, new_num):
        """
        Sets the number of bytes to transmit

        :param:

         - `new_num`: n[KM] or None
        """
        self.set_bytes(IperfClientConstants.num, new_num)
        return

    @property
    def tradeoff(self):
        """
        Flag to enable separate bi-directional testing

        :return: ` --tradeoff ` or None
        """
        return self._tradeoff

    @tradeoff.setter
    def tradeoff(self, turn_on):
        """
        enables or disables the separate bi-directional flag

        :param:

         - `turn_on`: Boolean which if True sets flag
        """
        self.set_boolean(IperfClientConstants.tradeoff, turn_on)
        return

    @property
    def time(self):
        """
        Flag to set the number of seconds to transmit

        :return: ` --time <seconds> ` or None
        """
        return self._time

    @time.setter
    def time(self, new_time):
        """
        Sets the flag to set the number of seconds to run

        :param:

         - `new_time`: number or None (negative numbers will run infinitely (or at least until the apocalypse))
        """
        self.set_number(IperfClientConstants.time, new_time)
        return

    @property
    def fileinput(self):
        """
        Flag to set filename to provide data to transmit instead of random bytes.

        :return: ` --fileinput <filename>` or None
        """
        return self._fileinput

    @fileinput.setter
    def fileinput(self, filename):
        """
        Sets the flag to use a file for data transmission instead of random bytes

        :param:

         - `filename`: name of file with data
        """
        self._fileinput = filename
        return

    @property
    def stdin(self):
        """
        Flag to accept data from stdin

        :return: ` --stdin` or None
        """
        return self._stdin

    @stdin.setter
    def stdin(self, turn_on):
        """
        Enables or disables flag to take data from standard input.

        :param:

         - `turn_on`: Boolean to enable or disable the flag.
        """
        self.set_boolean(IperfClientConstants.stdin, turn_on)
        return

    @property
    def listenport(self):
        """
        The flag to set the port to listen to when running bi-directional traffic

        :return: ` --listenport <port>` or None
        """
        return self._listenport

    @listenport.setter
    def listenport(self, new_port):
        """
        Sets the port to listen to

        :param:

         - `new_port`: number for port

        :raise: TunaError if not a number or less than 1024
        """
        self.set_number(IperfClientConstants.listenport, new_port,
                        lower_bound=IperfConstants.port_lower_bound)
        return

    @property
    def parallel(self):
        """
        Flag to set the number of parallel threads to run

        :return: ` --parallel <threads>` or None
        """
        return self._parallel

    @parallel.setter
    def parallel(self, threads):
        """
        Sets the flag for the number of parallel threads to run

        :param:

         - `threads`: number of threads (anything non-numeric or < 2 will be ignored)
        """
        self.set_number(IperfClientConstants.parallel, threads)

    @property
    def ttl(self):
        """
        The flag to set the time-to-live for multicast traffic

        :return: ` --ttl <time-to-live>` or None
        """
        return self._ttl

    @ttl.setter
    def ttl(self, time_to_live):
        """
        Sets the time-to-live flag

        :param:

         - `time_to_live`: interger time-to-live for multicast packets
        """
        self.set_number(IperfClientConstants.ttl, time_to_live)

    @property
    def linux_congestion(self):
        """
        The flag to set the TCP congestion control algorithm

        :return: ` --linux-congestion <algorithm>` or None
        """
        return self._linux_congestion

    @linux_congestion.setter
    def linux_congestion(self, algorithm):
        """
        Sets the TCP congestion-control algorithm flag

        :param:

         - `algorithm`: name of algorithm to use
        """
        self._linux_congestion = algorithm
        return

    def __str__(self):
        """
        settings string like parent-class but added to hands non-standard '--linux-congestion' option
        """
        output = super(IperfClientSettings, self).__str__()
        if self.linux_congestion is not None:
            output += " --linux-congestion {0}".format(self.linux_congestion)
        return output
# end class IperfClientSettings    


if __name__ == '__main__':
    import pudb; pudb.set_trace()
    configuration = IperfServerSettings()
    configuration.set('interval', 1)
            
    expected = " --server --interval 1"
    assert expected == str(configuration)
