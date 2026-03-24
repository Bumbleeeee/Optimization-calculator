import sympy
from abc import ABC
from numerical_optimization_method import NumericalOptimizationMethod
import helpers
from typing import Callable, List

x = sympy.symbols('x') #TODO: can remove this but have to change all explicit substitutions
PHI = (3-sympy.sqrt(5)) / 2

def get_range() -> List[float]:
    a = helpers.input_multi_float("Enter the left end of the search interval: ")[0]
    b = helpers.input_multi_float("Enter the right end of the search interval: ")[0]

    return [min(a, b), max(a, b)] # swaps a and b if user entered right then left


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
        a = helpers.input_multi_float("Enter a value for epsilon. If unsure, use 0.05: ")[0]
        if 0 <= a <= 0.5: break
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
    interval: List[float] = None
    new_interval: List[float] # stores most recently calculated interval
    end_cond_func: Callable = None # TODO: not really a fan of this but i guess it works
    end_cond_val: float

    def __init__(self, function, start_interval: List[float]):
        super().__init__(function)
        self.new_interval = start_interval



    def check_end_conditions(self):
        return helpers.check_end_conditions(self.end_cond_func, self.end_cond_val,
                                            self.interval, self.new_interval,
                                            self.iter_num)


    def get_cur_iterate(self) -> List[float]:
        return list(self.new_interval)

    def store_current_iterate(self) -> None:
        midpoint = (self.new_interval[0] + self.new_interval[1]) / 2
        self.previous_iterates.append([midpoint])

    def get_variables(self) -> tuple:
        return sympy.symbols('x', seq=True)

    # override
    def print_result(self):
        print(f"\nInterval containing optimal solution: {self.new_interval}")

        midpoint = (self.new_interval[0] + self.new_interval[1]) / 2
        print(f"Midpoint approximate optimal value: {self.expression.evalf(subs={x: midpoint})}")



class GoldenSectionSearch(DimOneAlg):

    def __init__(self, function, start_interval: List[float], end_conditions):
        super().__init__(function, start_interval)
        self.end_cond_func, self.end_cond_val = end_conditions


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

    def __init__(self, function, start_interval: List[float], end_conditions):
        super().__init__(function, start_interval)
        self.end_cond_func, self.end_cond_val = end_conditions


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

    def __init__(self, function, start_interval: List[float], num_iters, epsilon):
        super().__init__(function, start_interval)
        # figure out number of iters then precompute fib numbers
        self.end_cond_val: int = num_iters
        self.compute_fib_nums()
        self.epsilon = epsilon


    def method_iteration(self):
        # need to know current iteration (we do, 1 indexed)
        self.interval = self.new_interval
        a = self.interval[0]
        b = self.interval[1]
        num_iters = self.end_cond_val

        rho = 1 - (self.fib_numbers[num_iters+2 - self.iter_num-1] / self.fib_numbers[num_iters+2 - self.iter_num])
        if self.iter_num == num_iters:
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

