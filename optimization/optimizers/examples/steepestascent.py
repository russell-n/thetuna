
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


from pweave_helpers import run_climber
from pweave_helpers import plot_solutions
from pweave_helpers import plot_dataset


# python standard library
from collections import OrderedDict

# third party
import numpy

# this package
from optimization.datamappings.normalsimulation import NormalSimulation
from optimization.components.stopcondition import StopConditionIdeal
from optimization.components.convolutions import UniformConvolution, GaussianConvolution
from optimization.components.xysolution import XYSolution, XYTweak
from optimization.optimizers.steepestascent import SteepestAscent


outcomes = OrderedDict()
simulator = NormalSimulation(domain_start=-4,
                             domain_end=4,
                             steps=1000)

stop = StopConditionIdeal(ideal_value=simulator.ideal_solution,
                              delta=0.0001,
                              time_limit=300)

tweak = UniformConvolution(half_range=0.1,
                           lower_bound=simulator.domain_start,
                           upper_bound=simulator.domain_end)

xytweak = XYTweak(tweak)
# try a bad-case to start 
inputs = numpy.array([simulator.domain_start])
candidate = XYSolution(inputs=inputs)

climber = SteepestAscent(solution=candidate,
                         stop_condition=stop,
                         tweak=xytweak,
                         quality=simulator,
                         local_searches=4)
outcomes['Uniform Normal'] = run_climber(climber)


plot_solutions('normal_steepest_ascent', climber,
               "Normal Hill Climbing Solutions (Tweak Half-range=0.1)",
               xlabel="Solution Changes", ylabel='Solution Quality')


plot_dataset('steepest_ascent_normal_data',
             climber, simulator,
             "Dataset and Solution",
             y_offset=0.1)


candidate.output = None
climber._solutions = None
climber.solution = candidate
stop._end_time = None
climber.local_searches = 8
tweak.half_range = 1
run_climber(climber)


simulator.reset()
simulator.domain_start = -100
simulator.domain_end = 150
simulator.steps = 10000

candidate.output = None
climber._solutions = None
climber.solution = candidate
climber.emit = False

stop._end_time = None
stop.ideal_value = simulator.ideal_solution
stop.delta = 0.001

outcomes['Uniform Needle'] = run_climber(climber)


plot_solutions('needle_haystack_steepest_ascent',
               climber,
               "Needle In a Haystack Hill Climbing (Tweak Half-range=0.1)",
               xlabel='Solutions', ylabel="Quality")
print
plot_dataset('steepest_ascent_uniform_needle_haystack_data',
                climber, simulator,
              "Dataset and Solution",
              y_offset=0.1)


# change the randomization
tweak = GaussianConvolution(lower_bound=simulator.domain_start,
                            upper_bound=simulator.domain_end)
tweaker = XYTweak(tweak)
climber._solutions = None
climber.tweak = tweaker

# change the dataset
simulator.functions = [lambda x: numpy.sin(x), 
                       lambda x: numpy.cos(x)**2]
simulator._range = None
simulator.quality_checks = 0

candidate.output = None
simulator(candidate)    
climber.solution = candidate
stop.ideal_value = simulator.ideal_solution
stop._end_time = None

# run the optimization
outcomes['Gaussian Noise'] = run_climber(climber)


plot_solutions('gaussian_convolution_steepest_ascent_solutions',
               climber,
               "Steepest Ascent with Gaussian Convolution")
print
plot_dataset('gaussian_convolution_steepest_ascent_dataplot',
              climber, simulator,
              "Dataset and Solution")


simulator.reset()
simulator.domain_start = -4
simulator.domain_end = 4
simulator.steps = 1000
candidate.output = None
climber._solutions = None
climber.solution = candidate
stop._end_time = None
stop.ideal_value = simulator.ideal_solution
outcomes['Gaussian Normal'] = run_climber(climber)


plot_solutions('steepest_ascent_gaussian_convolution_normal_solutions',
               climber,
               "Gaussian Convolution Normal Dataset",
    xlabel='Solutions', ylabel="Quality")
print
plot_dataset('steepest_ascent_gaussian_convolution_normal_dataset',
              climber, simulator,
              "Dataset and Solution", y_offset=0.1)


simulator.reset()
simulator.domain_start = -100
simulator.domain_end = 150
simulator.steps = 10000
candidate.output = None
climber._solutions = None
climber.solution = candidate
stop._end_time = None
stop.ideal_value = simulator.ideal_solution
outcomes['Gaussian Needle'] = run_climber(climber)


plot_solutions('steepest_ascent_gaussian_convolution_needle_solutions',
               climber,
               "Gaussian Convolution Needle Dataset",
               xlabel='Solutions', ylabel="Quality")
print
plot_dataset('steepest_ascent_gaussian_convolution_needle_dataset',
              climber, simulator,
              "Dataset and Solution", y_offset=0.1)


from optimization.datamappings.examples.functions import SphereMapping
# for plotting only we want few steps
plot_sphere = SphereMapping(steps=120)

# for data we want more
data_sphere = SphereMapping()


output = 'figures/sphere_plot.svg'
figure = plt.figure()
axe = figure.add_subplot(111, projection='3d')

surface = axe.plot_wireframe(plot_sphere.x, plot_sphere.y, plot_sphere.z,
                             rstride=5, cstride=5)
figure.savefig(output)


simulator = data_sphere.mapping
climber.quality = simulator
candidate.output = None
climber._solutions = None
climber.solution = candidate
stop._end_time = None
stop.ideal_value = simulator.ideal
outcomes['Gaussian Sphere'] = run_climber(climber)


print ".. figure:: " + output


for name, data in outcomes.iteritems():
    print "   {0},{1:3}".format(name, data)
