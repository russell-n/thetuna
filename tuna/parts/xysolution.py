
# python standard library
import itertools
# third-party
import numpy

# this package
from tuna import BaseClass


class XYSolution(object):
    """
    A holder for n-space solutions
    """
    def __init__(self, inputs, output=None):
        """
        XY Solution constructor

        :param:

        - `inputs`: collection of inputs
        - `output`: value mapped to the inputs
        """
        self.inputs = inputs
        self.output = output
        return

    def __eq__(self, other):
        """
        Equality

        :return: self.output == other.output
        """
        return self.output == other.output

    def __le__(self, other):
        """
        self.output <= other.output
        """
        return self.output <= other.output

    def __ge__(self, other):
        """
        self.output >= other.output
        """
        return self.output >= other.output

    def __lt__(self, other):
        """
        Less than
        """
        return self.output < other.output

    def __add__(self, other):
        """
        Assumes the `other` value is a numpy array

        :return: self.inputs + other
        """
        return self.inputs + other

    def __radd__(self, other):
        """
        Assumes the other value is a numpy array
        """
        return self.inputs + other

    def __sub__(self, other):
        """
        subtracts other from inputs
        """
        return self.inputs - other

    def __rsub__(self, other):
        """
        Subtracts inputs from other
        """
        return other - self.inputs

    def __mul__(self, other):
        """
        Returns product of inputs x other
        """
        return self.inputs * other

    def __rmul__(self, other):
        """
        Returns the product other x inputs
        """
        return other * self.inputs

    def __len__(self):
        """
        Return number of inputs
        """
        return len(self.inputs)

    def __getitem__(self, index):
        """
        Returns the domain value matching the index
        """
        return self.inputs[index]

    def __str__(self):
        return "Inputs: {0} Output: {1}".format(self.inputs, self.output)
# end XYSolution    


class XYTweak(BaseClass):
    """
    An adapter to the tweaks to return an XYSolution instead of an array
    """
    def __init__(self, tweak, size=2):
        """
        XYTweak constructor

        :param:

         - `tweak`: object that adds noise to an array
         - `size`: size of vector (used for getting initial candidate)
        """
        super(XYTweak, self).__init__()
        self.tweak = tweak
        self.size = size
        return

    def __call__(self, vector=None):
        """
        Tweaks the vector, then uses it as the domain for an XY Solution

        If none is given, just return a random vector
        """
        if vector is not None:
            tweaked = self.tweak(vector)
        else:
            # linear interpolation
            if hasattr(self.tweak, 'lower_bound'):
                min_value, max_value = self.tweak.lower_bound, self.tweak.upper_bound
                tweaked = (max_value - min_value) * numpy.random.sample(size=self.size) + min_value
                tweaked = tweaked.astype(self.tweak.number_type)
            else:
                x_min, x_max, y_min, y_max = self.tweak.x_min, self.tweak.x_max, self.tweak.y_min, self.tweak.y_max
                x = self.tweak.number_type((x_max - x_min) * numpy.random.sample() + x_min)
                y = self.tweak.number_type((y_max - y_min) * numpy.random.sample() + y_min)
                #x = max(x_min, x)b
                #x = min(x_max, x)
                #y = max(y_min, y)
                #y = min(y_max, y)
                tweaked = numpy.array([x, y])
        #self.logger.debug("Tweak: {0}".format(tweaked))
        return XYSolution(inputs=tweaked)


class XYSolutionGenerator(object):
    """
    A generator of candidate XYSolutions
    """
    def __init__(self, low, high, size=1, random_function=numpy.random.uniform,
                 repetitions=None):
        """
        XYSolutionGenerator constructor

        :param:

         - `low`: The low (or loc) for the random-function
         - `high`: The high (or scale) for the random-function
         - `size`: Size of the array to give the XYSolution
         - `random_function`: function to create initial XYSolution inputs
         - `repetitions`: number of candidates to generate (default: infinite)
        """
        self.low = low
        self.high = high
        self.size = size
        self.random_function = random_function
        self.repetitions = repetitions
        return

    @property
    def candidate(self):
        """
        A candidate XYSolution with random inputs
        """
        return XYSolution(self.random_function(self.low,
                                               self.high,
                                               self.size))

    def __iter__(self):
        """
        Yields XYSolution candidates
        """
        if self.repetitions is None:
            candidates = itertools.repeat(True)
        else:
            candidates = xrange(self.repetitions)
        for candidate in candidates:
            yield self.candidate
# end XYSolutionGenerator    
