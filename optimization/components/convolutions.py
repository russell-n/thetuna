
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


class GaussianConvolution(object):
    """
    A Tweak that uses the Normal distribution
    """
    def __init__(self, lower_bound, upper_bound,
                 mean=0, standard_deviation=1):
        """
        GaussianConvolution constructor

        :param:

         - `lower_bound`: minimum value to allow in tweaked arrays
         - `upper_bound`: maximum value to allow in tweaked arrays
         - `mean`: Center of the distribution
         - `standard_deviation`: Spread of the distribution
        """
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.mean = mean
        self.standard_deviation = standard_deviation
        return

    def __call__(self, vector):
        """
        Adds normally distributed random noise to the vector

        :return: vector + noise, bounded by upper and lower bounds
        """
        tweak = numpy.random.normal(loc=self.mean,
                                    scale=self.standard_deviation,
                                    size=len(vector))
        tweaked = vector + tweak
        return tweaked.clip(self.lower_bound, self.upper_bound)
# class GaussianConvolution        
