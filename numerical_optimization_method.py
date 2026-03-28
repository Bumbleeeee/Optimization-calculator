from abc import ABC, abstractmethod
from typing import List
import sympy
import helpers
import numpy as np

MAX_ITERS = 200 # to avoid infinite loop when an algo is run with initial conditions that don't converge

class NumericalOptimizationMethod(ABC):

    def __init__(self, function):
        self.expression = function
        self.iter_num = 1
        self.previous_iterates: List[List[float]] = [] # each element is a list to support multidim


    def run_method(self):
        self.store_current_iterate() # store initial point

        for self.iter_num in range(self.iter_num, MAX_ITERS):
            self.method_iteration()
            self.store_current_iterate() # store new point

            #print(f"iteration {self.iter_num}")
            if self.check_end_conditions(): break

        return self.get_cur_iterate()

    # perform one iteration of a method
    # this method should take the point from the previous iteration and store it at the beginning
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
    def get_cur_iterate(self) -> List[float]:
        pass

    @abstractmethod
    def store_current_iterate(self) -> None:
        pass

    @abstractmethod
    def get_variables(self) -> tuple:
        pass


    def plot_func_vs_iter(self) -> None:
        # draw plot of iteration k vs function value f(x_k) for {x_k : kth iteration} the previous iterates
        var_tuple = self.get_variables()
        lambda_f = sympy.lambdify(var_tuple, self.expression, modules="numpy")

        x_vals = list(range(len(self.previous_iterates))) #start at 0 b/c plotting user-inputted start point
        y_vals = []
        mins_set = False # linear threshold for symlog axis scale
        min_abs_f = 1
        min_f = 1

        for point in self.previous_iterates:
            # convert to numpy array of floats otherwise doesn't work with the numpy trig
            f_x = lambda_f(*np.array(point).astype(float))
            y_vals.append(f_x)

            # get min value for symlog linear range
            if not mins_set:
                min_abs_f = abs(f_x)
                min_f = f_x
                mins_set = True
            else:
                min_abs_f = min(min_abs_f, abs(f_x))
                min_f = min(min_f, f_x)

        helpers.draw(x_vals, y_vals, min_f, min_abs_f)


    def print_result(self):
        point = self.get_cur_iterate()
        print(f"\nApproximate optimal solution: {point}")

        var_tuple = self.get_variables()
        subs_dict = {}
        for i in range(len(point)):
            subs_dict[var_tuple[i]] = point[i]

        print(f"Approximate optimal value: {self.expression.evalf(subs=subs_dict)}")


