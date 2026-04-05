from math import inf, isclose
import sympy as sy
from typing import Callable
from helpers import compute_gradient
from dataclasses import dataclass

MAX_STEPSIZE_ITERS = 100 # strictly positive integer

@dataclass
class ExtraFuncData:
    # store common data for step size algorithms in one place
    gradient: Callable #sympy lambdified func
    point: sy.Matrix
    search_dir: sy.Matrix


# TODO: want to be able to customize search direction?? also check to ensure descent direction
# TODO: algos only work if descent direction (otherwise not guaranteed to terminate)

# TODO: condition checks like armijo should take phi(a), phi(0) etc as args then just do condition checks
# TODO:     have some other function whose responsibility it is to calculate all this
# TODO:     would save like one gradient eval per iter


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
    # sufficient decrease condition

    phi_0 = func(*fd.point)
    phi_a = calc_phi_a(func, fd.point, fd.search_dir, step_length)
    phi_prime_0 = calc_phi_prime_a(fd, 0)
    step = c_1 * step_length * phi_prime_0

    return phi_a <= phi_0 + step


def check_wolfe_condition(fd: ExtraFuncData, step_length: float, c_2 = 0.1):
    phi_prime_a = calc_phi_prime_a(fd, step_length)
    phi_prime_0 = calc_phi_prime_a(fd, 0)
    return phi_prime_a >= c_2 * phi_prime_0


def check_strong_wolfe_condition(fd: ExtraFuncData, step_length: float, c_2 = 0.9):
    # TODO: use for quasi-newton and conjugate gradient, too strong for arbitrary gradient
    phi_prime_a = calc_phi_prime_a(fd, step_length)
    phi_prime_0 = calc_phi_prime_a(fd, 0)
    return abs(phi_prime_a) <= c_2 * abs(phi_prime_0)


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
    #alpha = strong_wolfe_line_search(f_lambda, ExtraFuncData(grad_lambda, point, neg_grad_dir), initial_alphas)
    return alpha


def calc_phi_a(func: Callable, point: sy.Matrix, direction: sy.Matrix, a: float) -> float:
    return float(func(*(point + a*direction))) # '*' to unpack the list into separate args


def calc_phi_prime_a(fd: ExtraFuncData, a: float) -> float:
    grad_xap = fd.gradient(*(fd.point + a*fd.search_dir))
    phi_prime_a = float((fd.search_dir.T @ grad_xap)[0, 0].evalf())
    return phi_prime_a


def cubic_interpolation(func: Callable, fd: ExtraFuncData, a_0: float, a_1: float):
    # from Nocedal and Wright

    phi_a_0 = calc_phi_a(func, fd.point, fd.search_dir, a_0)
    phi_a_1 = calc_phi_a(func, fd.point, fd.search_dir, a_1)
    phi_prime_a_0 = calc_phi_prime_a(fd, a_0)
    phi_prime_a_1 = calc_phi_prime_a(fd, a_1)

    d_1 = phi_prime_a_0 + phi_prime_a_1 - 3*((phi_a_0 - phi_a_1) / (a_0 - a_1))
    d_2 = ((a_1-a_0) / abs(a_1-a_0)) * sy.sqrt(d_1*d_1 - phi_prime_a_0*phi_prime_a_1)
    a_2 = a_1 - (a_1-a_0)*((phi_prime_a_1 + d_2 - d_1) / (phi_prime_a_1 - phi_prime_a_0 + 2*d_2))

    # safety checks
    epsilon = 0.1
    #note that a_i is always nonnegative
    #check for a_2 too close or far away from a_1
    if abs(a_2-a_1) < epsilon * a_1 or a_2 < epsilon * a_1:
        a_2 = a_1/2
    return a_2


def cubic_interpolation_zoom(func: Callable, fd: ExtraFuncData, alphas: tuple = (0, 1e10)):
    # Nocedal and Wright zoom algo
    # func, fd.gradient are sy.lambdified functions
    a_lo = alphas[0]
    a_j = 0
    a_hi = alphas[1]
    # TODO: doing multiple of the same evals b/c one in check_x_condition and another in here, need to fix
    for i in range(MAX_STEPSIZE_ITERS):
        # interpolate
        a_j = cubic_interpolation(func, fd, a_lo, a_hi)

        if (not check_armijo_condition(func, fd, a_j)) \
            or (calc_phi_a(func, fd.point, fd.search_dir, a_j) >= calc_phi_a(func, fd.point, fd.search_dir, a_lo)):
            a_hi = a_j

        else:
            # eval gradient at a_j (one time)
            phi_prime_a_j = calc_phi_prime_a(fd, a_j)

            if check_strong_wolfe_condition(fd, a_j):
                return a_j

            if phi_prime_a_j * (a_hi - a_lo) >= 0:
                # flip interval if +a direction has become ascent direction
                a_hi = a_lo

            a_lo = a_j

    return a_j



def strong_wolfe_line_search(func: Callable, fd: ExtraFuncData, alphas: tuple = (0, 1, 1e10)):
    # Nocedal and Wright strong wolfe line search algo

    a_prev = alphas[0] # alpha_i-1
    a_cur = alphas[1] # alpha_i
    a_max = alphas[2]
    i = 1

    a_opt = a_max # if never zoom, want to return a_max. Overridden from zoon

    while a_cur <= a_max:
        phi_a = calc_phi_a(func, fd.point, fd.search_dir, a_cur)
        phi_a_prev = calc_phi_a(func, fd.point, fd.search_dir, a_prev)

        if not check_armijo_condition(func, fd, a_cur) or (phi_a >= phi_a_prev and i > 1):
            a_opt = cubic_interpolation_zoom(func, fd, (a_prev, a_cur))
            break

        phi_prime_a = calc_phi_prime_a(fd, a_cur)

        if check_strong_wolfe_condition(fd, a_cur):
            # strong wolfe and armijo satisfied
            a_opt = a_cur
            break

        if phi_prime_a >= 0:
            # derivative positive so swap order of endpoints for zoom
            a_opt = cubic_interpolation_zoom(func, fd, (a_cur, a_prev))
            break

        #choose alpha_i+1
        # TODO: consider interpolation here
        a_prev = a_cur
        a_cur = 2*a_cur
        i += 1

    return a_opt


