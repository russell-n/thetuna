
# python standard library
import timeit
import random

# third-party
import matplotlib.pyplot as plt


collection = None
value = None
repetitions = 10**4

in_pweave = __name__ == '__builtin__'


def measure_list(size):
    global collection
    global value

    collection = range(size)
    value = random.randrange(1, size)
    command = '{0} in collection'.format(value)
    import_string = 'from tuna.documentation.developer.tabu_experiments import collection, value'
    timer = timeit.Timer(command, import_string)
    return timer.timeit(repetitions)

def measure_set(size):
    global collection
    global value

    collection = set(range(size))
    value = random.randrange(1, size)
    command = '{0} in collection'.format(value)
    import_string = 'from tuna.documentation.developer.tabu_experiments import collection, value'
    timer = timeit.Timer(command, import_string)
    return timer.timeit(repetitions)
    


if in_pweave:
    step = 1000
    upper_bound = 10**4 + 1
    list_times = [(size, measure_list(size)) for size in xrange(2, upper_bound, step)]
    set_times = [(size, measure_set(size)) for size in xrange(2, upper_bound, step)]


if in_pweave:
    output = 'figures/set_list_times.png'
    figure = plt.figure()
    axe = figure.gca()
    
    list_sizes = [size_time[0] for size_time in list_times]
    list_times = [size_time[1] for size_time in list_times]
    
    set_sizes = [size_time[0] for size_time in set_times]
    set_times = [size_time[1] for size_time in set_times]
    
    axe.plot(list_sizes, list_times, color='r', alpha=0.5, label='Lists')
    axe.plot(set_sizes, set_times, color='b', alpha=0.5, label='Sets')
    
    axe.set_xlabel("Collection Sizes")
    axe.set_ylabel("Times (seconds)")
    axe.set_title("Collection Size Vs Time")
    axe.legend()
    figure.savefig(output)
    print ".. figure:: " + output


if in_pweave:
    print "List Maximum: size={0}, time={1}".format(list_sizes[-1], list_times[-1])
    print "Set Maximum: size={0}, time={1}".format(set_sizes[-1], set_times[-1])
