
# third-party
import scipy
from scipy import stats
import matplotlib.pyplot as plt

# this package
from optimization.simulations.basesimulation import BaseSimulation


IN_PWEAVE = __name__ == '__builtin__'


class NormalSimulation(BaseSimulation):
    """
    Normal data
    """
    def __init__(self, functions=None, *args, **kwargs):
        """
        Normal Simulation constructor

        :param:

         - `functions`: functions to apply to the range (Y)
        """
        super(NormalSimulation, self).__init__(*args, **kwargs)
        self.functions = functions
        self._range = None
        return
    
    @property
    def range(self):
        """
        The y-values for the given x-values        
        """
        if self._range is None:
            self._range = stats.norm.pdf(self.domain)
            if self.functions is not None:
                for function in self.functions:
                    self._range += function(self.domain)
        return self._range
            
        
    @property
    def ideal_solution(self):
        """
        The maximal solution from our data set
        """
        return self.range.max()

    def __call__(self, target):
        """
        Gets the value of the height of the curve

        :param:

         - `target`: Solution object with inputs and output
        """
        if target.output is None:
            #target.output = scipy.stats.norm.pdf(target.inputs[0])
            # get the domain value closest to the input-value
            index = self.nearest_domain_index(target.inputs[0])
            # set it to the range value
            target.output = self.range[index]
        return target.output
# end NormalSimulation    


if IN_PWEAVE:
    simulator = NormalSimulation(domain_start=-4, domain_end=4, domain_step=0.1)


if IN_PWEAVE:
    output = 'figures/plot_normal.svg'
    figure = plt.figure()
    axe = figure.gca()
    axe.plot(simulator.domain, simulator.range)
    figure.savefig(output)
    print ".. figure:: "  + output


if IN_PWEAVE:
    simulator = NormalSimulation(domain_start=-100, domain_end=150, domain_step=0.1)    


if IN_PWEAVE:
    output = 'figures/plot_needle_in_haystack.svg'
    figure = plt.figure()
    axe = figure.gca()
    axe.plot(simulator.domain, simulator.range)
    figure.savefig(output)
    print ".. figure:: "  + output


class NoisySimulation(BaseSimulation):
    """
    A noisy data set
    """
    def __init__(self, functions=None, *args, **kwargs):
        """
        NoisySimulation constructor

        :param:

         - `functions`: list of extra functions to add noise
        """
        super(NoisySimulation, self).__init__(*args, **kwargs)
        self.functions = functions
        return

    @property
    def range(self):
        """
        the noisy data
        """
        if self._range is None:
            self._range = stats.norm.rvs(size=self.domain_end-self.domain_start + 1)
            if self.functions is not None:
                for function in self.functions:
                    self._range += function(self._range)
        return self._range
# end NoisySimulation        


if IN_PWEAVE:
    squared = lambda x: scipy.power(x, 2)
    sine = lambda x: scipy.sin(x)
    noisy = NoisySimulation(domain_start=0, domain_end=100, domain_step=1,
                            functions=[squared, sine])


if IN_PWEAVE:
    output = 'figures/noisy_data.svg'
    figure = plt.figure()
    axe = figure.gca()
    axe.plot(noisy.range)
    figure.savefig(output)
    print ".. figure:: " + output


if IN_PWEAVE:
    cosine_squared = lambda x: scipy.cos(x)**2
    sine = lambda x: -scipy.sin(x)
    simulator = NormalSimulation(domain_start=-4,
                                 domain_end=4.1,
                                 domain_step=0.1,
                                 functions=[cosine_squared, sine])


if IN_PWEAVE:
    output = 'figures/plot_local_optima.svg'
    figure = plt.figure()
    axe = figure.gca()

    axe.plot(simulator.range)
    figure.savefig(output)
    print ".. figure:: " + output
