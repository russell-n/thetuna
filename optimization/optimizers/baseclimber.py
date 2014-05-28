
class BaseClimber(object):
    """
    The Base hill-climbing class
    """
    def __init__(self, tweak, quality, stop_condition,
                 solution):
        """
        BaseClimber constructor

        :param:

         - `solution`: initial candidate solution
         - `tweak`: callable that tweaks solutions
         - `quality`: callable that assesses solution quality
         - `stop_condition`: callable - returns true when stop condition met
        """
        self.solution = solution
        self.tweak = tweak
        self.quality = quality
        self.stop_condition = stop_condition
        return
# end BaseClimber    
