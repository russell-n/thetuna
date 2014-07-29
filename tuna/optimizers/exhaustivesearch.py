
# third party
import numpy


class ExhaustiveSearch(object):
    """
    An exhaustive grid searcher
    """    
    def __init__(self, minima, maxima, increments, quality):
        """
        ExhaustiveSearch constructor

        :param:

         - `minima`: array of lowest-values for coordinates
         - `maxima`: array of maximum-values for coordinates
         - `increment`: array of step-sizes for coordinate-changes
        """
        self.minima = minima
        self.maxima = maxima
        self.increments = increments
        self.quality = quality
        return

    def carry(self, candidate):
        """
        Carries the column values if they exceed maxima

        :return: candidate with values carried-over
        """
        last_column = len(candidate) - 1
        for column in xrange(len(candidate)):
            if candidate[column] > self.maxima[column]:
                if column == last_column and self.bounded:
                    candidate[column] = self.maxima[column]
                else:
                    candidate[column] = self.minima[column]
                if column != last_column:
                    candidate[column+1] += self.increments[column+1]
        return candidate
        

    def __call__(self):
        """
        Starts the search

        :return: best value found
        """
        candidate = self.minima
        increment = numpy.zeros(len(candidate))
        increment[0] = self.increments[0]
        best = candidate[:]
        while candidate != self.maxima:
            candidate += increment
            candidate = self.carry(candidate)
            if self.quality(candidate) > self.quality(best):
                best = candidate
        return best
# end ExhaustiveSearch    