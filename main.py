# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import sympy
#from sympy import sin #or use sympy.sin, so probably want to import * otherwise getting this stuff as input might be weird
import Newton
import dim_one_algs
import multidimAlgs
import sys

runMap = {'1': Newton.newton_opt_method, '2': Newton.newton_root_method, '3': dim_one_algs.golden_section_search,
          '4': multidimAlgs.gradient_method, '5': dim_one_algs.bisection_search, '6': dim_one_algs.fibonacci_search }
methods = { '1': "Newton's Optimization", '2': "Newton's Root", '3': "Golden Section",
            '4': "Gradient Descent", '5': "Bisection search", '6': "Fibonacci search" }

def select_screen():

    for key, value in methods.items():
        print(key + ". " + value)

def choose_method():
    while True:
        method_num = input("Enter which number method to use, or Q to quit: ").strip().upper()
        if method_num == 'Q':
            sys.exit(-1)
        f = runMap.get(method_num)
        if f is None:
            print("Invalid method")
        else:
            print(f"Chose {methods[method_num]} method\n")
            return f, method_num

def main():
    sympy.init_printing()
    select_screen()

    method, method_num = choose_method()

    expr = input("Enter an expression. "
                 "\n- For functions from R to R, use 'x' as the variable. "
                 "For functions from R^n to R, use 'x_1',...,'x_n' or x, y, z. "
                 "\n- Please use '*' explicitly for all multiplication.\n")
    expr = sympy.sympify(expr)

    # get number of iterations
    while True:
        try:
            num_iters = abs(int(input("Enter number of iterations: ")))
            break
        except ValueError:
            print("Please enter an integer")

    if method_num == '1' or method_num == '2':
        # 1D algs with starting point
        start_point = Newton.newton_start()
        print(f"Expression: {expr} \tStarting Point: {start_point}")
        print(f"\nFinal solution: x = {method(expr, start_point, num_iters)}")

    elif method_num == '3' or method_num == '5' or method_num == '6':
        # 1D algs with starting interval
        a, b = dim_one_algs.get_range()
        print(f"Expression: {expr} \tStarting Interval: [{a}, {b}]")
        left_bound, right_bound = method(expr, a, b, num_iters)
        print(f"\nFinal interval: [{left_bound}, {right_bound}]")

    elif method_num == '4':
        # multidim algs
        point = multidimAlgs.get_point()

        # get step size
        step_size_func = multidimAlgs.get_step_size_input()

        print("Final solution:")
        sympy.pprint(method(expr, sympy.Matrix(point), step_size_func, num_iters))

    ''' end main function'''



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

'''
todo: (NOTE THAT CURRENTLY THE "FINAL SOLUTION" IS THE APPROXIMATION OF THE INPUT VALUE WHERE THE OPTIMAL SOLUTION IS)
1. main logic and math (input, derivatives, etc)
    - i. derivatives (1st and 2nd) - focus on newton's method as the first one
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
    - ii.  checks for whether initial conditions for method are satisfied
    
'''
#TODO: more error types
    # did euclidian dist, need to handle inputting the epsilon where we break AND **** handling args for dif inputs ****
    #TODO: actually use the end condition function -- need to find a way to use it without checking conditions repeatedly
#TODO: optimal step size, handle certain constants (pi, e, etc) and irrationals (sqrt2) as inputs
#TODO: more methods and graph(?)/plot something
#TODO: can also implement a bisection method for root finding very easily, but maybe not worth it
#TODO: give final numeric solution for dim one methods? (currently just return an interval)
#TODO: command to quit at any time - maybe with 'await'

#TODO: maybe can simplify select conditions with '*' or '**' in functions for unknown number of params? Page 10 of cheat sheet
    # https://realpython.com/python-type-hints-multiple-types/
    # https://realpython.com/python-kwargs-and-args/#using-the-python-args-variable-in-function-definitions

#TODO: variable epsilon for fib method - could just prompt for it in the function itself, otherwise maybe similar soln to above line

#TODO: checks for initial conditions such as strict unimodality on the provided interval
#TODO: check if descent condition is satisfied, otherwise alter step size (for nonoptimal step size ofc)
#TODO: methods to find a search interval that satisfies strict unimodality (to guarantee ICs for dim1 algos)
#TODO: secant method for when newton's fails (or just to use in general)


# 'raise' [exceptiontype] to manually raise exception (instead of just printing failure and exiting)
