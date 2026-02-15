import sympy
#will this handle sin, cos, etc. fine or should I import them? Need to test
import newton
import dim_one_algs
import multidim_algs
import sys
import helpers

runMap = {'1': newton.newton_opt_method, '2': newton.newton_root_method, '3': dim_one_algs.golden_section_search,
          '4': multidim_algs.gradient_method, '5': dim_one_algs.bisection_search, '6': dim_one_algs.fibonacci_search }
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



    # get number of iterations
    while True:
        try:
            num_iters = abs(int(input("Enter number of iterations: ")))
            break
        except ValueError:
            print("Please enter an integer")

    if method_num == '1' or method_num == '2':
        # 1D algs with starting point
        start_point = newton.newton_start()
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
        point = multidim_algs.get_point()

        # get step size
        step_size_func = multidim_algs.get_step_size_input()

        #TODO: extend this to all functions in place of 'num_iters'
        ec_func, ec_value = helpers.get_end_condition()

        print("Final solution:")
        sympy.pprint(method(expr, sympy.Matrix(point), step_size_func, ec_func, ec_value))

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
