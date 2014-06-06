
# python standard library
from abc import ABCMeta, abstractmethod

# this package
from optimization import BaseClass


class Component(BaseClass):
    """
    Component base class
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Component, self).__init__()
        return

    @abstractmethod
    def __call__(self):
        """
        The main interface, all components will get called
        """
        return

    @abstractmethod
    def check_rep(self):
        """
        A representation-check, every component should expect a call
        """
        return
# end Component    


class Composite(Component):
    """
    a class composed of components
    """
    def __init__(self, components=None):
        """
        Composite Constructor

        :param:

         - `components`: collection of Components
        """
        super(Composite, self).__init__()
        self._components = components
        return

    @property
    def components(self):
        """
        Collection of components
        """
        if self._components is None:
            self._components = []
        return self._components
    
    def __call__(self):
        """
        The main interface. Calls the components.

        """
        for component in self.components:
            component()
        return

    def check_rep(self):
        """
        Calls the component check-reps
        """
        for component in self.components:
            component.check_rep()
        return

    def add(self, component):
        """
        Adds the component to the components

        :param:

         - `component`: object that implements Component
        """
        self.components.append(component)
        return

    def remove(self, component):
        """
        Removes the first instance of the component
        """
        try:
            self.components.remove(component)
        except ValueError as error:
            # if it's not in the list
            # then it's already removed
            # so let it slide
            self.logger.debug(error)
        return
# end Composite
