import sympy
from typing import Tuple, Union, Callable



def euclidian_distance(x, y):
    if not isinstance(x, list): x = [x]
    if not isinstance(y, list): y = [y]

    if len(x) != len(y):
        print("Cannot calculate the distance between two points in different dimensions")
        return -1

    distance = 0
    for i in  range(len(x)):
        distance += (x[i] - y[i]) ** 2

    return sympy.sqrt(distance) # leaves irrationals unevaluated for better precision


def get_end_condition() -> Tuple[Callable, Union[int, float]]:
    end_conditions_dict = { '1': ["Fixed number of iterations", int, None],
                          '2': ["Maximum distance between points", float, helpers.euclidianDistance] }

    for key, value in end_conditions_dict.items():
        print(key + ". " + value[0])

    while True:
        ec_type = input("Enter the number of the error type: ")
        if ec_type not in end_conditions_dict.keys():
            print("Please enter a valid integer")
        else:
            break

    value_type = end_conditions_dict[ec_type][1]
    while True:
        try:
            ec_value = abs(value_type(input("Enter an end condition value: ")))
            break
        except ValueError:
            print("Please enter a valid end condition number based on the chosen type")

    return ec_type, ec_value







