
# third party
import numpy


class BaseSimulation(object):
    """
    A base simulated-data class
    """
    def __init__(self, domain_start, domain_end, domain_step):
        """
        BaseSimulation constructor

        :param:

         - `domain_start`: start of the range of domain data (x)
         - `domain_end`: end of the range of domain data (x)
         - `domain_step`: increment for steps from domain start to domain end
        """
        self.domain_start = domain_start
        self.domain_end = domain_end
        self.domain_step = domain_step
        self._domain = None
        self._range = None
        return

    @property
    def domain(self):
        """
        The x-values

        :rtype: numpy.array
        """
        if self._domain is None:
            self._domain = numpy.arange(self.domain_start,
                                        self.domain_end + self.domain_step,
                                        self.domain_step)
        return self._domain

    def nearest_domain_index(self, target):
        """
        Returns the index for the domain value that's closest to the target

        :param:

         - `target`: value within the range of the domain
        """
        return numpy.abs(self.domain - target).argmin()

    def reset(self):
        """
        Resets the properties to None
        """
        self._domain = None
        self._range = None
        self.domain_start = None
        self.domain_end = None
        self.domain_step = None
        return

    def __call__(self, target):
        """
        This is defined as the `nearest_range_value` so it can be used where the `Quality` function is expected

        :param:

         - `target`: a collection with 1-value to map to the range
        """
        index = numpy.abs(self.range - target[0]).argmin()
        return self.range[index]
# end BaseSimulation    
