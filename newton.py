import sympy

x = sympy.symbols('x')

def newton_root_iter(func, point):

    dfx = sympy.diff(func, x).evalf(subs={x: point})

    if dfx == 0:
        return sympy.oo

    return point - (func.evalf(subs={x: point}) / dfx) #TODO: maybe want to chop, idk (line 33 as well)

def newton_root_method(f, point, num_iters=10):
    for i in range (num_iters):
        point = newton_root_iter(f, point)
        if point == sympy.oo:
            print("failure - divide by zero")
            break
    return point


def newton_opt_iter(func, point):

    df = sympy.diff(func, x)
    dfx = df.evalf(subs={x: point})
    d2f = sympy.diff(df, x)
    d2fx = d2f.evalf(subs={x: point})

    if d2fx == 0:
        return sympy.oo

    return point - (dfx / d2fx) #maybe want to chop, idk

def newton_opt_method(f, point, num_iters=10):
    for i in range (num_iters):
        point = newton_opt_iter(f, x)
        if point == sympy.oo:
            print("failure - divide by zero")
            break
    return point

def newton_start():
    while True:
        try:
            start_point = float(input("Enter a starting point: "))
            return start_point
        except ValueError:
            print("Invalid input, please enter a real number")
