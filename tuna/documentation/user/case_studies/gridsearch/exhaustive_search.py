
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


data_path = '../data/data_step50.csv'
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
tens = flat_data[(flat_data < 20) & (flat_data >=10)]
twenties = flat_data[(flat_data < 30) & (flat_data >= 20)]
thirties = flat_data[(flat_data < 40) & (flat_data >= 30)]
forties = flat_data[(flat_data < 50) & (flat_data >= 40)]
fifties = flat_data[(flat_data >= 50) & (flat_data < 60)]
sixties = flat_data[(flat_data >=60) & (flat_data < 70)]
seventies = flat_data[(flat_data >= 70)]


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


z_series = pandas.Series(flat_data)
description = z_series.describe()

for stat in description.index:
    print "   {0},{1:g}".format(stat, description.ix[stat])
