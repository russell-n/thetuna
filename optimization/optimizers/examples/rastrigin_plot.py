
# third-party
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.pyplot as plt

# this package
from optimization.datamappings.examples.functions import RastriginMapping


rastrigin_plot = RastriginMapping(steps=200)
output = 'figures/rastrigin.svg'
figure = plt.figure()
axe = figure.add_subplot(111, projection='3d')
surface = axe.plot_surface(rastrigin_plot.x,
                           rastrigin_plot.y,
                           rastrigin_plot.z,
                           rstride=1, cstride=1,
                           cmap=cm.coolwarm, linewidth=0, antialiased=False)
figure.savefig(output)


print '.. figure:: ' + output
