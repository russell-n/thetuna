
# third party
import numpy

# this package
from optimization.datamappings.qualitymapping import QualityMapping


class SphereMapping(object):
    """
    Creates a Quality Mapping with spherical data
    """
    def __init__(self, start=-5.12, stop=5.12, steps=1000):
        """
        Sphere Mapping

        :param:

         - `start`: low-value for x and y
         - `stop`: high-value for x and y
         - `steps`: size of x and y
        """
        self._mapping = None
        self.start = start
        self.stop = stop
        self.steps = steps
        self._x = None
        self._y = None
        self._z = None
        return

    @property
    def x(self):
        """
        x-axis data
        """
        if self._x is None:
            self._x = numpy.linspace(self.start,
                               self.stop,
                               self.steps)
        return self._x

    @property
    def y(self):
        """
        2-d array (meshgrid for y-axis)
        """
        if self._y is None:
            self._y = numpy.linspace(self.start,
                               self.stop,
                               self.steps)
        return self._y

    @property
    def z(self):
        """
        2-d array (meshgrid for z-axis)
        """
        if self._z is None:
            if len(self.x.shape) == 1:
                # apply meshgrid
                self._x, self._y = numpy.meshgrid(self.x, self.y)
            self._z = self.x**2 + self.y**2
        return self._z

    @property
    def mapping(self):
        """
        Built QualityMapping
        """
        if self._mapping is None:
            mapping_function = lambda argument: numpy.sum(argument**2)
            self._mapping = QualityMapping(ideal=self.z.max(),
                                           mapping=mapping_function)
        return self._mapping
# end SphereMapping


two_pi = 2 * numpy.pi
def rastrigin(argument):
    return 10*len(argument) + numpy.sum(argument**2 - 10
                                        * numpy.cos(two_pi * argument))


class RastriginMapping(object):
    """
    Creates a Quality Mapping with the Rastrigin function
    """
    def __init__(self, start=-5.12, stop=5.12, steps=1000):
        """
        Rastrigin Mapping Constructor

        :param:

         - `start`: low-value for x and y
         - `stop`: high-value for x and y
         - `steps`: size of x and y
        """
        self._mapping = None
        self.start = start
        self.stop = stop
        self.steps = steps
        self._x = None
        self._y = None
        self._z = None
        return

    @property
    def x(self):
        """
        x-axis data
        """
        if self._x is None:
            self._x = numpy.linspace(self.start,
                               self.stop,
                               self.steps)
        return self._x

    @property
    def y(self):
        """
        2-d array (meshgrid for y-axis)
        """
        if self._y is None:
            self._y = numpy.linspace(self.start,
                               self.stop,
                               self.steps)
        return self._y

    @property
    def z(self):
        """
        2-d array (meshgrid for z-axis)
        """
        if self._z is None:
            if len(self.x.shape) == 1:
                
                # apply meshgrid
                self._x, self._y = numpy.meshgrid(self.x, self.y)
            self._z = (20 + (self.x**2-10 * numpy.cos(two_pi*self.x)) +
                       (self.y**2-10 * numpy.cos(two_pi*self.y)))
        return self._z

    @property
    def mapping(self):
        """
        Built QualityMapping
        """
        if self._mapping is None:
            self._mapping = QualityMapping(ideal=self.z.max(),
                                           mapping=rastrigin)
        return self._mapping
# end RastriginMapping
