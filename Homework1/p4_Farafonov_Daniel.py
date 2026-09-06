import math
import matplotlib.pyplot as plt


def plot_function(fun_str, domain, ns):
    xmin, xmax = domain
    xs = [xmin + i * (xmax - xmin) / (ns - 1) for i in range(ns)]

    ys = []
    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    for x, y in zip(xs, ys):
        print("{:.4f}\t{:.4f}".format(x, y))

    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.show()


fun_str = input("Enter function with variable x: ")
xmin = float(input("Enter xmin: "))
xmax = float(input("Enter xmax: "))
ns = int(input("Enter number of samples: "))

plot_function(fun_str, (xmin, xmax), ns)
