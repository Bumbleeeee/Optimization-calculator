# Optimization-calculator
A calculator for various numerical optimization algorithms

### Installation
Run the following line to install the required packages:

     pip install -r requirements.txt 


### Important input information

- Variable names must be written **exactly** as stated, or the calculator will treat them as constants.

- For multidimensional algorithms (R<sup>n</sup> → R), n is determined by the number of elements in the starting point you provide

- When using x, y, z as the variables, you must use them in the written order. For example, a function from R<sup>2</sup> → R must be a function f(x, y).

- x = x_1, y = x_2, z = x_3, so using the two variable naming conventions in the same equation is generally not advised. For example, x + x_1 = 2*x_1. **Note how this is an expression of one variable, not two**.

- When entering a step size function, **note the iteration number starts at 1**. Ensure the function is defined for all integers {1,...,k}, where k is the number of iterations. Otherwise, the program will crash.

- Search algoithms (golden section, bisection, fibonacci) are currently implemented to find the min, subject to the requirement that the function is strictly unimodal on the provided interval. Checks and methods to find such an interval are coming soon.

- For maximization, enter the negative of the function you wish to maximize as each algorithm currently only handles minimization