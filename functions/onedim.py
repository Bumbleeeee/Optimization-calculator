import sympy as sy
import functions.base_class as bc
from sympy.abc import x


parabola = bc.Function(
    name="Parabola",
    f=sy.sympify("(x-3)^2"),
    x_opt=(3,),
    variables=(x,),
    start_points=[[0.1], [1], [-5], [50]]
)

line = bc.Function(
    name="line",
    f=sy.sympify("x"),
    x_opt=None,
    variables=(x,),
    start_points=[[-50], [0], [0.1], [3]]
)

constant = bc.Function(
    name="constant",
    f=sy.sympify("1"),
    x_opt=None,
    variables=(x,),
    start_points=[[-50], [0], [0.1], [3]]
)