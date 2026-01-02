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

    if (f1 > f2): return x1, b
    else: return a, x2

def goldenSectionSearch(f, a, b, numIters = 10):
    for i in range(numIters):
        a, b = goldenSectionIter(f, a, b)
    return a, b
