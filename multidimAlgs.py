import sympy
import helpers

x, y, z = sympy.symbols('x y z')
# note the use of point-direction-stepsize so individual iterations should probably handle the step size
# the method func probably only handles the type
#       (just pass through to iter which delegates the step size work elsewhere right before returning)
# user should be able to enter a number, function, OR choose optimal step size
# WHEN ENTERING A FUNCTION NOTE THE ITER NUM STARTS AT 1 -- need to make this clear



def findStepSize(func, stepSizeFunc, iterNum):
    if stepSizeFunc == sympy.oo:
        #TODO: optimal step size
        # phi(a) = f(x - a*f'(x))
        # will be hard to do a perfectly optimal step size but could do smth like Armijo backtracking algorithm fairly easily
        # lots of conditions that can be used, page 4 of ch5
        return 0.25
    else:
        return stepSizeFunc.evalf(subs={x : iterNum})


def gradientIteration(expr, point, iterNum, varList, stepSizeFunc):
    variables = sympy.Matrix(varList)
    subsDict = {}
    for i in range(len(variables)):
        subsDict[variables[i]] = point[i]

    gradient = sympy.Matrix([expr]).jacobian(variables).T
    stepSizeNum = findStepSize(expr, stepSizeFunc, iterNum)
    #print(stepSizeNum)
    return point - gradient.evalf(subs=subsDict) * stepSizeNum


def gradientMethod(expr, point, stepSizeFunc, numIters = 10, errorType = 'iter'):
    # create enough vars
    x_1 = sympy.symbols('x_1')
    varString = " ".join(f"x_{i+1}" for i in range(point.__len__()))
    x_symbols = sympy.symbols(varString, seq=True)

    # remove x,y,z if present
    xyzList = [x, y, z]
    for i in range(min(point.__len__(), 3)):
        expr = expr.subs(xyzList[i], x_symbols[i])

    # run iters
    if errorType == 'iter':
        for i in range(numIters):
            point = gradientIteration(expr, point, i+1, x_symbols, stepSizeFunc)
        return point

    else: #TODO: this is dangerous because it may never converge
        while True:
            newPoint = gradientIteration(expr, point, i+1, x_symbols, stepSizeFunc)
            if helpers.euclidianDistance(point, newPoint) < 0.05:
                return newPoint
            else:
                point = newPoint


def getPoint():
    while True:
        try:
            pointStr = input("Enter a starting point. For multiple dimensions, separate with a space: ")
            pointListStr = pointStr.split()
            point = []
            for p in pointListStr:
                point.append(float(p))
            return point
        except ValueError:
            print("Please enter real numbers for each coordinate.")


def getStepSizeInput():
    while True:
        stepSize = input("\nEnter step size. "
                         "\nIt can be a constant, a function of 'x' - the iteration number (starting at 1), "
                         "\nor type 'optimal' to use the optimal step size at each iteration: ")
        if (stepSize.lower() == 'optimal'):
            stepSize = sympy.oo
            break
        else:
            stepSize = sympy.sympify(stepSize)
            # eval at 1 should be safe since first iter must evaluate at 1
            if (sympy.ask(sympy.Q.real(stepSize.evalf(subs={x: 1}))) == True):
                break
            else:
                print("\nPlease enter a valid step size.")

    return stepSize
