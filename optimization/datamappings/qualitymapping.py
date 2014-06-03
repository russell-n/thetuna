
class QualityMapping(object):
    """
    A QualityMapping from a domain to an image (range)
    """
    def __init__(self, mapping, domain=None, ideal=None,
                 maxima=True):
        """
        QualityMapping constructor

        :param:

         - `mapping`: function to map inputs to an output (Quality function)
         - `domain`: vector of valid inputs for the mapping-function
         - `ideal`: Value that for the ideal solution
         - `maxima`: if true and ideal is calculated, use max value, else min-value
        """
        self.domain = domain
        self.mapping = mapping
        self._ideal = ideal
        self.maxima = maxima
        self._image = None
        return

    @property
    def ideal(self):
        """
        The ideal value (if it is knowable)
        """
        if self._ideal is None and self.domain is not None:
            if self.maxima:
                self._ideal = self.image.max()
            else:
                self._ideal = self.image.min()
        return self._ideal

    @ideal.setter
    def ideal(self, ideal):
        """
        sets the ideal value

        :param:

         - `ideal`: stopping-value
        """
        self._ideal = ideal
        return self._ideal

    @property
    def image(self):
        """
        The image (range) for the domain and mapping-function

        :precondition: domain has valid input for mapping-function        
        """
        if self._image is None and self.domain is not None:
            self._image = self.mapping(self.domain)
        return self._image

    def __call__(self, argument):
        """
        maps the argument to the image

        :param:

         - `argument`: valid input for the mapping function

        :return: mapping(argument)
        """
        return self.mapping(argument)        
# end QualityMapping    
