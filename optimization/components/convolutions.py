
# third-party
import numpy


class UniformConvolution(object):
    """
    A bounded uniform convolver
    """
    def __init__(self, half_range, lower_bound, upper_bound):
        """
        UniformConvolution constructor

        :param:

         - `half_range`: (-half_range, half_range) bounds the noise
         - `lower_bound`: minimum value to allow in convolved arrays
         - `upper_bound`: maximum value to allow in convolved array
        """
        self.half_range = half_range
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        return

    def __call__(self, vector):
        """
        adds random noise, bounded by the lower and upper bound values
        """
        tweak = numpy.random.uniform(low=-self.half_range,
                                     high=self.half_range,
                                     size=len(vector))
        tweaked = vector + tweak
        return tweaked.clip(self.lower_bound, self.upper_bound)
# end UniformConvolution    
