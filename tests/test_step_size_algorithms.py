import sympy as sy
import pytest

import helpers
import step_size_algorithms as ssa
from step_size_algorithms import ExtraFuncData
import math


def test_cubic_interpolation():
    var_list = sy.symbols("x,")
    func = sy.sympify("x^2 + sin(x)")
    point = sy.Matrix([2.9])

    f_lambda = sy.lambdify(var_list, func, modules=["sympy"])
    gradient = helpers.compute_gradient(func, var_list)
    grad_lambda = sy.lambdify(var_list, gradient, modules=["sympy"])
    neg_grad_dir = -1 * grad_lambda(*point)
    fd = ExtraFuncData(grad_lambda, point, neg_grad_dir)

    assert math.isclose(ssa.cubic_interpolation(f_lambda, fd, 0, 1), 0.6675483177)
    assert math.isclose(ssa.cubic_interpolation(f_lambda, fd, 0.7, 1), 0.6941285679)

    # safety check cases (divide a_1 by 2 b/c too close or far)
    assert ssa.cubic_interpolation(f_lambda, fd, 1.3, .7) == 0.35 # would be 0.695 so too close to a_1
    assert ssa.cubic_interpolation(f_lambda, fd, 1, 8) == 4 # would be 0.55 so too far from a_1
