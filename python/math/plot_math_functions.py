import matplotlib.pyplot as plt
import numpy as np


def plot_x_squared():
    # From -10 to 10
    x = np.arange(-1 * 10, 10)
    y = x**2
    plt.plot(x, y)


def plot_x_squared_points():
    # From -10 to 10
    x = np.arange(-1 * 10, 10)
    y = x**2
    plt.plot(x, y)
    # Add another plot (with the same x and y) but with option `o` which just
    # show the points, scattered.
    plt.plot(x, y, "o")


def plot_sin():
    # From 0 to 4pi with step of 0.1 to show the curves smoothly
    x = np.arange(0, 4 * np.pi, 0.1)
    y = np.sin(x)
    plt.plot(x, y)


def plot_sin_cosin():
    # From 0 to 4pi with step of 0.1 to show the curves smoothly
    x = np.arange(0, 4 * np.pi, 0.1)
    y = np.sin(x)
    z = np.cos(x)

    plt.plot(x, y)
    plt.plot(x, z)

    # Some information on the plot
    plt.title("Sin and Cosin")
    plt.xlabel("radian")
    plt.ylabel("y")
    plt.legend(["Sin", "Cosin"])


def plot_tangent():
    # From 0 to 4pi with step of 0.1 to show the curves smoothly
    x = np.arange(0, 4 * np.pi, 0.1)
    y = np.tan(x)

    # Matplot is not able to show the small values in the tangent curve because
    # the range of y is so large. So, we limit it to -4 to 4 and then cut down
    # anythine after 10 to remove the continuous line to the next curve.
    plt.ylim(-4, 4)
    tol = 10
    y[y > tol] = np.nan
    y[y < -tol] = np.nan
    plt.plot(x, y)


# plot_x_squared()
# plot_sin()
# plot_sin_cosin()
plot_tangent()

plt.show()
