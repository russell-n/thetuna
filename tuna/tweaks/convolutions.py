
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
                 mean=0, standard_deviation=1, number_type=float):
        """
        GaussianConvolution constructor

        :param:

         - `lower_bound`: minimum value to allow in tweaked arrays
         - `upper_bound`: maximum value to allow in tweaked arrays
         - `mean`: Center of the distribution
         - `standard_deviation`: Spread of the distribution
         - `number_type`: type to cast random vector to
        """
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.number_type = number_type
        return

    def set_seed(self, seed):
        """
        Sets the numpy random seed (for reproducibility)
        """
        numpy.random.seed(seed)
        return

    def __call__(self, vector):
        """
        Adds normally distributed random noise to the vector

        Casts the tweak values to type specified by self.number_type

        :return: vector + noise, bounded by upper and lower bounds
        """
        tweak = numpy.random.normal(loc=self.mean,
                                    scale=self.standard_deviation,
                                    size=len(vector)).astype(self.number_type)
        tweaked = vector + tweak
        return tweaked.clip(self.lower_bound, self.upper_bound)
# class GaussianConvolution        


if __name__ == '__builtin__':
    gaussian = GaussianConvolution(lower_bound=-100,
                                   upper_bound=100)
    candidate = numpy.array([5,6])
    print gaussian(candidate)

    # change the candidate, move the mean up, widen the distribution
    gaussian.standard_deviation = 20
    gaussian.mean = 5
    candidate = numpy.array([0, 1, 2])
    gaussian.number_type = int
    print gaussian(candidate)

    # clip the values so it's right-skewed
    gaussian.lower_bound = 5
    gaussian.upper_bound = 100
    print gaussian(candidate)