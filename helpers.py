import sympy
from typing import Tuple, Union, Callable

import helpers


def euclidianDistance(x, y):
    if not isinstance(x, list): x = [x]
    if not isinstance(y, list): y = [y]

    if len(x) != len(y):
        print("Cannot calculate the distance between two points in different dimensions")
        return -1

    distance = 0
    for i in  range(len(x)):
        distance += (x[i] - y[i]) ** 2

    return sympy.sqrt(distance) # leaves irrationals unevaluated for better precision


def getEndCondition() -> Tuple[Callable, Union[int, float]]:
    endConditionsDict = { '1': ["Fixed number of iterations", int, None],
                          '2': ["Maximum distance between points", float, helpers.euclidianDistance] }

    for key, value in endConditionsDict.items():
        print(key + ". " + value[0])

    while True:
        ecType = input("Enter the number of the error type: ")
        if ecType not in endConditionsDict.keys():
            print("Please enter a valid integer")
        else:
            break

    valueType = endConditionsDict[ecType][1]
    while True:
        try:
            ecValue = abs(valueType(input("Enter an end condition value: ")))
            break
        except ValueError:
            print("Please enter a valid end condition number based on the chosen type")

    return ecType, ecValue







