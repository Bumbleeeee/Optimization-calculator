import helpers
from helpers import compute_gradient
import sympy
import pytest
from typing import Tuple

locals_map = {'e': sympy.E}


def test_euclidian_distance():
    assert (helpers.euclidian_distance([1], [-1]) == 2)
    assert (helpers.euclidian_distance([1, 2], [0, 0]) == sympy.sqrt(5))
    assert (helpers.euclidian_distance([1], [1, 2]) == -1)
    assert (helpers.euclidian_distance([], []) == 0)


FUNC_VAR_GRAD = [
    {"f": "x^2 + 2*x + 3", "v": "x", "g": ("2*x+2",)},
    {"f": "x^3 + y^2 + sin(z)", "v": "x, y, z", "g": ("3*x^2", "2*y", "cos(z)")},
    {"f": "x^3*y + sin(x)*y^2 + e^x*sin(z)", "v": "x, y, z",
     "g": ("y*3*x^2 + cos(x)*y^2 + e^x*sin(z)", "x^3 + 2*y*sin(x)", "cos(z)*e^x")},
    {"f": "1", "v": "x", "g": ("0",)}
]


@pytest.mark.parametrize("params", FUNC_VAR_GRAD)
def test_compute_gradient(params):
    func = params["f"]
    var_string = params["v"]
    g: Tuple[str] = params["g"]

    grad_list = []
    for string in g:
        grad_list.append([sympy.sympify(string, locals=locals_map)])

    assert compute_gradient(sympy.sympify(func, locals=locals_map), sympy.symbols(var_string + ",")) == sympy.Matrix(
        grad_list)


def test_compute_fib_nums():
    assert helpers.compute_fib_nums(-2) == []
    assert helpers.compute_fib_nums(0) == []
    assert helpers.compute_fib_nums(1) == [1]
    assert helpers.compute_fib_nums(2) == [1, 1]
    assert helpers.compute_fib_nums(5) == [1, 1, 2, 3, 5]
