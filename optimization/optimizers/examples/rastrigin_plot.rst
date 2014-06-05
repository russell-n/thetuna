Rastrigin Plot
--------------

::

    # third-party
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    import matplotlib.pyplot as plt
    import numpy
    
    # this package
    from optimization.datamappings.examples.functions import RastriginMapping
    
    

::

    rastrigin_plot = RastriginMapping(steps=50)
    output = 'figures/rastrigin.svg'
    figure = plt.figure()
    axe = figure.add_subplot(111, projection='3d')
    
    X = numpy.linspace(-5.12, 5.12, 100)
    Y = numpy.linspace(-5.12, 5.12, 100)
    X, Y = numpy.meshgrid(X, Y)
    
    Z = 20 + X**2 - 10 * numpy.cos(2 * numpy.pi * X) + Y**2 - 10 * numpy.cos(2 
    * numpy.pi * Y)
    
    surface = axe.plot_surface(X,
                               Y,
                               Z,
                               rstride=1, cstride=1,
                               cmap=cm.winter, linewidth=0, antialiased=False) 
                              
    figure.savefig(output)
    
    

.. figure:: figures/rastrigin.svg

