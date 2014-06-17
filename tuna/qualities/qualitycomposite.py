
# this package
from tuna.components.composite import Composite
from tuna.infrastructure.quartermaster import QuarterMaster
from tuna import DontCatchError, MODULES_SECTION


class QualityComposite(Composite):
    """
    A quality for the optimizer
    """
    def __call__(self, *args, **kwargs):
        """
        Calls the components, passing along the arguments

        :return: last output from the components not None
        """
        output = None
        for component in self.components:
            returned = component(*args, **kwargs)
            if returned is not None:
                output = returned
        return output

    def close(self):
        """
        Calls close on all components

        (this is different from the regular composite, we want to keep the components
        """
        for component in self.components:
            if hasattr(component, 'close'):
                component.close()
            else:
                self.logger.warning("'{0}' hasn't implemented the 'close' method. We hate him.".format(component))
        return

    def reset(self):
        """
        calls 'reset' on components that have them
        """
        for component in self.components:
            if hasattr(component, 'reset'):
                component.reset()
        return

# end QualityComposite    


class QualityCompositeBuilder(object):
    """
    A builder of quality-composites
    """
    def __init__(self, configuration, section_header):
        """
        QualityCompositeBuilder constructor

        :param:

         - `configuration`: configuration map with options to build this thing
         - `section_header`: section in the configuration with values needed
        """
        self.configuration = configuration
        self.section_header = section_header
        self._product = None
        return

    @property
    def product(self):
        """
        A built Quality Composite
        """
        if self._product is None:
            quartermaster = QuarterMaster(name='components')
            self._product = QualityComposite(error=DontCatchError,
                                      error_message="Component has failed.",
                                      component_category='quality')
            defaults = self.configuration.defaults
            external_modules = [option for option in self.configuration.options(MODULES_SECTION)
                                 if option not in defaults]
            quartermaster.external_modules = external_modules
            for component_section in self.configuration.get_list(section=self.section_header,
                                                                 option='components'):
                component_name = self.configuration.get(section=component_section,
                                                        option='component',
                                                        optional=False)
                component_def = quartermaster.get_plugin(component_name)
                component = component_def(self.configuration,
                                          component_section).product
                self._product.add(component)
            if not len(self._product.components):
                raise ConfigurationError("Unable to build quality components using 'components={0}'".format(self.section_header,
                                                                                                            option='components'))
        return self._product
