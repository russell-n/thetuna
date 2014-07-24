
# python standard library
import os

# third-party
import pandas
import matplotlib.pyplot as plt
import numpy


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
