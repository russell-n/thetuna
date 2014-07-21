
# python standard library
from itertools import izip
import os

# third party
import numpy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import pandas


data_path = 'data/data_step50.csv'
z_data = numpy.loadtxt(data_path, delimiter=',')
flat_data = numpy.reshape(z_data, -1)
width, height = z_data.shape
x_data = numpy.linspace(start=0, stop=3000, num=width)
y_data = numpy.linspace(start=0, stop=3000, num=height)
x_data, y_data = numpy.meshgrid(x_data, y_data)


output = 'figures/data_profile.png'
if not os.path.isfile(output):
    figure = plt.figure()
    axe = figure.add_subplot(111, projection='3d')
    axe.plot_surface(x_data, y_data, z_data, cmap=cm.winter)
    axe.elev -= 30
    axe.azim += 60
    figure.savefig(output)
print '.. figure:: ' + output
print "   :scale: 75%"


output = 'figures/data_angled.png'
if not os.path.isfile(output):
    figure = plt.figure()
    axe = figure.add_subplot(111, projection='3d')
    axe.plot_surface(x_data, y_data, z_data, cmap=cm.winter)
    figure.savefig(output)
print '.. figure:: ' + output
print "   :scale: 75%"


noughts = flat_data[flat_data < 10]
tens = flat_data[flat_data < 20]
tens = tens[tens >= 10]
twenties = flat_data[flat_data < 30]
twenties = twenties[twenties >= 20]
thirties = flat_data[flat_data < 40]
thirties = thirties[thirties >= 30]
forties = flat_data[flat_data < 50]
forties = forties[forties >= 40]
fifties = flat_data[flat_data >= 50]
fifties = fifties[fifties < 60]
sixties = flat_data[flat_data >=60]
sixties = flat_data[sixties < 70]
seventies = flat_data[flat_data >= 70]


output = 'figures/contoured.png'
max_value = z_data.max()
min_value = z_data.min()

max_index = numpy.where(z_data == max_value) 
min_index = numpy.where(z_data == min_value)

max_index_x = max_index[0][0] * 50
max_index_y = max_index[1][0] * 50

min_index_x = min_index[0][0] * 50
min_index_y = min_index[1][0] * 50
    
if not os.path.isfile(output):
    figure=plt.figure()
    axe = figure.gca()
    c_data = axe.contour(y_data, x_data, z_data)
    axe.clabel(c_data)
    axe.axvline(max_index_x, color='r')
    axe.axhline(max_index_y, color='r')
    
    axe.axvline(min_index_x, color='b')
    axe.axhline(min_index_y, color='b')
    axe.set_title("Contour Map")
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



output = 'figures/best_worst_scatter.png'
if not os.path.isfile(output):   
    figure=plt.figure()
    axe = figure.gca()
    
    data_10 = numpy.where(z_data < 10)
    data_70 = numpy.where(z_data >= 70)
    colors = 'black red'.split()
    data = (data_10, data_70)
    
    axe.scatter(data_10[0] * 50, data_10[1] * 50,
                    edgecolors='black',
                    facecolors='none')
    axe.scatter(data_70[0] * 50, data_70[1] * 50,
                    edgecolors='red',
                    facecolors='none')
    
    axe.axvline(max_index_x, color='r')
    axe.axhline(max_index_y, color='r')
    
    axe.axvline(min_index_x, color='b')
    axe.axhline(min_index_y, color='b')
    axe.set_xlim((0, 3000))
    axe.set_ylim((0, 3000))
    axe.set_title("Best and Worst")
    figure.savefig(output)
print ".. figure:: " + output
print "   :scale: 75%"
print
print "   Best and worst throughput locations. Black indicates < 10 Mbits/second. Red indicates > 70 Mbits/second."
print "   Intersection of red lines indicate best overall location. Intersection of blue lines indicate worst location."


z_series = pandas.Series(flat_data)
description = z_series.describe()

for stat in description.index:
    print "   {0},{1:g}".format(stat, description.ix[stat])


output = 'figures/box_plot.png'
if not os.path.isfile(output):    
    figure = plt.figure()
    axe = figure.gca()
    axe.set_title("Throughput")
    axe.boxplot(flat_data)
    axe.set_ylabel("Mbits/sec")
    figure.savefig(output)
print ".. figure:: " + output
print "     :scale: 75%"


output = 'figures/data_kde.png'
if not os.path.isfile(output):
    frame = pandas.DataFrame(z_data)
    
    figure = plt.figure()
    axe = figure.gca()
    
    stacked = frame.stack()
    stacked.hist(ax=axe, alpha=0.25, color='k', normed=1)
    stacked.plot(kind='kde', ax=axe, alpha=0.5, color='b')
    
    axe.axvline(numpy.median(flat_data), color='r', alpha=0.5)
    axe.set_xlabel("Throughput (Mb/s)")
    
    figure.savefig(output)
print '.. figure:: ' + output
print "   :scale: 75%"


output = 'figures/data_cdf.png'
if not os.path.isfile(output):
    figure = plt.figure()
    axe = figure.gca()
    normed = flat_data/flat_data.sum()
    cumulative_data = numpy.cumsum(normed)
    #axe.plot(cumulative_data)
    out = axe.hist(flat_data, normed=True, cumulative=True, bins=500, histtype='step')
    out = axe.set_xlim((0, flat_data.max()))
    out = axe.set_ylim((0, 1))
    out = axe.set_title("Cumulative Distribution")
    axe.set_xlabel("Bandwidth Mbits/second")
    out = plt.axvline(numpy.median(flat_data), color='r')
    figure.savefig(output)
print '.. figure:: ' + output
print "  :scale: 75%"


total = float(len(flat_data))
less_than_one = flat_data[flat_data < 1]
one_to_twenty = flat_data[(flat_data >=1) & (flat_data < 20)]


print "**Less than 1 Mbits/Second:** {0:.3g}\n".format(len(less_than_one)/total)
print "**From 1 to less than 20 Mbits/Second:** {0:.3g}".format(len(one_to_twenty)/total)


print "   0-9,{0},{1:.3f}".format(len(noughts), len(noughts)/total)
print "   10-19,{0},{1:.3f}".format(len(tens), len(tens)/total)
print "   20-29,{0},{1:.3f}".format(len(twenties), len(twenties)/total)
print "   30-39,{0},{1:.3f}".format(len(thirties), len(thirties)/total)
print "   40-49,{0},{1:.3f}".format(len(forties), len(forties)/total)
print "   50-59,{0},{1:.3f}".format(len(fifties), len(fifties)/total)
print "   60-69,{0},{1:.3f}".format(len(sixties), len(sixties)/total)
print "   >= 70,{0},{1:.3f}".format(len(seventies), len(seventies)/total)


partition = int(width/2.)
z_sub = z_data[:partition,:]
width, height = z_sub.shape
x_data = numpy.linspace(0, 1500, num=width)
y_data = numpy.linspace(start=0, stop=3000, num=height)
x_data, y_data = numpy.meshgrid(y_data, x_data)


output = 'figures/sub_set.png'
figure=plt.figure()
axe = figure.gca()
c_data = axe.contour(y_data, x_data, z_sub)
axe.clabel(c_data)
axe.set_title("Contour Map (Left Half)")
figure.savefig(output)
print ".. figure:: " + output
print "   :scale: 75%"


output = 'figures/sub_scatter.png'
figure=plt.figure()
axe = figure.gca()

data_10 = numpy.where(z_sub < 10)
data_70 = numpy.where(z_sub >= 70)
colors = 'black red'.split()
data = (data_10, data_70)

axe.scatter(data_10[0] * 50, data_10[1] * 50,
                edgecolors='black',
                facecolors='none')
axe.scatter(data_70[0] * 50, data_70[1] * 50,
                edgecolors='red',
                facecolors='none')

axe.axvline(max_index_x, color='r')
axe.axhline(max_index_y, color='r')

axe.axvline(min_index_x, color='b')
axe.axhline(min_index_y, color='b')
axe.set_xlim((0, 1500))
axe.set_ylim((0, 3000))
axe.set_title("Best and Worst (Left Side)")
figure.savefig(output)
print ".. figure:: " + output
print "   :scale: 75%"
print
print "   Best and worst throughput locations. Red indicates < 10 Mbits/second. Black indicates > 70 Mbits/second."


flat_data = numpy.reshape(z_sub, -1)
noughts = flat_data[flat_data < 10]
tens = flat_data[flat_data < 20]
tens = tens[tens >= 10]
twenties = flat_data[flat_data < 30]
twenties = twenties[twenties >= 20]
thirties = flat_data[flat_data < 40]
thirties = thirties[thirties >= 30]
forties = flat_data[flat_data < 50]
forties = forties[forties >= 40]
fifties = flat_data[flat_data >= 50]
fifties = fifties[fifties < 60]
sixties = flat_data[flat_data >=60]
sixties = flat_data[sixties < 70]
seventies = flat_data[flat_data >= 70]

total = float(len(flat_data))
print "   0-9,{0},{1:.3f}".format(len(noughts), len(noughts)/total)
print "   10-19,{0},{1:.3f}".format(len(tens), len(tens)/total)
print "   20-29,{0},{1:.3f}".format(len(twenties), len(twenties)/total)
print "   30-39,{0},{1:.3f}".format(len(thirties), len(thirties)/total)
print "   40-49,{0},{1:.3f}".format(len(forties), len(forties)/total)
print "   50-59,{0},{1:.3f}".format(len(fifties), len(fifties)/total)
print "   60-69,{0},{1:.3f}".format(len(sixties), len(sixties)/total)
print "   >= 70,{0},{1:.3f}".format(len(seventies), len(seventies)/total)


bandwidths = pandas.read_csv('data/solution_bandwidths.csv')
description = bandwidths.Bandwidth.describe()


for name in description.index:
    print "   {0},{1}".format(name, description.ix[name])


output = 'figures/bandwidths_kde.png'
if not os.path.isfile(output):
    figure = plt.figure()
    axe = figure.gca()
        
    bandwidths.Bandwidth.hist(ax=axe, alpha=0.25, color='k', normed=1)
    bandwidths.Bandwidth.plot(kind='kde', ax=axe, alpha=0.5, color='b',
                              title='Best Bandwidth Solutions Found')
        
    axe.axvline(numpy.median(flat_data), color='r', alpha=0.5)
    axe.set_xlabel("Throughput (Mb/s)")
        
    figure.savefig(output)
print '.. figure:: ' + output
print "   :scale: 75%"


trials = 10**5
n = len(bandwidths)
samples = numpy.random.choice(bandwidths.Bandwidth,
                              size=(n, trials))
means = samples.mean(axis=0)
alpha = 0.01
p = alpha/2

low = numpy.percentile(means, p)
high = numpy.percentile(means, 1-p)


print "**99% Confidence Interval:** ({0}, {1})".format(low, high)


repetitions = 0
out_file = "data/best_repetitions_counts.csv"
with open(out_file, 'w') as w:
    w.write("TemperatureCount\n")
    for line in open("data/initial_temperatures.log"):
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
samples = numpy.random.sample(runtimes, size=(len(runtimes), trials))
means = samples.mean(axis=0)
low = numpy.percentile(means, p)
high = numpy.percentile(means, 1-p)
print "**99% Confidence Interval:** ({0:.2f}, {1:.2f})".format(low, high)


output = 'figures/runtime_kde.png'
if not os.path.isfile(output):
    figure = plt.figure()
    axe = figure.gca()
        
    counts.TemperatureCount.hist(ax=axe, alpha=0.25, color='k', normed=1)
    counts.TemperatureCount.plot(kind='kde', ax=axe, alpha=0.5, color='b',
                                 title='Iperf Run Counts')
        
    axe.axvline(numpy.median(flat_data), color='r', alpha=0.5)
    axe.set_xlabel("Number of Throughput Checks")
        
    figure.savefig(output)
print '.. figure:: ' + output
print "   :scale: 75%"

