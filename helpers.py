import sympy
from typing import Tuple, Union, Callable

import helpers

def euclidian_distance(x, y):
    # TODO: maybe a better way to do this
    if isinstance(x, sympy.Matrix): x = x.flat()
    if isinstance(y, sympy.Matrix): y = y.flat()
    if not isinstance(x, list): x = [x]
    if not isinstance(y, list): y = [y]

    if len(x) != len(y):
        print("Cannot calculate the distance between two points in different dimensions")
        return -1

    distance = 0
    for i in  range(len(x)):
        distance += (x[i] - y[i]) ** 2

    return sympy.sqrt(distance) # leaves irrationals unevaluated for better precision


# return: end condition function, end condition threshold (int or float)
# note: checking the end condition is delegated to individual algorithm functions for now
def get_end_condition() -> Tuple[Callable, Union[int, float]]:
    end_conditions_dict = { '1': ["Fixed number of iterations", int, None],
                            '2': ["Maximum distance between points", float, helpers.euclidian_distance] }

    for key, value in end_conditions_dict.items():
        print(key + ". " + value[0])

    # get type of end condition
    while True:
        ec_type: str = input("Enter the number of the error type: ")
        if ec_type not in end_conditions_dict.keys():
            print("Please enter a valid integer")
        else:
            break

    value_type = end_conditions_dict[ec_type][1]

    # get threshold value for end condition
    while True:
        try:
            ec_value = abs(value_type(input("Enter an end condition value: ")))
            break
        except ValueError:
            print("Please enter a valid end condition number based on the chosen type")

    ec_func: Callable = end_conditions_dict[ec_type][2]
    return ec_func, ec_value




