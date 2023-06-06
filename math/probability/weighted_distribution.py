import time
import numpy as np

elements = ["A", "B", "C", "D", "E"]
weights = [1, 2, 3, 5, 100]
probabilities = weights / np.sum(weights)


def draw_element(elements, probabilities):
    return np.random.choice(elements, p=probabilities)


def wheel_of_fortune():
    # Spin the wheel
    print("Spinning the wheel...")
    for i in range(5):
        print(draw_element(elements, probabilities))
        time.sleep(1)

    # Choose and print the final result
    print("Final result:", draw_element(elements, probabilities))


if __name__ == "__main__":
    wheel_of_fortune()
