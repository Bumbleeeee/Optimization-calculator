import sympy
#will this handle sin, cos, etc. fine or should I import them? Need to test
import newton
import dim_one_algs
import multidim_algs
import sys
import helpers

runMap = {'1': newton.NewtonOptimizationMethod, '2': newton.NewtonRootFindingMethod, '3': dim_one_algs.GoldenSectionSearch,
          '4': multidim_algs.GradientMethod, '5': dim_one_algs.BisectionSearch, '6': dim_one_algs.FibonacciSearch }
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
            return f

def main():

    select_screen()

    method = choose_method()

    method_obj = method()

    #TODO: need a better way to print because the output is ugly rn - perhaps build it into classes
    print(method_obj.run_method())


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
