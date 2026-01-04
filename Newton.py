import sympy

x = sympy.symbols('x')

def newtonRootIter(func, point):

    dfx = sympy.diff(func, x).evalf(subs={x:point})

    if dfx == 0:
        return sympy.oo

    return point - (func.evalf(subs={x:point}) / dfx) #maybe want to chop idk

def newtonRootMethod(f, x, numIters=10):
    for i in range (numIters):
        x = newtonRootIter(f, x)
        if x == sympy.oo:
            print("failure - divide by zero")
            break
    return x


def newtonOptIter(func, point):

    df = sympy.diff(func, x)
    dfx = df.evalf(subs={x:point})
    d2f = sympy.diff(df, x)
    d2fx = d2f.evalf(subs={x:point})

    if d2fx == 0:
        return sympy.oo

    return point - (dfx / d2fx) #maybe want to chop idk

def newtonOptMethod(f, x, numIters=10):
    for i in range (numIters):
        x = newtonOptIter(f, x)
        if x == sympy.oo:
            print("failure - divide by zero")
            break
    return x

def newtonStart():
    while True:
        try:
            startPoint = float(input("Enter a starting point: "))
            return startPoint
        except ValueError:
            print("Invalid input, please enter a real number")
