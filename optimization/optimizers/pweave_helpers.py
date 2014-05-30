# python standard library
import time

# third-party
import matplotlib.pyplot as plt

def run_climber(climber, simulator):
    """
    Runs the optimization and summarizes it
    """
    start = time.time()
    solution = climber()
    end = time.time()
    print "solution: {0}".format(solution)
    print "Ideal: {0}".format(simulator.ideal_solution)
    print "Difference: {0}".format(solution.output - simulator.ideal_solution)
    print "Elapsed: {0}".format(end - start)
    return

def plot_dataset(filename, climber, simulator, title):
    output = 'figures/{0}.svg'.format(filename)
    figure = plt.figure()
    axe = figure.gca()
    axe.plot(simulator.domain, simulator.range)
    axe.axhline(climber.solution.output, color='r')
    figure.savefig(output)
    print ".. figure:: " + output
    return
