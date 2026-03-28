import pytest
import helpers
from multidim_algs import GradientMethod
import sympy
import functions.multidim as fm
import functions.onedim as fo

END_CONDITIONS = [
    (None, 200), # fixed number of iterations
    (helpers.euclidian_distance, 1e-6) # max distance between successive iterates
]

def gradient_descent_helper(func, tol, end_cond, start_point):
    method_obj = GradientMethod(func.f, sympy.oo, sympy.Matrix(start_point), end_cond)
    method_obj.run_method()
    assert(helpers.euclidian_distance(method_obj.get_cur_iterate(), func.x_opt) <= tol)


@pytest.mark.parametrize("end_cond", END_CONDITIONS)
@pytest.mark.parametrize("start_point", fm.rosenbrock.start_points)
def test_rosenbrock(end_cond, start_point):
    gradient_descent_helper(fm.rosenbrock, 1e-2, end_cond, start_point)


@pytest.mark.parametrize("end_cond", END_CONDITIONS)
@pytest.mark.parametrize("start_point", fo.parabola.start_points)
def test_parabola(end_cond, start_point):
    gradient_descent_helper(fo.parabola, 1e-6, end_cond, start_point)