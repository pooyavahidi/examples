import pandas as pd
from matplotlib import pyplot as plt


def plot_x_and_y():
    data = [[1, 2], [2, 3], [3, 4]]

    df = pd.DataFrame(data, columns=["x", "y"])
    plt.plot(df.x, df.y, "o")
    plt.show()


def plot_x_and_y_custom_function():
    data = []
    for i in range(1, 10):
        # Custom function to derive y. (i / 2) could be any function.
        data.append([i, (i / 2)])

    df = pd.DataFrame(data, columns=["x", "y"])
    plt.plot(df.x, df.y, "o")
    plt.show()


plot_x_and_y_custom_function()
