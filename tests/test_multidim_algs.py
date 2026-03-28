import multidim_algs as mda
import pytest
import sympy

locals_map = {'e': sympy.E}

FUNCS_AND_SYMBOLS = [
    (sympy.sympify("3*x^2 + 1"), sympy.sympify("3*x_1^2 + 1"), sympy.symbols("x_1,"), 1),
    (sympy.sympify("1"), sympy.sympify("1"), sympy.symbols("x_1,"), 1),
    (sympy.sympify("e^x+y^2+sin(z)+x*pi", locals=locals_map), sympy.sympify("e^x_1+x_2^2+sin(x_3)+x_1*pi", locals=locals_map), sympy.symbols("x_1, x_2, x_3"), 3),
    (sympy.sympify("x_1 + x_2 + x_3 + x_4 + x_5"), sympy.sympify("x_1 + x_2 + x_3 + x_4 + x_5"), sympy.symbols("x_1, x_2, x_3, x_4, x_5"), 5)
]

@pytest.mark.parametrize("fs", FUNCS_AND_SYMBOLS)
def test_create_symbols(fs):
    grad_obj = mda.GradientMethod(fs[0], sympy.oo, sympy.Matrix.zeros(fs[3], 1), (None, 1))
    assert grad_obj.create_symbols() == fs[2]
    assert grad_obj.expression == fs[1]
    grad_obj.method_iteration()

