import time
import numpy as np

M = np.array(
    [
        ["A", 1],
        ["B", 2],
        ["C", 3],
        ["D", 5],
        ["E", 10],
    ]
)

elements = M[:, 0]  # All rows, first column
weights = M[:, 1].astype(int)  # All rows, second column, convert to integer

probabilities = weights / np.sum(weights)


def draw_element(elements, probabilities):
    return np.random.choice(elements, p=probabilities)


def print_probabilities():
    for i in range(len(elements)):
        print(f"{elements[i]}: {probabilities[i]*100}%")


def wheel_of_fortune():
    # Spin the wheel
    print("Spinning the wheel...")
    for i in range(5):
        print(draw_element(elements, probabilities))
        time.sleep(1)

    # Choose and print the final result
    print("Final result:", draw_element(elements, probabilities))


if __name__ == "__main__":
    print_probabilities()
    wheel_of_fortune()
