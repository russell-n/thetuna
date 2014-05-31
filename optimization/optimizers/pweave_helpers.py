# python standard library
import time
from collections import namedtuple

# third-party
import matplotlib.pyplot as plt

class ComparisonsSolutionsRatio(namedtuple('ComparisonsSolutionsRatio',
                                           'comparisons solutions ratio'.split())):
    __slots__ = ()
    def __str__(self):
        return ",".join(["{0:.3f}".format(item) for item in (self.solutions,
                                                self.comparisons,
                                                self.ratio)])
    

def run_climber(climber):
    """
    Runs the optimization and summarizes it
    """
    start = time.time()
    solution = climber()
    end = time.time()
    print "Solution: {0}".format(solution)
    print "Ideal: {0}".format(climber.quality.ideal_solution)
    print "Difference: {0}".format(solution.output -
                                   climber.quality.ideal_solution)
    print "Elapsed: {0}".format(end - start)
    checks = climber.quality.quality_checks
    solutions = len(climber.solutions)
    comparisons = (checks - 1)/2.0
    ratio = solutions/comparisons
    print "Quality Checks: {0}".format(checks)
    print "Comparisons: {0}".format(comparisons)
    print "Solutions: {0}".format(solutions)
    print "Solutions/Comparisons: {0}".format(ratio)
    return ComparisonsSolutionsRatio(comparisons,
                                     solutions,
                                     ratio)

def plot_dataset(filename, climber, simulator, title, y_offset=0.5):
    output = 'figures/{0}.svg'.format(filename)
    figure = plt.figure()
    axe = figure.gca()
    axe.plot(simulator.domain, simulator.range)
    axe.axhline(climber.solution.output, color='r')
    axe.set_title(title)
    axe.set_ylim(top=max(simulator.range) + y_offset)
    figure.savefig(output)
    print ".. figure:: " + output
    return

def plot_solutions(filename, climber, title, xlabel='Solution', ylabel='Quality'):
    output = 'figures/{0}.svg'.format(filename)
    figure = plt.figure()
    axe = figure.gca()
    data = [solution.output for solution in climber.solutions]
    axe.plot(data)
    axe.set_title(title)
    axe.set_xlabel(xlabel)
    axe.set_ylabel(ylabel)
    figure.savefig(output)
    print '.. figure:: '  + output
    return
