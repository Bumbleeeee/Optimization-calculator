import sympy
import helpers

x, y, z = sympy.symbols('x y z')
# note the use of point-direction-stepsize so individual iterations should probably handle the step size
# the method func probably only handles the type
#       (just pass through to iter which delegates the step size work elsewhere right before returning)
# user should be able to enter a number, function, OR choose optimal step size
# WHEN ENTERING A FUNCTION NOTE THE ITER NUM STARTS AT 1 -- need to make this clear



def find_step_size(func, step_size_func, iter_num):
    if step_size_func == sympy.oo:
        #TODO: optimal step size
        # phi(a) = f(x - a*f'(x))
        # will be hard to do a perfectly optimal step size but could do smth like Armijo backtracking algorithm fairly easily
        # lots of conditions that can be used, page 4 of ch5
        return 0.25
    else:
        return step_size_func.evalf(subs={x: iter_num})


# perform one iteration of the gradient method
def gradient_iteration(expr, point, iter_num, var_list, step_size_func):
    variables = sympy.Matrix(var_list)
    subs_dict = {}
    for i in range(len(variables)):
        subs_dict[variables[i]] = point[i]

    gradient = sympy.Matrix([expr]).jacobian(variables).T
    step_size_num = find_step_size(expr, step_size_func, iter_num)

    return point - gradient.evalf(subs=subs_dict) * step_size_num


def gradient_method(expr, point, step_size_func, num_iters=10, error_type='iter'):
    # create enough vars
    x_1 = sympy.symbols('x_1')
    var_string = " ".join(f"x_{i+1}" for i in range(point.__len__()))
    x_symbols = sympy.symbols(var_string, seq=True)

    # remove x,y,z if present
    xyz_list = [x, y, z]
    for i in range(min(point.__len__(), 3)):
        expr = expr.subs(xyz_list[i], x_symbols[i])

    # run iters
    if error_type == 'iter':
        for i in range(num_iters):
            point = gradient_iteration(expr, point, i+1, x_symbols, step_size_func)
        return point

    else: #TODO: this is dangerous because it may never converge
        while True:
            new_point = gradient_iteration(expr, point, i+1, x_symbols, step_size_func)
            if helpers.euclidian_distance(point, new_point) < 0.05:
                return new_point
            else:
                point = new_point


def get_point():
    while True:
        try:
            point_str = input("Enter a starting point. For multiple dimensions, separate with a space: ")
            point_list_str = point_str.split()
            point = []
            for p in point_list_str:
                point.append(float(p))
            return point
        except ValueError:
            print("Please enter real numbers for each coordinate.")


def get_step_size_input():
    while True:
        step_size = input("\nEnter step size. "
                         "\nIt can be a constant, a function of 'x' - the iteration number (starting at 1), "
                         "\nor type 'optimal' to use the optimal step size at each iteration: ")
        if step_size.lower() == 'optimal':
            step_size = sympy.oo
            break
        else:
            step_size = sympy.sympify(step_size)
            # eval at 1 should be safe since first iter must evaluate at 1
            if sympy.ask(sympy.Q.real(step_size.evalf(subs={x: 1}))):
                break
            else:
                print("\nPlease enter a valid step size.")

    return step_size
