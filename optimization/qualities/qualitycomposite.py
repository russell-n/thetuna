
# this package
from optimization.components.component import Composite


class QualityComposite(Composite):
    """
    A quality for the optimizer
    """
    def __call__(self, *args, **kwargs):
        """
        Calls the components, passing along the arguments

        :return: last output from the components not None
        """
        output = None
        for component in self.components:
            returned = component(*args, **kwargs)
            if returned is not None:
                output = returned
        return output
# end QualityComposite    
