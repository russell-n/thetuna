The Tuna
========

This is a package of `metaheuristic optimizers <http://en.wikipedia.org/wiki/Metaheuristic>`_. Although there are `existing python <http://docs.scipy.org/doc/scipy/reference/optimize.html>`_ optimization libraries, the purpose of the tuna is to work interactively with external systems to tune testing parameters. The documentation can be found `here <http://rallion.bitbucket.org/hortators/the_tuna/index.html>`_.

The Documentation
-----------------

The package was written using `Pweave <http://mpastell.com/pweave/>`_ and so has at least some documentation for most of the modules. To build the documentation you need `sphinx <http://sphinx-doc.org/>`_, `sphinxcontrib-plantuml <https://pypi.python.org/pypi/sphinxcontrib-plantuml/0.4>`_ (which itself requires `plantUML <http://plantuml.sourceforge.net/>`_) and `graphviz <http://www.graphviz.org/>`_ (and possibly some other things I can't remember).

Plugins
-------

To allow the running of non-tuna code a rudimentary plugin system was created that requires sub-classing the tuna's BasePlugin class and pointing to it in the config file. There's an example plugin at the top-level of the tuna's folder-structure (next to the setup.py file).