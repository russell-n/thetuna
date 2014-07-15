# python standard library
import timeit
import random

# third-party
import matplotlib.pyplot as plt


collection = None
value = None
repetitions = 10**4

def measure_list(size):
    global collection
    global value

    collection = range(size)
    value = size - 1
    command = '{0} in collection'.format(value)
    import_string = 'from __main__ import collection, value'
    timer = timeit.Timer(command, import_string)
    return timer.timeit(repetitions)

def measure_set(size):
    global collection
    global value

    collection = set(range(size))
    value = size - 1
    command = '{0} in collection'.format(value)
    import_string = 'from __main__ import collection, value'
    timer = timeit.Timer(command, import_string)
    return timer.timeit(repetitions)


step = 100000
lower_bound = 80000
upper_bound = 9 * 10**5 + 1
list_sizes_times = [(size, measure_list(size)) for size in xrange(lower_bound, upper_bound, step)]
set_sizes_times = [(size, measure_set(size)) for size in xrange(lower_bound, upper_bound, step)]

output = 'figures/set_list_times.png'
figure = plt.figure()
axe = figure.gca()

list_sizes = [size_time[0] for size_time in list_sizes_times]
list_times = [size_time[1] for size_time in list_sizes_times]

set_sizes = [size_time[0] for size_time in set_sizes_times]
set_times = [size_time[1] for size_time in set_sizes_times]

axe.plot(list_sizes, list_times, color='r', alpha=0.5, label='Lists')
axe.plot(set_sizes, set_times, color='b', alpha=0.5, label='Sets')

axe.set_xlabel("Collection Sizes")
axe.set_ylabel("Times (seconds)")
axe.set_title("Collection Size Vs Time")
axe.legend(loc='upper left')
figure.savefig(output)


with open('data/list_times.csv', 'w') as lw:
    lw.write("Size,Time\n")
    for size, time in list_sizes_times:
        lw.write("{0},{1}\n".format(size,time))

with open('data/set_times.csv', 'w') as sw:
    sw.write("Size,Time\n")
    for size, time in set_sizes_times:
        sw.write("{0},{1}\n".format(size,time))




