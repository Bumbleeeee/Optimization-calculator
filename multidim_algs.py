import sympy
import helpers
from numerical_optimization_method import NumericalOptimizationMethod
from abc import ABC

x, y, z = sympy.symbols('x y z')
# note the use of point-direction-stepsize so individual iterations should probably handle the step size
# the method func probably only handles the type
#       (just pass through to iter which delegates the step size work elsewhere right before returning)
# user should be able to enter a number, function, OR choose optimal step size
# WHEN ENTERING A FUNCTION NOTE THE ITER NUM STARTS AT 1 -- need to make this clear



def find_step_size(func, step_size_func, iter_num):
    if step_size_func == sympy.oo:
        #TODO: optimal step size
        # phi(a) = f(x - a*f'(x))
        # will be hard to do a perfectly optimal step size but could do smth like Armijo backtracking algorithm fairly easily
        # lots of conditions that can be used, page 4 of ch5
        return 0.25
    else:
        return step_size_func.evalf(subs={x: iter_num})


def input_point():
    while True:
        try:
            point_str = input("Enter a starting point. For multiple dimensions, separate with a space: ")
            point_list_str = point_str.split()
            point = []
            for p in point_list_str:
                point.append(float(p))
            return point
        except ValueError:
            print("Please enter real numbers for each coordinate.")


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

    def __int__(self):
        self.step_size_func = get_step_size_input()
        self.new_point = sympy.Matrix(input_point())
        self.symbols_list = self.create_symbols()
        self.end_cond_func, self.end_cond_val = helpers.get_end_condition()


    def check_end_conditions(self) -> bool:
        ret_val = False
        if self.end_cond_func is None:
            if self.iter_num >= self.end_cond_val:
                ret_val = True
        elif self.end_cond_func(self.point.flat(), self.new_point.flat()) <= self.end_cond_val:
            ret_val = True

        return ret_val


    def get_point(self):
        return self.new_point


    # TODO: not really a good place for this, but works for now
    # creates symbols x_1, ..., x_n to standardize the symbols used
    def create_symbols(self):
        var_string = " ".join(f"x_{i + 1}" for i in range(self.point.__len__()))
        x_symbols = sympy.symbols(var_string, seq=True)

        # replace x,y,z with x_1, x_2, x_3 if present
        xyz_list = [x, y, z]
        for i in range(min(self.point.__len__(), 3)):
            self.expression = self.expression.subs(xyz_list[i], x_symbols[i])

        return x_symbols



class GradientMethod(MultiDimAlg):

    def __init__(self):
        super().__init__()


    # perform one gradient method iteration
    def method_iteration(self):
        self.point = self.new_point

        variables = sympy.Matrix(self.symbols_list)
        subs_dict = {}
        for i in range(len(variables)):
            subs_dict[variables[i]] = self.point[i]

        gradient = sympy.Matrix([self.expression]).jacobian(variables).T
        step_size_num = find_step_size(self.expression, self.step_size_func, self.iter_num)

        self.new_point = self.point - gradient.evalf(subs=subs_dict) * step_size_num



