# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import sympy
#from sympy import sin #or use sympy.sin, so probably want to import * otherwise getting this stuff as input might be weird
import Newton
import sys

runMap = {'1' : Newton.newtonOptMethod, '2' : Newton.newtonRootMethod }
methods = { '1' : "Newton's Optimization", '2' : "Newton's Root" }

def selectScreen():

    for key, value in methods.items():
        print(key + ". " + value)

def chooseMethod():
    while True:
        methodNum = input("Enter which number method to use, or Q to quit: ").strip().upper()
        if (methodNum == 'Q'):
            sys.exit(-1)
        f = runMap.get(methodNum)
        if (f == None):
            print("Invalid method")
        else:
            print("Chose", methods[methodNum], "method\n")
            return f

def main():
    selectScreen()

    f = chooseMethod()

    expr = input("Enter an expression. Please use '*' explicitly for all multiplication: ")
    expr = sympy.sympify(expr)

    while True:
        try:
            startPoint = int(input("Enter a starting point: "))
            break
        except ValueError:
            print("Invalid input, please enter a valid integer")

    print("Expression:", expr, "\tStarting Point: ", startPoint)

    print("\nFinal solution:", f(expr, startPoint))



    ''' end main function'''



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

'''
todo:
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
    - ii.  
'''