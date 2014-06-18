
# this package
from tuna.components.composite import Composite
from tuna.infrastructure.quartermaster import QuarterMaster
from tuna import DontCatchError, MODULES_SECTION


class QualityComposite(Composite):
    """
    A quality for the optimizer
    """
    def __init__(self, *args, **kwargs):
        super(QualityComposite, self).__init__(*args, **kwargs)
        self.quality_checks = 0
        return
    
    def __call__(self, *args, **kwargs):
        """
        Calls the components, passing along the arguments

        :return: last output from the components not None
        """
        # since the quality-components are buried in a list
        # this is here to help see how efficient the optimizers are
        self.quality_checks += 1
        output = None
        for component in self.components:
            returned = component(*args, **kwargs)
            if returned is not None:
                output = returned
        return output

    def reset(self):
        """
        Resets the quality-checks
        """
        super(QualityComposite, self).reset()
        self.quality_checks = 1
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
