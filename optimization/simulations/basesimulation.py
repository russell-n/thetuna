
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

    def nearest_index(self, target):
        """
        Returns the index for the domain value that's closest to the target

        :param:

         - `target`: value within the range of the domain
        """
        return numpy.abs(self.domain - target).argmin()
# end BaseSimulation    
