
# python standard library
import os
import importlib
import inspect

# this package
from tuna import BaseClass
from tuna.infrastructure.ryemother import RyeMother
from tuna.plugins.base_plugin import BasePlugin


class QuarterMaster(BaseClass):
    """
    A plugin manager
    """
    def __init__(self, external_modules=None, parent=BasePlugin,
                 group='tuna.plugins', name='plugins',
                 exclusions=['tuna.plugins.index']):
        """
        The Plugin Manager

        :param:

         - `external_modules`: iterable collection of module-names
         - `parent`: Parent class to identify plugins
         - `group`: group-name from setup.py
         - `name`: name from the setup.py file
         - `exclusions`: module names not to import (to avoid side-effects)
        """
        super(QuarterMaster, self).__init__()
        self._plugins = None
        self._import_plugins = None
        self.external_modules = None
        self.parent = BasePlugin
        self.group = group
        self.name = name
        self.exclusions = exclusions
        return

    @property
    def import_plugins(self):
        """
        A RyeMother instance
        """
        if self._import_plugins is None:
            # the group and name values are created in setup.py entry_points
            self._import_plugins = RyeMother(group=self.group, name=self.name,
                                             exclusions=self.exclusions,
                                             parent=self.parent)
        return self._import_plugins

    @property
    def plugins(self):
        """
        A dictionary of plugins (this is persistent, unlike the generators, in case it gets re-used)
        """
        if self._plugins is None:
            self._plugins = self.import_plugins()
            # check if external modules were given
            if self.external_modules is not None:
                for module_name in self.external_modules:
                    self._plugins.update(self.import_plugins(modulename=module_name))
        return self._plugins        
    
    def list_plugins(self):
        """
        Prints the names of the plugins to standard out
        """
        for name in sorted(self.plugins.keys()):
            print name
        return

    def get_plugin(self, name):
        """
        Retrieves a plugin object.

        :param:

         - `name`: The name of a plugin class
         - `configuration`: A configuration map instance

        :return: An un-built plugin object definition
        """
        self.logger.debug("Retrieving {0}".format(name))
        try:
            return self.plugins[name]
        except KeyError as error:
            self.logger.error(error)
        return
# end class QuarterMaster    
