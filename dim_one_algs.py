import sympy
from abc import ABC
from numerical_optimization_method import NumericalOptimizationMethod
import helpers
from typing import Callable

x = sympy.symbols('x')
PHI = (3-sympy.sqrt(5)) / 2

def get_range():
    while True:
        try:
            a = float(input("Enter the left end of the search interval: "))
            break
        except ValueError:
            print("Invalid input, please enter a real number")

    while True:
        try:
            b = float(input("Enter the right end of the search interval: "))
            break
        except ValueError:
            print("Invalid input, please enter a real number")

    return min(a, b), max(a, b) # swaps a and b if user entered right then left


# TODO: this is a common func it seems like, see where else we have smth similar
def get_num_iters():
    while True:
        try:
            a = abs(int(input("Enter the number of iterations: ")))
            break
        except ValueError:
            print("Invalid input, please enter an integer")


    return a

def get_epsilon():
    while True:
        try:
            a = abs(float(input("Enter a value for epsilon. If unsure, use 0.05: ")))
        except ValueError:
            print("Invalid input, please enter a real number")
        else:
            if a >= 0 or a <= 0.5: break
            print("Invalid input, please enter a number in the interval [0, 0.5]")

    return a


# TODO: delete once testing is successful
'''
def fibonacci_iter(f, a, b, rho):
    a1 = a + rho * (b-a)
    b1 = a + (1-rho) * (b-a)
    fa1 = f.evalf(subs={x: a1})
    fb1 = f.evalf(subs={x: b1})

    if fa1 > fb1:
        return a1, b
    else:
        return a, b1


def fibonacci_search(f, a, b, num_iters=10, epsilon=0.05):
    fib_numbers = [1, 1] # fibNumbers[i] = ith fibonacci number
    for i in range(2, num_iters+2):
        fib_numbers.append(fib_numbers[i-1] + fib_numbers[i-2])

    for i in range(num_iters):
        rho_i = 1 - (fib_numbers[num_iters-i] / fib_numbers[num_iters-i+1])
        if i == num_iters-1:
            rho_i -= epsilon

        a, b = fibonacci_iter(f, a, b, rho_i)

    return a, b
'''


class DimOneAlg(NumericalOptimizationMethod, ABC):
    interval: tuple = None
    new_interval: tuple
    end_cond_func: Callable = None # TODO: not really a fan of this but i guess it works
    end_cond_val: float

    def __init__(self):
        super().__init__()
        self.new_interval = get_range()


    # TODO: need to be careful here b/c interval, not point, but should be OK for now since only one coord changes
        # TODO: at a time - although may not get the intended behavior with a given end condition
    # TODO: if all is well, maybe check_end_conditions can be a helper func since impl seems similar in all methods
    def check_end_conditions(self):
        ret_val = False
        if self.end_cond_func is None:
            if self.iter_num >= self.end_cond_val:
                ret_val = True
        elif self.end_cond_func(self.interval, self.new_interval) <= self.end_cond_val:
            ret_val = True

        return ret_val


    def get_point(self):
        return self.new_interval



class GoldenSectionSearch(DimOneAlg):

    def __init__(self):
        super().__init__()
        self.end_cond_func, self.end_cond_val = helpers.get_end_condition()


    # TODO: is it necessary to evaluate phi - can we wait until the end?
    def method_iteration(self):
        self.interval = self.new_interval
        a = self.interval[0]
        b = self.interval[1]

        phi_approx = PHI.evalf()
        x1 = a + phi_approx * (b - a)
        x2 = a + (1 - phi_approx) * (b - a)
        f1 = self.expression.evalf(subs={x: x1})
        f2 = self.expression.evalf(subs={x: x2})

        if f1 > f2:
            self.new_interval = x1, b
        else:
            self.new_interval = a, x2



class BisectionSearch(DimOneAlg):

    def __init__(self):
        super().__init__()
        self.end_cond_func, self.end_cond_val = helpers.get_end_condition()


    def method_iteration(self):
        self.interval = self.new_interval
        a = self.interval[0]
        b = self.interval[1]

        # works on the assumption that f'(a) < 0, f'(b) > 0
        midpoint = (a + b) / 2.0
        dfx = self.expression.diff(x).evalf(subs={x: midpoint})

        ret_tup: tuple
        if dfx < 0:
            ret_tup = midpoint, b
        elif dfx > 0:
            ret_tup = a, midpoint
        else:
            ret_tup = midpoint, midpoint

        self.new_interval = ret_tup



class FibonacciSearch(DimOneAlg):
    # TODO: should the user be able to choose epsilon?
    # TODO: what about number of iterations - given that this is a necessity for the method
    fib_numbers: list

    def __init__(self):
        super().__init__()
        # figure out number of iters then precompute fib numbers
        self.end_cond_val: int = get_num_iters()
        self.compute_fib_nums()
        self.epsilon = get_epsilon()


    def method_iteration(self):
        # need to know current iteration (we do, 0 indexed)
        self.interval = self.new_interval
        a = self.interval[0]
        b = self.interval[1]
        num_iters = self.end_cond_val

        rho = 1 - (self.fib_numbers[num_iters - self.iter_num] / self.fib_numbers[num_iters - self.iter_num + 1])
        if self.iter_num == num_iters - 1:
            rho -= self.epsilon

        a1 = a + rho * (b - a)
        b1 = a + (1 - rho) * (b - a)
        fa1 = self.expression.evalf(subs={x: a1})
        fb1 = self.expression.evalf(subs={x: b1})

        if fa1 > fb1:
            self.new_interval = a1, b
        else:
            self.new_interval = a, b1


    def compute_fib_nums(self):
        num_iters = self.end_cond_val

        fib_numbers = [1, 1]  # fibNumbers[i] = ith fibonacci number
        for i in range(2, num_iters + 2):
            fib_numbers.append(fib_numbers[i - 1] + fib_numbers[i - 2])

        self.fib_numbers = fib_numbers

