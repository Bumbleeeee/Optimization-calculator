import sympy
from abc import ABC
from numerical_optimization_method import NumericalOptimizationMethod
import helpers
import sys

x = sympy.symbols('x')


def newton_start_point():
    while True:
        try:
            start_point = float(input("Enter a starting point: "))
            return start_point
        except ValueError:
            print("Invalid input, please enter a real number")


# TODO: this whole class of algs could really be a subset of something else, but fine for now
class NewtonAlg(NumericalOptimizationMethod, ABC):
    point: float = None
    new_point: float  # this stores the most recently calculated iterate

    def __init__(self):
        super().__init__()
        self.new_point = newton_start_point()
        self.end_cond_func, self.end_cond_val = helpers.get_end_condition()


    def check_end_conditions(self) -> bool:
        ret_val = False
        if self.end_cond_func is None:
            if self.iter_num >= self.end_cond_val:
                ret_val = True
        elif self.end_cond_func([self.point], [self.new_point]) <= self.end_cond_val:
            ret_val = True

        return ret_val


    def get_point(self):
        return self.new_point



class NewtonOptimizationMethod(NewtonAlg):

    def __init__(self):
        super().__init__()


    def method_iteration(self):
        self.point = self.new_point

        df = sympy.diff(self.expression, x)
        dfx = df.evalf(subs={x: self.point})
        d2f = sympy.diff(df, x)
        d2fx = d2f.evalf(subs={x: self.point})

        #TODO: look into a better way to handle this - try to return last valid point
        if d2fx == 0:
            print("Error - divide by zero.")
            sys.exit()

        self.new_point = self.point - (dfx / d2fx)  #TODO: maybe want to chop


class NewtonRootFindingMethod(NewtonAlg):

    def __init__(self):
        super().__init__()


    def method_iteration(self):
        self.point = self.new_point

        fx = self.expression.evalf(subs={x: self.point})
        dfx = sympy.diff(self.expression, x).evalf(subs={x: self.point})

        # TODO: look into a better way to handle this - try to return last valid point
        if dfx == 0:
            print("Error - divide byt zero.")
            sys.exit()

        self.new_point = self.point - (fx / dfx)  # TODO: maybe want to chop

