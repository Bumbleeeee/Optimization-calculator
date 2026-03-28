import sympy as sy
from sympy.abc import x, y, z
from typing import List


class Function:

    def __init__(self, name: str, f, start_points: List[List[float]], x_opt: tuple = None, variables: tuple = (x, y, z)):
        self.f = f
        self.grad = sy.Matrix([f]).jacobian(variables).T
        self.x_opt = x_opt
        self.name = name
        self.start_points = start_points

        self.lam_f = sy.lambdify(variables, f)
        self.lam_grad = sy.lambdify(variables, self.grad)
