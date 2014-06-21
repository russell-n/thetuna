The Base Configuration
======================



.. _rvrconfiguration-baseconfiguration:

BaseConfiguration Class
-----------------------

The purpose of this class is to enforce some expected attributes and to provide an `unknown_options` method to children. Additionally, since it inherits from the :ref:`BaseClass <base-class>` children will get a logger (assuming they initialize this parent class).

.. uml::

   BaseClass <|-- BaseConfiguration
   BaseConfiguration o- ConfigurationAdapter
   BaseConfiguration : String section
   BaseConfiguration : List options
   BaseConfiguration : List unknown_options
   BaseConfiguration : List exclusions
   BaseConfiguration : check_rep()
   BaseConfiguration : reset()

.. currentmodule:: tuna.common.baseconfiguration
.. autosummary::
   :toctree: api

   BaseConfiguration
   BaseConfiguration.section
   BaseConfiguration.options
   BaseConfiguration.example
   BaseConfiguration.unknown_options
   BaseConfiguration.exclusions
   BaseConfiguration.check_rep
   BaseConfiguration.reset

