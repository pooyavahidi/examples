import pandas as pd
import numpy as np


# DataFrame represents tabular data. Under the hood, data stored in one or
# multiple two-dimensional blocks rather than a list, dict or some other
# collection of one-dimensional arrays.


def create_df_using_dict():
    solar_system_data = {
        "planet": ["Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
        "radius": [6371, 3390, 69911, 58232, 25362, 24622],
        "moons": [1, 2, 79, 62, 27, 14],
    }

    df = pd.DataFrame(solar_system_data)
    print(df)

    # Selects the first five rows
    print(df.head())

    # Selects the last five rows
    print(df.tail())

    # Define a custom index, instead of non-negative integers
    df1 = pd.DataFrame(
        solar_system_data,
        index=["First", "Second", "Third", "Fourth", "Fifth", "Sixth"],
    )
    print(df1)

    # Adding a new column.
    df2 = pd.DataFrame(
        solar_system_data,
        columns=["planet", "moons", "radius", "distance_From_Sun"],
    )
    # The name of existing columns will be matched, any new columns will be
    # shown with values of NaN
    print(df2)


def retrieve_from_df():
    solar_system_data = {
        "planet": ["Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
        "radius in km": [6371, 3390, 69911, 58232, 25362, 24622],
        "moons": [1, 2, 79, 62, 27, 14],
    }

    df = pd.DataFrame(solar_system_data)
    print(df)

    # Reading values of column "planet"
    planets = df.planet
    print(planets)

    # This is actually a Series
    print(type(planets))

    # The same as above, it can be used for time that column name is not a
    # proper python variable
    print(df["radius in km"])

    # Read by position or name of the index. Retrieve row with index=2
    print(df.loc[2])

    # Read values of df. It returns a two-dimentional ndarray.
    print(df.values)
    print(df.values[3][2])

    # Slicing from index 2 to 4. Pandas is different from Python as the last
    # index is inclusive
    print(df[2:4])

    # Slice from 0 to position 2 (included)
    print(df[:2])

    # Filtering with all the rows with moons>2
    print(df[df["moons"] > 2])

    # using loc to select a subset of rows and columns.
    # The following choose row index 3, and only columns of planet and moons
    print(df.loc[3, ["planet", "moons"]])

    # iloc (integer loc) is the same but using the integer indexes.
    # The following provides the same result as above. 0 and 2 are indexes of
    # columns planet and moons
    print(df.iloc[3, [0, 2]])

    # Print number of total moons of all planets
    print(df.sum().loc["moons"])

    # Print number of total moons of planets which has radius > 25,000KM
    print(df[df["radius in km"] > 25000].sum().loc["moons"])


def modify_df():
    solar_system_data = {
        "planet": ["Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
        "radius": [6371, 3390, 69911, 58232, 25362, 24622],
        "moons": [1, 2, 79, 62, 27, 14],
    }

    df = pd.DataFrame(solar_system_data)

    # Add a new column which made of multiplication of column radius and 1000
    df["radius in meter"] = df["radius"] * 1000
    print(df)

    # Add a new boolean column for planets which radius bigger 50,000km
    df["is_large"] = df.radius > 50000
    print(df)

    # Or we can simply update an existing column. Convert redius to miles
    df.radius = df.radius * 0.62
    print(df)

    # Add a new column as the row number
    df["row number"] = np.arange(1, 7)
    print(df)

    # Add a series to dataframe.
    # The following adds length_of_year column to the df, however, the value
    # for row indexes of 1,2 and 5 will be set and the rest of rows will have
    # NaN value.
    length_of_year = pd.Series([164.81, 1.88, 11.86], index=[5, 1, 2])
    df["length_of_year"] = length_of_year
    print(df)

    # Delete a column
    del df["radius"]
    print(df)


def create_df_using_different_types():
    # List
    planets = ["Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    df = pd.DataFrame(planets)
    print(df)

    # Tuple
    planets = ("Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune")
    df = pd.DataFrame(planets)
    print(df)

    # Set
    planets = {"Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"}
    df = pd.DataFrame(planets)
    print(df)

    # Dictionary
    dic = {
        "planet": ["Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
        "radius": [6371, 3390, 69911, 58232, 25362, 24622],
        "moons": [1, 2, 79, 62, 27, 14],
    }
    df = pd.DataFrame(dic)
    print(df)

    # The following results in the similar structure as above
    dic = [
        {"planet": "Earth", "radius": 6371, "moons": 1},
        {"planet": "Mars", "radius": 3390, "moons": 2},
        {"planet": "Jupiter", "radius": 3390, "moons": 79},
        {"planet": "Saturn", "radius": 3390, "moons": 62},
    ]
    df = pd.DataFrame(dic)
    print(df)

    dic = [
        ["Earth", 6371, 1],
        ["Mars", 3390, 2],
        ["Jupiter", 3390, 79],
        ["Saturn", 3390, 62],
    ]
    df = pd.DataFrame(dic, columns=["planet", "radius", "moons"])
    print(df)

    # Dictionary of dictionary
    dic = {
        "Earth": {"radius": 6371, "moons": 1},
        "Mars": {"radius": 3390, "moons": 2},
        "Jupiter": {"radius": 3390, "moons": 79},
        "Saturn": {"radius": 3390, "moons": 62},
    }
    df = pd.DataFrame(dic)
    print(df)

    # Transpose the df which swaps columns and rows
    print(df.T)


# create_df_using_dict()
# retrieve_from_df()
# modify_df()
create_df_using_different_types()
