Quality Composite
=================

This is a composite with the call overriden so that it takes arguments and passes them to the components and then retrieves an output and returns it. This assumes that the components take arguments, and can filter out what they need, which is different from the default Component definition. This was implemented so that the composite can pass along tweaked candidates to the components that know what to do with them. This requires that the creator of components for this composite be careful to not have conflicting parameter names, that all components take arguments, even if they don't use them, and that only one of the components returns a valid output (because that is all that will be returned). Additionally, unless only one component takes arguments (and even in that case) it will be safer for the caller of the composite to use keyword arguments only.

.. '

The Quality Composite
---------------------



.. uml::

   Composite <|-- QualityComposite
   Composite : __call__(*args, **kwargs)

.. currentmodule:: tuna.qualities.qualitycomposite
.. autosummary::
   :toctree: api

   QualityComposite
   QualityComposite.__call__



Quality Composite Builder
-------------------------

A convenience class to build quality composites. Builders are turning out to be light-weight versions of plugins (no help for the user).

.. currentmodule:: tuna.qualities.qualitycomposite
.. autosummary::
   :toctree: api

   QualityCompositeBuilder
   QualityCompositeBuilder.product


::

    class QualityCompositeBuilder(object):
        """
        A builder of quality-composites
        """
        def __init__(self, configuration, section_header):
            """
            QualityCompositeBuilder constructor
    
            :param:
    
             - `configuration`: configuration map with options to build this th
    ing
             - `section_header`: section in the configuration with values neede
    d
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
                                          error_message="Component has failed."
    ,
                                          component_category='quality')
                defaults = self.configuration.defaults
                external_modules = [option for option in self.configuration.opt
    ions(MODULES_SECTION)
                                     if option not in defaults]
                quartermaster.external_modules = external_modules
                for component_section in self.configuration.get_list(section=se
    lf.section_header,
                                                                     option='co
    mponents'):
                    component_name = self.configuration.get(section=component_s
    ection,
                                                            option='component',
    
                                                            optional=False)
                    component_def = quartermaster.get_plugin(component_name)
                    component = component_def(self.configuration,
                                              component_section).product
                    self._product.add(component)
                if not len(self._product.components):
                    raise ConfigurationError("Unable to build quality component
    s using 'components={0}'".format(self.section_header,
                                                                               
                                     option='components'))
            return self._product
    
    

