# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import jax
import jax.numpy as jnp
import sympy
#from sympy import sin #or use sympy.sin, so probably want to import * otherwise getting this stuff as input might be weird

import newton

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.




# Press the green button in the gutter to run the script.
def test_func():
    print_hi('PyCharm')
    list1 = [1, 2, 3, 7, 9, 11, -1, 2]
    for item in list1:
        if item > 5: print(item)

    dict1 = {'g': 17, 't' : 8, 'p' : 10, 'a' : 1}
    for name, number in dict1.items():
        print(name, number - 5)

    for number in dict1.values():
        print(number)

    for i in dict1:
        print(i)

    if 'g' in dict1: print("YAY")
    else: print("SAD")

    f = lambda x: x ** 3 + 2 * x ** 2 - 3 * x + 1

    print(Newton.newtonIter(f, 1))
    dfdx = jax.grad(f)
    print(dfdx(1.))
    d2dx = jax.grad(dfdx)
    print(d2dx(1.)) #make sure to use non-integer inputs

    f2 = lambda x: x ** 2 # ** is for exponent
    print(Newton.newtonIter(f2, 1))
    print(Newton.newtonMethod(f2, 1, 5))
    print(Newton.newtonMethod(f2, 1))


    x, y = sympy.symbols('x y')
    #expr = x**3 + 2*y + sin(y) #looks ugly when displaying exponents but this is the right way to do it
    expr = input("Input expression: ")
    expr = sympy.sympify(expr)
    print(expr) # x+2*y
    print(expr - x) # 2y
    df = sympy.diff(expr, x)
    print(df)
    print(sympy.diff(expr, y))
    print(expr.evalf(subs={x : 2, y : 3}, chop=True))
    print(df.evalf(2, subs={x : 2, y : 3}, chop=True))
    print(df.evalf(2, subs={x : sympy.pi, y : 3}, chop=True))
    # use lambdify to eval if doing many evals (probably won't need, especially for simple methods)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

'''
todo:
1. main logic and math (input, derivatives, etc)
    - i. derivatives (1st and 2nd) - focus on newton's method as the first one -->  https://docs.jax.dev/en/latest/automatic-differentiation.html
    - ii. inputting the function so it doesn't have to be hard coded
2. selection of method, iterations/error etc
    - i. prompt for method
    - ii. prompt for error type
    - iii. prompt for maximum allowed error or number of iterations
3. plotting results (what are the results we want to plot?)
    - i. (maybe) the value of the iteratively selected point as we iterated
4. expand to multivariable?? Need to see what functionality python has for that (like template in c++)
5. polish (this might need implementation with html or smth)
    - i. button for method (real gui), error type, etc
    - ii. checks / showing user what conditions are or are not met when using a method (i.e. caution when function is not everywhere convex or smth, although dunno how to impl)
'''