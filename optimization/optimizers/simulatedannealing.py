
class SimulatedAnnealing(object):
    """
    a Simulated Annealing optimizer
    """
    def __init__(self, temperature_schedule, candidates, quality, candidate):
        """
        SimulatedAnnealing Constructor

        :param:

         - `temperature_schedule`: a generator of temperatures
         - `candidates`: a generator of candidate solutions
         - `quality`: Quality checker for candidates
         - `candidate`: initial candidate solution
        """
        self.temperature_schedule = temperature_schedule
        self.candidates = candidates
        self.quality = quality
        self.candidate = candidate
        return
# SimulatedAnnealing    


class TemperatureGenerator(object):
    """
    A class to generate temperature drops for the annealing
    """
    def __init__(self, start, stop=0, schedule=lambda x: x-1):
        """
        TemperatureGenerator constructor

        :param:

         - `start`: starting temperature
         - `stop`: stopping temperature
        """
        self.start = start
        self.stop = stop
        self.schedule = schedule
        return

    def __iter__(self):
        """
        Generates decreasing temperatures

        :yield: next temperature in the schedule
        """
        temperature = self.start
        while temperature >= self.stop:
            yield temperature
            temperature = self.schedule(temperature)
        return
# end class TemperatureGenerator    
