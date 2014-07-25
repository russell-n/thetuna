
# python standard library
import os

# third-party
import pandas
import matplotlib.pyplot as plt
import numpy


# third party
import matplotlib.pyplot as plt
import numpy


data_path = 'data/data_step50.csv'
z_data_full = numpy.loadtxt(data_path, delimiter=',')
z_data = z_data_full[0:30, 30:60]


output = 'figures/full_table_scatter.png'
max_value = z_data_full.max()
min_value = z_data_full.min()

max_index = numpy.where(z_data_full == max_value) 
min_index = numpy.where(z_data_full == min_value)

max_index_y = max_index[0][0] * 50
max_index_x = max_index[1][0] * 50

min_index_y = min_index[0][0] * 50
min_index_x = min_index[1][0] * 50
    
if not os.path.isfile(output):
    figure=plt.figure()
    axe = figure.gca()
    data_10 = numpy.where(z_data_full < 10)
    data_70 = numpy.where(z_data_full >= 70)
    colors = 'black red'.split()
    data = (data_10, data_70)
    
    axe.scatter(data_10[1] * 50, data_10[0] * 50,
                    edgecolors='black',
                    facecolors='none')
    axe.scatter(data_70[1] * 50, data_70[0] * 50,
                    edgecolors='red',
                    facecolors='none')

    axe.axvline(max_index_x, color='r')
    axe.axhline(max_index_y, color='r')
    
    axe.axvline(min_index_x, color='b')
    axe.axhline(min_index_y, color='b')
    axe.set_title("Best and Worst Bandwidths (Full Table)")
    axe.set_ylim((0, 3000))
    axe.set_xlim((0, 3000))
    figure.savefig(output)
print ".. figure:: " + output
print "   :scale: 75%"
print
print "   Max-throughput ({0} Mb/s) at ({1}, {2}) indicated by intersection of red lines. Min-throughput ({3} Mb/s) at ({4}, {5}) indicated by intersection of blue lines.\n".format(max_value,
                                                                                     max_index_x,
                                                                                     max_index_y,
                                                                                     min_value,
                                                                                     min_index_x,
                                                                                     min_index_y)




output = 'figures/quarter_table_scatter.png'
max_value = z_data.max()
min_value = z_data.min()

max_index = numpy.where(z_data == max_value) 
min_index = numpy.where(z_data == min_value)

max_index_y = max_index[0][0] * 50
max_index_x = max_index[1][0] * 50

min_index_y = min_index[0][0] * 50
min_index_x = min_index[1][0] * 50

#if not os.path.isfile(output):
if True:
    figure=plt.figure()
    axe = figure.gca()
    data_10 = numpy.where(z_data < 10)
    data_70 = numpy.where(z_data >= 70)
    colors = 'black red'.split()
    data = (data_10, data_70)
    
    axe.scatter(data_10[1] * 50, data_10[0] * 50,
                    edgecolors='black',
                    facecolors='none')
    axe.scatter(data_70[1] * 50, data_70[0] * 50,
                    edgecolors='red',
                    facecolors='none')

    axe.axvline(max_index_x, color='r')
    axe.axhline(max_index_y, color='r')
    
    axe.axvline(min_index_x, color='b')
    axe.axhline(min_index_y, color='b')
    axe.set_title("Best and Worst Bandwidths")
    #axe.set_ylim((0, 1500))
    #axe.set_xlim((1500, 3000))
    figure.savefig(output)
print ".. figure:: " + output
print "   :scale: 75%"
print
print "   Max-throughput ({0} Mb/s) at ({1}, {2}) indicated by intersection of red lines. Min-throughput ({3} Mb/s) at ({4}, {5}) indicated by intersection of blue lines.\n".format(max_value,
                                                                                     max_index_x,
                                                                                     max_index_y,
                                                                                     min_value,
                                                                                     min_index_x,
                                                                                     min_index_y)




bandwidths = pandas.read_csv('data/half_table_bandwidths.csv')
description = bandwidths.Bandwidth.describe()


for name in description.index:
    print "   {0},{1}".format(name, description.ix[name])


output = 'figures/half_table_bandwidths_kde.png'
if not os.path.isfile(output):
    figure = plt.figure()
    axe = figure.gca()
        
    bandwidths.Bandwidth.hist(ax=axe, alpha=0.25, color='k', normed=1)
    bandwidths.Bandwidth.plot(kind='kde', ax=axe, alpha=0.5, color='b',
                              title='Best Bandwidth Solutions Found (Half Table)')
        
    axe.axvline(bandwidths.Bandwidth.quantile(.5), color='r', alpha=0.5)
    axe.set_xlabel("Throughput (Mb/s)")
        
    figure.savefig(output)
print '.. figure:: ' + output
print "   :scale: 75%"


trials = 10**5
n = bandwidths.shape[0]
samples = numpy.random.choice(bandwidths.Bandwidth,
                              size=(n, trials))
means = samples.mean(axis=0)
alpha = 0.01
p = alpha/2

low = numpy.percentile(means, p)
high = numpy.percentile(means, 1-p)


print "**99% Confidence Interval:** ({0}, {1})".format(low, high)


repetitions = 0
out_file = "data/half_table_best_repetitions_counts.csv"
if not os.path.isfile(out_file):
    with open(out_file, 'w') as w:
        w.write("TemperatureCount\n")
        for line in open("data/half_table_initial_temperatures.log"):
            if "Initial" in line and repetitions !=0:
                w.write("{0}\n".format(repetitions))
                repetitions = 0
                continue
            if "Temperature" in line:
                repetitions += 1
        w.write("{0}\n".format(repetitions))


counts = pandas.read_csv(out_file)
description = counts.TemperatureCount.describe()


for name in description.index:
    print "   {0},{1:g}".format(name, description.ix[name])


RUNTIME = 15
SECONDS_PER_HOUR = 60.0 * 60.0


for name in "min 50% max".split():
    print "   {0},{1:.2g}".format(name,
                                  RUNTIME * description.ix[name]/SECONDS_PER_HOUR)


runtimes = counts.TemperatureCount * RUNTIME/SECONDS_PER_HOUR
samples = numpy.random.choice(runtimes, size=(runtimes.shape[0], trials))
means = samples.mean(axis=0)
medians = numpy.median(samples, axis=0)
low = numpy.percentile(means, p)
high = numpy.percentile(means, 1-p)

low_median = numpy.percentile(medians, p)
high_median = numpy.percentile(medians, 1-p)


print "**99% Confidence Interval (mean):** ({0:.2f}, {1:.2f})".format(low, high)
print "\n**99% Confidence Interval (Median):** ({0:.2f}, {1:.2f})".format(low_median,
                                                                          high_median)


output = 'figures/half_table_runtime_kde.png'
if not os.path.isfile(output):
    
    figure = plt.figure()
    axe = figure.gca()
        
    runtimes.hist(ax=axe, alpha=0.25, color='k', normed=1)
    runtimes.plot(kind='kde', ax=axe, alpha=0.5, color='b',
                                 title='Estimated Runtimes')
        
    axe.axvline(numpy.median(runtimes), color='r', alpha=0.5)
    axe.set_xlabel("Runtimes (Hours)")
        
    figure.savefig(output)
print '.. figure:: ' + output
print "   :scale: 75%"
