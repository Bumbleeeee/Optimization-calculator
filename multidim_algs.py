import sympy

import helpers
from numerical_optimization_method import NumericalOptimizationMethod
from abc import ABC
import step_size_algorithms

x, y, z = sympy.symbols('x y z')
# note the use of point-direction-stepsize so individual iterations should probably handle the step size
# the method func probably only handles the type
#       (just pass through to iter which delegates the step size work elsewhere right before returning)
# user should be able to enter a number, function, OR choose optimal step size
# WHEN ENTERING A FUNCTION NOTE THE ITER NUM STARTS AT 1 -- need to make this clear


def get_step_size_input():
    while True:
        step_size = input("\nEnter step size. "
                         "\nIt can be a constant, a function of 'x' - the iteration number (starting at 1), "
                         "\nor type 'optimal' to use the optimal step size at each iteration: ")
        if step_size.lower() == 'optimal':
            step_size = sympy.oo
            break
        else:
            step_size = sympy.sympify(step_size)
            # eval at 1 should be safe since first iter must evaluate at 1
            if sympy.ask(sympy.Q.real(step_size.evalf(subs={x: 1}))):
                break
            else:
                print("\nPlease enter a valid step size.")

    return step_size


class MultiDimAlg(NumericalOptimizationMethod, ABC):
    point: sympy.Matrix = None
    new_point: sympy.Matrix # this stores the most recently calculated iterate

    def __init__(self, function, step_size_func, start_point: sympy.Matrix, end_conditions):
        super().__init__(function)
        self.step_size_func = step_size_func
        self.new_point = start_point
        self.symbols: tuple = self.create_symbols()
        self.end_cond_func, self.end_cond_val = end_conditions



    def check_end_conditions(self) -> bool:
        return helpers.check_end_conditions(self.end_cond_func, self.end_cond_val,
                                            self.point.flat(), self.new_point.flat(),
                                            self.iter_num)


    def get_cur_iterate(self):
        return self.new_point

    def store_current_iterate(self) -> None:
        self.previous_iterates.append(self.new_point.flat())

    def get_variables(self) -> tuple:
        return self.symbols


    # TODO: not really a good place for this, but works for now
    # creates symbols x_1, ..., x_n to standardize the symbols used
    def create_symbols(self) -> tuple:
        var_string = " ".join(f"x_{i+1}" for i in range(self.new_point.__len__()))
        x_symbols = sympy.symbols(var_string, seq=True) # tuple

        # replace x,y,z with x_1, x_2, x_3 if present
        xyz_list = [x, y, z]
        for i in range(min(self.new_point.__len__(), 3)):
            self.expression = self.expression.subs(xyz_list[i], x_symbols[i])

        return x_symbols



class GradientMethod(MultiDimAlg):

    def __init__(self, function, step_size_func, start_point: sympy.Matrix, end_conditions):
        super().__init__(function, step_size_func, start_point, end_conditions)


    # perform one gradient method iteration
    def method_iteration(self):
        self.point = self.new_point

        # TODO: doing this every time is a waste
        variables = self.symbols
        subs_dict = {}
        for i in range(len(variables)):
            subs_dict[variables[i]] = self.point[i]

        gradient = sympy.Matrix([self.expression]).jacobian(variables).T

        # handle different step size methods
        if self.step_size_func == sympy.oo:
            step_size_num = step_size_algorithms.armijo_backtracking_alg(self.expression, self.point, variables)
        else:
            step_size_num = self.step_size_func.evalf(subs={x: self.iter_num})

        self.new_point = self.point - gradient.evalf(subs=subs_dict) * step_size_num



