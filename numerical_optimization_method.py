from abc import ABC, abstractmethod
import helpers

MAX_ITERS = 1000 # to avoid infinite loop when an algo is run with initial conditions that don't converge

class NumericalOptimizationMethod(ABC):

    def __init__(self):
        self.expression = helpers.get_func_to_optimize()
        self.iter_num = 0

    # TODO: do i want to store points here??? maybe iteration number
    def run_method(self):
        for self.iter_num in range(MAX_ITERS):
            self.method_iteration()
            if self.check_end_conditions(): break
        return self.get_point()

    # perform one iteration of a method
    @abstractmethod
    def method_iteration(self):
        pass

    # check if end conditions are satisfied
    @abstractmethod
    def check_end_conditions(self):
        pass

    # return current point (numerical approximation of optimal value)
    # TODO: what if we are dealing with intervals i.e. one dimensional algorithms
    @abstractmethod
    def get_point(self):
        pass

