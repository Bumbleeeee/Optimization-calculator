from math import inf, isclose
import sympy as sy
from typing import Callable
from helpers import compute_gradient
from dataclasses import dataclass

MAX_STEPSIZE_ITERS = 100

@dataclass
class ExtraFuncData:
    # store common data for step size algorithms in one place
    gradient: Callable #sympy lambdified func
    cur_point: sy.Matrix
    search_direction: sy.Matrix


# TODO: want to be able to customize search direction?? also check to ensure descent direction

def armijo_backtracking_alg(func: sy.Function, point: sy.Matrix, var_list: tuple, alpha = 1.0, decrement = 0.75):
    # Armijo Backtracking algorithm (guaranteed to terminate for continuously differentiable functions)

    f_lambda = sy.lambdify(var_list, func, modules=["sympy"])
    gradient = compute_gradient(func, var_list)
    grad_lambda = sy.lambdify(var_list, gradient, modules=["sympy"])
    neg_grad_dir = -1 * grad_lambda(*point)

    for i in range(MAX_STEPSIZE_ITERS):
        if check_armijo_condition(f_lambda, ExtraFuncData(grad_lambda, point, neg_grad_dir), alpha):
            break
        else:
            alpha *= decrement

    return alpha



def check_armijo_condition(func: Callable, fd: ExtraFuncData, step_length: float, c_1 = 1e-4):
    f_x = func(*fd.cur_point) # '*' to unpack the list into separate args
    f_xap = func(*(fd.cur_point + step_length*fd.search_direction))
    g_x = fd.gradient(*fd.cur_point)

    step = c_1 * step_length * fd.search_direction.T @ g_x # '@' does matrix mult
    # 1x1 matrix so just take top element to get a float
    step_float = sy.Float(step[0,0].evalf())

    return f_xap <= f_x + step_float



def check_wolfe_condition(fd: ExtraFuncData, step_length: float, c_2 = 0.1):
    g_x = fd.gradient(*fd.cur_point)
    g_xap = fd.gradient(*(fd.cur_point + step_length*fd.search_direction))

    lhs_float = sy.Float((fd.search_direction.T @ g_xap)[0,0].evalf())
    rhs_float = sy.Float((c_2 * fd.search_direction.T @ g_x)[0,0].evalf())
    return lhs_float >= rhs_float


def check_strong_wolfe_condition(fd: ExtraFuncData, step_length: float, c_2 = 0.1):
    # TODO: use for quasi-newton and conjugate gradient, too strong for arbitrary gradient
    g_x = fd.gradient(*fd.cur_point)
    g_xap = fd.gradient(*(fd.cur_point + step_length*fd.search_direction))

    lhs_float = sy.Float((fd.search_direction.T @ g_xap)[0, 0].evalf())
    rhs_float = sy.Float((c_2 * fd.search_direction.T @ g_x)[0, 0].evalf())
    return abs(lhs_float) <= abs(rhs_float)


#TODO: look into Nocedal and Wright algo (uses func value check as well i thinK)

def armijo_wolfe_bisection(func: Callable, fd: ExtraFuncData, alphas: tuple = (0, 1, 1e10)) -> float:
    # bisection style algorithm for bracketing and zooming to find a point satisfying Armijo and Wolfe conditions
    # alphas = (a_0, a_1, a_max)
    alpha: list = list(alphas)
    while not isclose(alpha[1], alpha[2], rel_tol=1e-9):
        if not check_armijo_condition(func, fd, alpha[1]):
            # step too large
            alpha[2] = alpha[1]
            alpha[1] = (alpha[2] + alpha[0]) / 2
        elif not check_wolfe_condition(fd, alpha[1]):
            # step too small
            alpha[0] = alpha[1]
            if alpha[2] == inf:
                alpha[1] = 2*alpha[1]
            else:
                alpha[1] = (alpha[0] + alpha[2]) / 2
        else:
            break

    return alpha[1]


def armijo_wolfe_alg(func: sy.Function, point: sy.Matrix, var_list: tuple, initial_alphas: tuple = (0, 1, 1e10)):
    f_lambda = sy.lambdify(var_list, func, modules=["sympy"])
    gradient = compute_gradient(func, var_list)
    grad_lambda = sy.lambdify(var_list, gradient, modules=["sympy"])
    neg_grad_dir = -1 * grad_lambda(*point)

    alpha = armijo_wolfe_bisection(f_lambda, ExtraFuncData(grad_lambda, point, neg_grad_dir), initial_alphas)
    return alpha