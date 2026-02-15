import sympy

x = sympy.symbols('x')
PHI = (3-sympy.sqrt(5)) / 2

def get_range():
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

def golden_section_iter(f, a, b):
    phi_approx = PHI.evalf()
    x1 = a + phi_approx * (b-a)
    x2 = a + (1-phi_approx) * (b-a)
    f1 = f.evalf(subs={x: x1})
    f2 = f.evalf(subs={x: x2})

    if f1 > f2: return x1, b
    else: return a, x2

def golden_section_search(f, a, b, num_iters=10):
    for i in range(num_iters):
        a, b = golden_section_iter(f, a, b)
    return a, b


def bisection_iter(f, a, b):
    # works on the assumption that f'(a) < 0, f'(b) > 0
    midpoint = (a+b) / 2.0
    dfx = f.diff(x).evalf(subs={x: midpoint})
    if dfx < 0:
        return midpoint, b
    elif dfx > 0:
        return a, midpoint
    else:
        return midpoint, midpoint

def bisection_search(f, a, b, num_iters=10):
    for i in range(num_iters):
        a, b = bisection_iter(f, a, b)
        if a == b: break
    return a, b


def fibonacci_iter(f, a, b, rho):
    a1 = a + rho * (b-a)
    b1 = a + (1-rho) * (b-a)
    fa1 = f.evalf(subs={x: a1})
    fb1 = f.evalf(subs={x: b1})

    if fa1 > fb1:
        return a1, b
    else:
        return a, b1


def fibonacci_search(f, a, b, num_iters=10, epsilon=0.05):
    fib_numbers = [1, 1] # fibNumbers[i] = ith fibonacci number
    for i in range(2, num_iters+2):
        fib_numbers.append(fib_numbers[i-1] + fib_numbers[i-2])

    for i in range(num_iters):
        rho_i = 1 - (fib_numbers[num_iters-i] / fib_numbers[num_iters-i+1])
        if i == num_iters-1:
            rho_i -= epsilon

        a, b = fibonacci_iter(f, a, b, rho_i)

    return a, b