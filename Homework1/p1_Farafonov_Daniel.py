import math
import matplotlib.pyplot as plt

while True:
    a = input("Enter a: ")
    if a == "":
        break
    b = input("Enter b: ")
    c = input("Enter c: ")

    a = float(a)
    b = float(b)
    c = float(c)

    disc = b ** 2 - 4 * a * c

    if disc < 0:
        print("no real solutions")
        xopt = -b / (2 * a)
        xmin = xopt - 5
        xmax = xopt + 5
    elif disc == 0:
        x1 = -b / (2 * a)
        print("one solution: {:.5f}".format(x1))
        xmin = x1 - 5
        xmax = x1 + 5
    else:
        x1 = (-b - math.sqrt(disc)) / (2 * a)
        x2 = (-b + math.sqrt(disc)) / (2 * a)
        print("two solutions: x1={:.5f} x2={:.5f}".format(x1, x2))
        xmin = min(x1, x2) - 2
        xmax = max(x1, x2) + 2

    xs = [xmin + i * (xmax - xmin) / 149 for i in range(150)]
    ys = [a * x ** 2 + b * x + c for x in xs]

    plt.plot(xs, ys, "b.")
    plt.show()
