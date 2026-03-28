import sympy as sy
import functions.base_class as bc
from sympy.abc import x, y, z
import sympy


rosenbrock = bc.Function(
    name="Rosenbrock",
    f=sy.sympify("(1-x)^2 + (y-x^2)^2"),
    x_opt=(1, 1),
    variables=(x, y),
    start_points=[[-1.2, 1], [2, 2], [-2, 2], [70, -30], [-2, sympy.pi]]
)