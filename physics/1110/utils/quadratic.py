import math

def solve_quadratic(a, b, c):
    """
    Solves the quadratic equation ax^2 + bx + c = 0.
    Returns a tuple of real or complex roots.
    """
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return (root1, root2)
    elif discriminant == 0:
        root = -b / (2*a)
        return (root,)
    else:
        real_part = -b / (2*a)
        imag_part = math.sqrt(-discriminant) / (2*a)
        return (complex(real_part, imag_part), complex(real_part, -imag_part))

# Example usage:
# roots = solve_quadratic(1, -3, 2)
# print(roots)

if __name__ == "__main__":
    a = float(input("Enter coefficient a: "))
    b = float(input("Enter coefficient b: "))
    c = float(input("Enter coefficient c: "))
    roots = solve_quadratic(a, b, c)
    print("Roots:", roots)