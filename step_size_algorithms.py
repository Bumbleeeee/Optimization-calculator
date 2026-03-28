import sympy as sy
from typing import Callable
from helpers import compute_gradient
MAX_STEPSIZE_ITERS = 100
import time


def armijo_backtracking_alg(func, point, var_list: tuple, alpha = 1.0, decrement = 0.75):
    # Armijo Backtracking algorithm (guaranteed to terminate for continuously differentiable functions)

    f_lambda = sy.lambdify(var_list, func, modules=["sympy"])
    gradient = compute_gradient(func, var_list)
    grad_lambda = sy.lambdify(var_list, gradient, modules=["sympy"])
    neg_grad_dir = -1 * grad_lambda(*point)

    for i in range(MAX_STEPSIZE_ITERS):
        if check_armijo_condition(f_lambda, grad_lambda, point, neg_grad_dir, alpha):
            break
        else:
            alpha *= decrement

    return alpha



def check_armijo_condition(func: Callable, gradient: Callable, cur_point: sy.Matrix, search_direction: sy.Matrix,
                           step_length: float, c_1 = 1e-4):
    f_x = func(*cur_point) # '*' to unpack the list into separate args
    f_xap = func(*(cur_point + step_length*search_direction))
    g_x = gradient(*cur_point)

    step = c_1 * step_length * search_direction.T @ g_x # '@' does matrix mult
    # 1x1 matrix so just take top element to get a float
    step_float = sy.Float(step[0,0].evalf()) #TODO: might break when I add support for pi and other constants b/c I think they need to be evaluated to become sy.Float type

    return f_xap <= f_x + step_float



def check_wolfe_condition(gradient: Callable, cur_point: sy.Matrix, search_direction: sy.Matrix,
                          step_length: float, c_2 = 0.1):
    #TODO: use for quasi-newton and conjugate gradient, too strong for arbitrary gradient
    # TODO: convert to sy.Float as above
    g_x = gradient(*cur_point)
    g_xap = gradient(*(cur_point + step_length*search_direction))
    return search_direction.T * g_xap >= c_2 * search_direction.T * g_x