
# third-party
import numpy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

# this package
from optimization.datamappings.examples.functions import RastriginMapping
from optimization.components.stopcondition import StopConditionIdeal
from optimization.components.convolutions import GaussianConvolution
from optimization.components.xysolution import XYSolution, XYTweak
from optimization.optimizers.steepestascent import SteepestAscent
from pweave_helpers import run_climber


rastrigin_data = RastriginMapping()
rastrigin_plot = RastriginMapping(steps=200)
simulator = rastrigin_data.mapping

stop = StopConditionIdeal(ideal_value=simulator.ideal_solution,
                                   delta=0.0001,
                                   time_limit=300)

tweak = GaussianConvolution(lower_bound=rastrigin_data.start,
                            upper_bound=rastrigin_data.stop)
xytweak = XYTweak(tweak)
candidate = XYSolution(inputs=numpy.array([0,0]))
climber = SteepestAscent(solution=candidate,
                         stop_condition=stop,
                         tweak=xytweak,
                         quality=simulator,
                         local_searches=4)


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


run_climber(climber)
