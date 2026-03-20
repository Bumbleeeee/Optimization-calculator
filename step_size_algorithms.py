import sympy as sy
from typing import Callable


def armijo_backtracking_alg(func, point, var_list, alpha = 1.0, decrement = 0.75):
    # Armijo Backtracking algorithm (guaranteed to terminate for continuously differentiable functions)

    f_lambda = sy.lambdify(var_list, func)
    gradient = sy.Matrix([func]).jacobian(var_list).T
    grad_lambda = sy.lambdify(var_list, gradient)
    neg_grad_dir = -1 * grad_lambda(*point)

    for i in range(1000):
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
    return f_xap <= f_x + (c_1 * step_length * search_direction.T @ g_x) # '@' does matrix mult



def check_wolfe_condition(gradient: Callable, cur_point: sy.Matrix, search_direction: sy.Matrix,
                          step_length: float, c_2 = 0.1):
    #TODO: use for quasi-newton and conjugate gradient, too strong for arbitrary gradient
    g_x = gradient(*cur_point)
    g_xap = gradient(*(cur_point + step_length*search_direction))
    return search_direction.T * g_xap >= c_2 * search_direction.T * g_x