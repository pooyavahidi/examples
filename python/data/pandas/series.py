import pandas as pd
import numpy as np

# Series are one-dimentional array-like objects containing a sequence of values
# of a type
def simple_series_using_array():
    seq = pd.Series([1, 2, 3, 4])
    print(seq)


def simple_series_custom_index():
    seq = pd.Series([1, 2, 3, 4], index=["a", "b", "c", "d"])
    print(seq)

    # reference to that value using custom index
    print(seq["c"])


def filtering():
    seq = pd.Series([1, 2, 3, 4])

    # Returns the boolean array for all the items in the array
    print(seq > 2)

    # Filter the series using the boolean
    print(seq[seq > 2])


def math_functions():
    seq = pd.Series([1, 2, 3, 4])

    # Raise all the items in the series to the power of 3
    print(seq**3)

    # Apply math functions on all the items of the series
    print(np.square(seq))


# Using Series as dictionaries


def using_series_as_dict():
    dic = {"key1": 1, "key2": 2}
    seq = pd.Series(dic)
    print(seq)
    print(seq[1])

    dic = {"key1": [1, 2], "key2": "value 2"}
    seq = pd.Series(dic)
    print(seq[0][1])

    dic = {"key1": [1, 2], "key2": {"inner_key1": [3, 4]}}
    seq = pd.Series(dic)
    print(seq[1]["inner_key1"][1])


def using_series_as_dict2():
    # Solar system's planet radius in KM
    solar_system_sizes_dict = {
        "Earth": 6371,
        "Ears": 3390,
        "Jupiter": 69911,
        "Saturn": 58232,
    }

    planet_sizes = pd.series(solar_system_sizes_dict)

    print(planet_sizes)

    print(planet_sizes["Mars"])

    # Creating a new Series with a new index.
    # It will automatically align match the indexes, for the new ones put value
    # of NaN, for missing ones, just drop it from the sequence.
    planet_size2 = pd.Series(
        solar_system_sizes_dict, index=["Venus", "Mars", "Jupiter", "Earth"]
    )
    print(planet_size2)

    # Return a boolean array of items. For the items with value NaN, it returns
    # True
    print(planet_size2.isnull())


def series_arithmetic():
    A = {"a": 1, "b": 2, "c": 3, "d": 4}
    B = {"a": 5, "b": 6, "c": 7, "d": 8}

    seq_A = pd.Series(A)
    seq_B = pd.Series(B)

    # Apply the arithmetic on each item which are aligned together based on
    # their index.
    print(seq_A + seq_B)
    print(seq_A * seq_B)

    # This one is missing index b. So, the result has b=NaN
    C = {"c": 9, "d": 10, "a": 11}
    seq_C = pd.Series(C)

    print(seq_A + seq_C)


def series_other_attributes():
    solar_system_sizes_dict = {
        "earth": 6371,
        "mars": 3390,
        "jupiter": 69911,
        "saturn": 58232,
    }

    planet_sizes = pd.Series(solar_system_sizes_dict)
    planet_sizes.name = "Planet Sizes"
    planet_sizes.index.name = "PlanetName"

    print(planet_sizes)


# using_series_as_dict()
# using_series_as_dict2()
# using_series_as_dict_multi_properties()
# series_arithmetic()
series_other_attributes()
