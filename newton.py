import sympy
from abc import ABC
from numerical_optimization_method import NumericalOptimizationMethod
import sys
import helpers
from typing import List

x = sympy.symbols('x') #TODO: this needs to change


# TODO: this whole class of algs could really be a subset of something else, but fine for now
class NewtonAlg(NumericalOptimizationMethod, ABC):
    point: float = None
    new_point: float  # this stores the most recently calculated iterate

    def __init__(self, function, start_point: float, end_conditions):
        super().__init__(function)
        self.new_point = start_point
        self.end_cond_func, self.end_cond_val = end_conditions


    def check_end_conditions(self) -> bool:
        return helpers.check_end_conditions(self.end_cond_func, self.end_cond_val,
                                            [self.point], [self.new_point],
                                            self.iter_num)


    def get_cur_iterate(self) -> List[float]:
        return [self.new_point]

    def store_current_iterate(self) -> None:
        self.previous_iterates.append([self.new_point])

    def get_variables(self) -> tuple:
        return sympy.symbols('x', seq=True)



class NewtonOptimizationMethod(NewtonAlg):

    def __init__(self, function, start_point: float, end_conditions):
        super().__init__(function, start_point, end_conditions)


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

    def __init__(self, function, start_point: float, end_conditions):
        super().__init__(function, start_point, end_conditions)


    def method_iteration(self):
        self.point = self.new_point

        fx = self.expression.evalf(subs={x: self.point})
        dfx = sympy.diff(self.expression, x).evalf(subs={x: self.point})

        # TODO: look into a better way to handle this - try to return last valid point
        if dfx == 0:
            print("Error - divide byt zero.")
            sys.exit()

        self.new_point = self.point - (fx / dfx)  # TODO: maybe want to chop

