import sympy
#will this handle sin, cos, etc. fine or should I import them? Need to test
import newton
import dim_one_algs
import multidim_algs
import sys
import helpers
from typing import Callable


# TODO: a bit repetitive in here, maybe can consolidate
OPT_CONFIG = {
    "Gradient Descent": {
        "class": multidim_algs.GradientMethod,
        "params": {
            "function": helpers.get_func_to_optimize,
            "step_size_func": multidim_algs.get_step_size_input,
            "start_point": lambda: sympy.Matrix(helpers.input_multi_float("Enter a starting point. For multiple dimensions, separate with a space: ")),
            "end_conditions": helpers.get_end_condition
        }
    },
    "Newton's Optimization": {
        "class": newton.NewtonOptimizationMethod,
        "params": {
            "function": helpers.get_func_to_optimize,
            "start_point": lambda: helpers.input_multi_float()[0],
            "end_conditions": helpers.get_end_condition
        }
    },
    "Newton's Root": {
        "class": newton.NewtonRootFindingMethod,
        "params": {
            "function": helpers.get_func_to_optimize,
            "start_point": lambda: helpers.input_multi_float()[0],
            "end_conditions": helpers.get_end_condition
        }
    },
    "Golden Section": {
        "class": dim_one_algs.GoldenSectionSearch,
        "params": {
            "function": helpers.get_func_to_optimize,
            "start_interval": dim_one_algs.get_range,
            "end_conditions": helpers.get_end_condition
        }
    },
    "Fibonacci search": {
        "class": dim_one_algs.FibonacciSearch,
        "params": {
            "function": helpers.get_func_to_optimize,
            "start_interval": dim_one_algs.get_range,
            "num_iters": dim_one_algs.get_num_iters,
            "epsilon": dim_one_algs.get_epsilon
        }
    },
    "Bisection search": {
        "class": dim_one_algs.BisectionSearch,
        "params": {
            "function": helpers.get_func_to_optimize,
            "start_interval": dim_one_algs.get_range,
            "end_conditions": helpers.get_end_condition
        }
    }

}


def select_screen(key_list: list):
    for i in range(len(key_list)):
        print(f"{i+1}. {key_list[i]}")

def choose_method() -> str:
    key_list = list(OPT_CONFIG.keys())
    select_screen(key_list)

    while True:
        try:
            method_num = input("Enter which number method to use, or Q to quit: ").strip().upper()
            if method_num == 'Q':
                sys.exit(-1)
            method_num = int(method_num)
            if 1 <= method_num <= len(key_list): break
        except ValueError:
            print("Invalid method")

    f_str = key_list[method_num-1]
    print(f"Chose {f_str} method\n")
    return f_str


def get_params(method_name: str):
    config = OPT_CONFIG.get(method_name)
    if config is None:
        print("Error - Invalid method")
        sys.exit(-1)

    args_dict = {}
    for param_name, getter_func in config["params"].items():
        args_dict[param_name] = getter_func()

    return args_dict


def main():

    method_name = choose_method()
    args_dict = get_params(method_name)

    # method_obj is initialized object of proper class for chosen optimization method
    method_obj = OPT_CONFIG[method_name]["class"](**args_dict)

    #TODO: need a better way to print because the output is ugly rn - perhaps build it into classes
    print(f"\nApproximate optimal solution: {method_obj.run_method()}")


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



#TODO: checks for initial conditions such as strict unimodality on the provided interval
#TODO: check if descent condition is satisfied, otherwise alter step size (for nonoptimal step size ofc)
#TODO: methods to find a search interval that satisfies strict unimodality (to guarantee ICs for dim1 algos)
#TODO: secant method for when newton's fails (or just to use in general)


# 'raise [exceptiontype]' to manually raise exception (instead of just printing failure and exiting)
