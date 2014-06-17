
# python standard library
import re
import os
from collections import OrderedDict

# this package
import tuna.infrastructure.arguments.arguments as basearguments
from tuna.infrastructure.arguments.argumentbuilder import ArgumentBuilder
from tuna.infrastructure.configurationmap import ConfigurationMap
from tuna.components.composite import Composite
#from tuna.parts.storage.filestorage import FileStorage
from tuna.infrastructure import singletons
from tuna import GLOBAL_NAME

from base_plugin import BasePlugin

from tuna import TunaError, DontCatchError, ConfigurationError
from tuna import SECTION, MODULES_SECTION
from tuna.infrastructure.quartermaster import QuarterMaster
from tuna.parts.countdown.countdown import INFO
from tuna.parts.countdown.countdown import CountdownTimer


in_pweave = __name__ == '__builtin__'


DEFAULT = 'DEFAULT'
SUBFOLDER  = 'subfolder'
COMPILED_EXTENSION = '.compiled'
FILE_STORAGE_NAME = 'infrastructure'
TIMESTAMP = 'timestamp'

CONFIGURATION = '''[{0}]
# the option names are just identifiers
# they will be executed in the order given.
# Each option has to have a corresponding section below
# e.g. if there is a Sleep1 plugin listed
# Then there needs to be a [Sleep1] section below
# to configure it
<option_name_1> = <comma-separated-list of plugins>
<option_name_2> = <comma-separated-list of plugins>
...
<option_name_n> = <comma-separated-list of plugins>

# !!!! to use an option in a commented section you need to
# uncomment both the section header and the option
# if you only uncomment the option it will be assigned
# to the first un-commented section header above it, not
# necessarily the one you want

#[MODULES]
# If you are getting a plugin from a non-ape package put the module here
# it should use the import's dot-notation. e.g. :
# packagename.modulename

#[DEFAULT]
# if you add a configuration-file-glob to the default, all matching files will be added to the configuration
# even though these need to be in the ini format I like to use a different file-extension
# so they won't accidentally get picked up if you use a glob to point to the main config files
#config_glob = settings*.config

# if you want to repeat the operation defined in this config, give it repetitions
# repetitions = 1000000

# If you want to put a time limit after which to quit (this overrides repetitions)
# total_time = 1 day 3 hours

# if you want to put an end time (this will override repetitions and total time):
# end_time = November 23, 2013 8:00 am

# if you want to store files in a sub-folder
# {1} = <name>

# If you get a ParserError check:
#   - is everything flush-left?
#   - no inline comments? (this won't raise a Parser error but it will create an error later)
'''.format(SECTION, SUBFOLDER)



output_documentation = __name__ == '__builtin__'


EXAMPLES = '''
ape run ape.ini
ape help
ape fetch
ape list'''

class Tuna(BasePlugin):
    """
    The default plugin (provides the front-end for the Tuna)
    """
    def __init__(self, configfiles=None, *args, **kwargs):
        """
        Ape plugin Constructor

        :param:

         - `configfiles`: list of config-files to build product (Hortator Composite)
        """
        super(Tuna, self).__init__(*args, **kwargs)
        self.configfiles = configfiles
        self._arguments = None
        self.file_storage = None
        return

    @property
    def arguments(self):
        """
        The ArgumentBuilder (used to set up the help-string)
        """
        if self._arguments is None:
            self._arguments = ArgumentBuilder()
        return self._arguments

    @property
    def sections(self):
        """
        An ordered dictionary for the HelpPage
        """
        if self._sections is None:
            bold = '{bold}'
            reset = '{reset}'
            
            name = __package__.split('.')[0]
            bold_name = bold + name + reset
            program = name + '[.\w]*'
            expression = re.compile(program)

            # get sample usage text
            arg_string = basearguments.__doc__.replace('Usage: ', '')
            

            # the main parser doesn't show help for the sub-commands (just --debug, --pudb, etc.)
            # so they are pulled separately
            argument_definitions = ArgumentBuilder().argument_definitions
            for definition in argument_definitions.itervalues():
                arg_string += '-' * 40 + '\n'
                arg_string +=  expression.sub(bold_name,
                                              definition().sub_usage.replace('Usage: ', ''))
            
            self._sections = OrderedDict()
            self._sections['Name'] = '{blue}' + name + reset + ' -- an optimizing package'
            self._sections['Synopsis'] = arg_string
            self._sections['Description'] = bold_name + ' is the main code-runner. When it is run it looks for a configuration file or list of configuration files. Within each file it looks for an [{0}] section. Each entry in that section is interpreted to be a list of plugins to execute in top-down, left-right ordering.'.format(TUNASECTION)
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Examples'] = 'tuna run *.ini\ntuna help\ntuna fetch\ntuna list\ntuna check *ini'
            self._sections['Errors'] = '{bold}Oops, I crapped my pants:{reset} unexpected error (probably indicates implementation error)'
            self._sections['subcommands'] = "help (this help), fetch (sample configuration), run <configuration-file(s)>, list (known plugins), check (configuration)"
            self._sections['Files'] = __file__
        return self._sections
    
    @property
    def product(self):
        """
        This is the Hortator Composite product

        :precondition: self.configfiles has been set 
        :return: hortator built from self.configfiles
        """
        #create a hortator
        hortator = Composite(error=Exception,
                             identifier='Hortator',
                             error_message="Operator Crash",
                             component_category='Operator')
        # Set the TimeTracker level to info so it outputs to the screen
        hortator.time_remains.log_level = INFO
        # traverse the config-files to get Operators and configuration maps
        for config_file in self.configfiles:
            # the QuarterMaster is being created each time because I am now allowing the addition
            # of external packages, and I don't want namespace clashes
            quartermaster = QuarterMaster()

            # each APE config gets its own Operator
            operator = Composite(identifier="Operator",
                                 error=TunaError,
                                 error_message='Operation Crash',
                                 component_category='Operation')

            configuration = ConfigurationMap(config_file)
            
            defaults = configuration.defaults

            # build the countdown timer
            repetitions = configuration.get_int(section=DEFAULT,
                                                option='repetitions',
                                                optional = True,
                                                default=1)
            total_time = configuration.get_relativetime(section=DEFAULT,
                                                        option='total_time',
                                                        optional=True,
                                                        default=None)
            end_time = configuration.get_datetime(section=DEFAULT,
                                                      option='end_time',
                                                      optional=True,
                                                      default=None)
            operator.time_remains = CountdownTimer(repetitions=repetitions,
                                                   total_time=total_time,
                                                   end_time=end_time,
                                                   log_level=INFO)
            # check for external package declarations
            if MODULES_SECTION in configuration.sections:
                external_modules = [option for option in configuration.options(MODULES_SECTION)
                                    if option not in defaults]
                quartermaster.external_modules = external_modules                        
            
            # traverse the APE Section's options to get Operations
            # configuration.options(TUNASECTION) is a list of config-file options in the [APE] section
            # names is filtered to get rid of the DEFAULT options
            names = (name for name in configuration.options(SECTION) if not
                     (name in defaults and
                      defaults[name] ==
                      configuration.get(SECTION, name)))

            # the operations won't know repetitions or how long the operation has been running
            # but since end_time is an absolute time, they can check for that between operations
            countdown = None
            if end_time is not None:
                countdown = CountdownTimer(end_time=end_time)

            # the next loop is going to start building plugins, so we need to set the FileStorage now
            self.initialize_file_storage(configuration)
            
            for operation_name in names:
                # every option in the APE section gets an operation
                operation = Composite(identifier='Operation',
                                      error=DontCatchError,
                                      error_message='{0} Crash'.format(operation_name),
                                      component_category=operation_name,
                                      time_remains=countdown)

                #traverse this line to get plugins
                # get_list is a list of comma-separated strings in the operation line
                for plugin_section_name in configuration.get_list(SECTION, operation_name):                    
                    # the quartermaster returns a class-definition, not an instance
                    # so we can pass in the configuration and build it to get the `product`

                    # in order to allow multiple configurations for the same plugin
                    # I'm detaching the section name from the plugin name
                    # this means there is a requirement that a 'plugin' field be in each
                    # plugin definition
                    plugin_name = configuration.get(plugin_section_name, 'plugin')
                    if plugin_name is None:
                        raise ConfigurationError("Plugin for section '{0}' missing (e.g. plugin=HillClimber)".format(plugin_section_name))
                    plugin_def = quartermaster.get_plugin(plugin_name)
                    try:
                        # since there are now arbitrary names for the sections
                        # either the specific section or the section name has to be passed in
                        plugin = plugin_def(configuration=configuration, section_header=plugin_section_name).product
                        if plugin is None:
                            raise TunaError("{0} is missing a `product` (returned None)".format(plugin_name))
                    except TypeError as error:
                        self.log_error(error)
                        raise ConfigurationError('Could not build "{0}" plugin'.format(plugin_name))
                    operation.add(plugin)
                operator.add(operation)

            hortator.add(operator)
            # save the configuration as a copy so there will be a record
            self.save_configuration(configuration)
        return hortator

    def initialize_file_storage(self, configuration):
        """
        This has to be called before the plugins are built so the path will be set

        :param:

         - `configuration`: the Configuration (a ConfigParser like object)

        :postcondition: file-storage singleton with sub-folder from default section added as path
        """
        if self.file_storage is None:
            self.file_storage = singletons.get_filestorage(name=GLOBAL_NAME)
            
        if SUBFOLDER in configuration.defaults:
            self.file_storage.path = configuration.defaults[SUBFOLDER]
        if TIMESTAMP in configuration.defaults:
            self.file_storage.timestamp = configuration.defaults[TIMESTAMP]
        return

    def save_configuration(self, configuration):
        """
        saves the configuration map to disk

        :param:

         - `configuration`: A ConfigurationMap to save to disk
        """
        if self.file_storage is None:
            self.initialize_file_storage(configuration)
        # get the sub-folder (if given) and let the FileStorage mangle the name as needed
        # to prevent clobbering files

        filename, extension = os.path.splitext(configuration.filename)

        # the extension is changed so if the user is using a glob
        # and didn't provide a sub-folder the compiled file won't
        # get picked up on re-running the code
        filename += COMPILED_EXTENSION
        name = self.file_storage.safe_name(filename)
        configuration.write(name)
        return
        
    def fetch_config(self):
        """
        Prints example configuration to stdout
        """
        print CONFIGURATION
# end class Tuna
