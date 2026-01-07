import sympy

x = sympy.symbols('x')
phi = (3-sympy.sqrt(5))/2

def getRange():
    while True:
        try:
            a = float(input("Enter the left end of the search interval: "))
            break
        except ValueError:
            print("Invalid input, please enter a real number")

    while True:
        try:
            b = float(input("Enter the right end of the search interval: "))
            break
        except ValueError:
            print("Invalid input, please enter a real number")

    return min(a, b), max(a, b) # swaps a and b if user entered right then left

def goldenSectionIter(f, a, b):
    phiApprox = phi.evalf()
    x1 = a + phiApprox * (b-a)
    x2 = a + (1-phiApprox) * (b-a)
    f1 = f.evalf(subs={x: x1})
    f2 = f.evalf(subs={x: x2})

    if f1 > f2: return x1, b
    else: return a, x2

def goldenSectionSearch(f, a, b, numIters = 10):
    for i in range(numIters):
        a, b = goldenSectionIter(f, a, b)
    return a, b


def bisectionIter(f, a, b):
    # works on the assumption that f'(a) < 0, f'(b) > 0
    midpoint = (a+b) / 2.0
    dfx = f.diff(x).evalf(subs={x : midpoint })
    if dfx < 0:
        return midpoint, b
    elif dfx > 0:
        return a, midpoint
    else:
        return midpoint, midpoint

def bisectionSearch(f, a, b, numIters = 10):
    for i in range(numIters):
        a, b = bisectionIter(f, a, b)
        if a == b: break
    return a, b


def fibonacciIter(f, a, b, rho):
    a1 = a + rho * (b-a)
    b1 = a + (1-rho) * (b-a)
    fa1 = f.evalf(subs={x : a1})
    fb1 = f.evalf(subs={x : b1})

    if fa1 > fb1:
        return a1, b
    else:
        return a, b1


def fibonacciSearch(f, a, b, numIters = 10, epsilon = 0.05):
    fibNumbers = [1, 1] # fibNumbers[i] = ith fibonacci number
    for i in range(2, numIters+2):
        fibNumbers.append(fibNumbers[i-1] + fibNumbers[i-2])

    for i in range(numIters):
        rho_i = 1 - (fibNumbers[numIters - i] / fibNumbers[numIters - i + 1])
        if i == numIters - 1:
            rho_i -= epsilon

        a, b = fibonacciIter(f, a, b, rho_i)

    return a, b

